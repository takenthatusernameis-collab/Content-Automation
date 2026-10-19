#!/usr/bin/env python3
"""Print a ready-to-edit experiment_decision.json skeleton from a packet.

Reads idea.md and, if present, uses experiment_loop to inspect comparison state.
Emits a JSON object that matches the load_decision contract, with decision
left as pending and source marked as needing a real documented review.
Does not invent keep/discard/retest decisions, reasons, or results.
Does not write files unless --write is given (and still leaves decision pending).
Does not call APIs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from experiment_loop import (  # noqa: E402
    ALLOWED_DECISIONS,
    RECORDED_DECISIONS,
    inspect_experiment,
)

def build_skeleton(comparison: dict | None, change: str = "") -> dict:
    metric = ""
    if comparison:
        metric = comparison.get("primary_metric", "")
    return {
        "_generated_by": "tools/experiment_decision_starter.py",
        "_warning": "TEMPLATE. Set an explicit decision (keep, discard, or retest), a real reason, and a documented source before use. experiment_loop.py rejects invented/placeholder sources and ignores the file until a numeric comparison exists.",
        "decision": "pending",
        "reason": "REPLACE: documented review reason such as 'delta positive and mechanism holds under spot-check'",
        "source": "REPLACE: documented observation such as 'human review of comparison on YYYY-MM-DD'",
        "primary_metric": metric or "average_view_duration_seconds",
        "notes": (
            "decision must be one of: " + ", ".join(RECORDED_DECISIONS) +
            ". source must not contain invented/assumed/placeholder/guess. "
            "File is ignored until comparison exists."
        ),
    }

def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the decision skeleton."""
    p = packet
    return [
        f"edit skeleton: set an explicit decision (keep/discard/retest), real reason, and documented non-placeholder source in the JSON above",
        f"write decision: python3 tools/experiment_decision_starter.py {p} --write",
        f"notes if needed: python3 tools/experiment_notes_starter.py {p}",
        f"package view: python3 tools/experiment_package_starter.py {p}",
        f"setup suggestions: python3 tools/experiment_setup_report.py {p}",
        f"quality scans: python3 tools/quality_scan.py {p} && python3 tools/claim_scan.py {p}",
        f"full production if needed: python3 tools/full_production_starter.py {p}",
        "do not invent decisions or results; experiment_loop.py rejects placeholder sources and ignores until comparison exists",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print experiment_decision.json skeleton. No invented decisions."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write experiment_decision.json to the packet (still with decision pending).",
    )
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}", file=sys.stderr)
        return 1
    report = inspect_experiment(path)
    comparison = None
    if report.get("record", {}).get("comparison"):
        comparison = report["record"]["comparison"]
    skeleton = build_skeleton(comparison)
    out = json.dumps(skeleton, indent=2) + "\n"
    print("EXPERIMENT DECISION STARTER (skeleton only; edit before use)")
    print(f"packet: {path.name}")
    print(f"comparison_present: {comparison is not None}")
    print(f"allowed_recorded_decisions: {', '.join(RECORDED_DECISIONS)}")
    print()
    print(out)
    print("Copy the JSON above to videos/<id>-<slug>/experiment_decision.json after")
    print("setting an explicit keep/discard/retest, a real reason, and a documented non-placeholder source.")
    print("Do not invent decisions or results. experiment_loop.py will reject invalid files and ignore them until comparison exists.")
    print()
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    if args.write:
        dest = path / "experiment_decision.json"
        dest.write_text(out, encoding="utf-8")
        print(f"wrote: {dest} (decision remains pending)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
