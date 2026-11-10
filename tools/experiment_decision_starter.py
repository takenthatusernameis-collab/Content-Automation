#!/usr/bin/env python3
"""Print a ready-to-edit experiment_decision.json skeleton from a packet.

Looks for an existing comparison in experiment_state or by inspecting the loop.
Prints a JSON object matching the load_decision contract, with decision left
as a template value so it cannot be accidentally accepted as real.
Does not invent a keep/discard/retest. Does not invent metrics or sources.
Does not call APIs or poll secrets. Soft only unless --write is given
(and the written file remains a template).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from experiment_loop import (  # noqa: E402
    RECORDED_DECISIONS,
    inspect_experiment,
    load_baseline,
)

def build_skeleton(primary_metric: str | None, packet_name: str) -> dict:
    metric = primary_metric or "average_view_duration_seconds"
    return {
        "_generated_by": "tools/experiment_decision_starter.py",
        "_warning": "TEMPLATE. Replace decision, reason, and source with a real documented review after a numeric comparison exists. experiment_loop.py rejects invented/placeholder sources and non-recorded decisions.",
        "decision": "TEMPLATE: replace with keep, discard, or retest",
        "reason": "TEMPLATE: replace with a short documented reason from the review after seeing the numeric delta",
        "source": "REPLACE: documented review such as 'Human review of YouTube Studio analytics on YYYY-MM-DD after observation window'",
        "primary_metric": metric,
        "notes": (
            f"decision must be one of: {', '.join(RECORDED_DECISIONS)}. "
            "reason and source are required. source must not contain invented/assumed/placeholder/guess. "
            "primary_metric should match the comparison if present."
        ),
        "packet": packet_name,
    }

def recommended_actions(packet: str) -> list[str]:
    p = packet
    return [
        "fill decision: set decision to keep/discard/retest, add real reason and non-placeholder source after reviewing the comparison",
        f"write template: python3 tools/experiment_decision_starter.py {p} --write",
        f"validate: python3 tools/experiment_template_validator.py {p}/experiment_decision.json",
        f"loop: python3 tools/experiment_loop.py {p}",
        "do not invent a decision; only record after a documented review of real metrics",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print experiment_decision.json skeleton. No invented decisions."
    )
    parser.add_argument("packet", help="Packet folder")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write experiment_decision.json to the packet (remains a template).",
    )
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    # Prefer metric from baseline if present; otherwise default
    baseline, _ = load_baseline(path)
    metric = None
    if baseline:
        metric = baseline.get("primary_metric")

    # Soft inspect to see if comparison already exists (does not write)
    try:
        report = inspect_experiment(path)
        comparison = (report.get("record") or {}).get("comparison")
        if isinstance(comparison, dict) and comparison.get("primary_metric"):
            metric = comparison["primary_metric"]
    except Exception:
        pass  # inspection may fail without upload state; skeleton still useful

    skeleton = build_skeleton(metric, path.name)
    out = json.dumps(skeleton, indent=2) + "\n"

    print("EXPERIMENT DECISION STARTER (skeleton only; edit before use)")
    print(f"packet: {path.name}")
    print(f"primary_metric: {metric or '(default)'}")
    print(f"allowed_decisions: {', '.join(RECORDED_DECISIONS)}")
    print()
    print(out)
    print("Copy the JSON above to videos/<id>-<slug>/experiment_decision.json after")
    print("a real numeric comparison exists and a documented review has been performed.")
    print("Do not invent a keep/discard/retest. experiment_loop.py will reject invalid files.")
    print()
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()

    if args.write:
        dest = path / "experiment_decision.json"
        dest.write_text(out, encoding="utf-8")
        print(f"wrote: {dest} (still a template; edit before the loop will accept it)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
