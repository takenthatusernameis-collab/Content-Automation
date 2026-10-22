#!/usr/bin/env python3
"""Print a ready-to-edit experiment_baseline.json skeleton from a packet.

Reads idea.md for topic and mechanism to ground a hypothesis template.
Lists the allowed single-variable changes from experiment_loop.py.
Prints a JSON object that matches the load_baseline contract, with baseline
null and source marked as needing a real documented observation.
Does not invent numeric baselines, sources, or results. Does not write files
unless --write is given (and still leaves baseline null). Does not call APIs.
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

from experiment_loop import ALLOWED_CHANGES  # noqa: E402
from idea_utils import extract as idea_extract  # noqa: E402

def extract(idea_text: str) -> tuple[str, str]:
    mech, _problem, topic = idea_extract(idea_text)
    return mech, topic

def build_skeleton(mech: str, topic: str, change: str = "hook") -> dict:
    if change not in ALLOWED_CHANGES:
        change = "hook"
    hyp_base = mech or topic or "the packet mechanism"
    hypothesis = (
        f"A stronger {change.replace('_', ' ')} that names '{hyp_base[:60]}' "
        "will raise average view duration on the first 30 seconds"
    )
    return {
        "_generated_by": "tools/experiment_baseline_starter.py",
        "_warning": "TEMPLATE. Edit hypothesis if needed. Set numeric baseline and documented source before use. experiment_loop.py rejects invented/placeholder sources and null baselines.",
        "hypothesis": hypothesis,
        "change": change,
        "primary_metric": "average_view_duration_seconds",
        "baseline": None,
        "source": "REPLACE: documented observation such as 'YouTube Studio analytics for video XYZ on YYYY-MM-DD'",
        "notes": (
            "change must be one of: " + ", ".join(ALLOWED_CHANGES) +
            ". baseline must be numeric. source must not contain invented/assumed/placeholder/guess."
        ),
    }

def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the baseline skeleton."""
    p = packet
    return [
        f"edit skeleton: set a real numeric baseline and documented non-placeholder source in the JSON above",
        f"write baseline: python3 tools/experiment_baseline_starter.py {p} --write",
        f"notes next: python3 tools/experiment_notes_starter.py {p}",
        f"full package: python3 tools/experiment_package_starter.py {p}",
        f"quality scans: python3 tools/quality_scan.py {p} && python3 tools/claim_scan.py {p}",
        f"full production if needed: python3 tools/full_production_starter.py {p}",
        "do not invent metrics; experiment_loop.py rejects null baselines and placeholder sources",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print experiment_baseline.json skeleton. No invented metrics."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    parser.add_argument(
        "--change",
        default="hook",
        help="Allowed change variable (default: hook). Must be in experiment_loop.ALLOWED_CHANGES.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write experiment_baseline.json to the packet (still with baseline null).",
    )
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}", file=sys.stderr)
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, topic = extract(text)
    skeleton = build_skeleton(mech, topic, args.change)
    out = json.dumps(skeleton, indent=2) + "\n"
    print("EXPERIMENT BASELINE STARTER (skeleton only; edit before use)")
    print(f"packet: {path.name}")
    print(f"mechanism: {mech or '(none)'}")
    print(f"topic: {topic or '(none)'}")
    print(f"allowed_changes: {', '.join(ALLOWED_CHANGES)}")
    print()
    print(out)
    print("Copy the JSON above to videos/<id>-<slug>/experiment_baseline.json after")
    print("setting a real numeric baseline and a documented non-placeholder source.")
    print("Do not invent metrics or results. experiment_loop.py will reject invalid files.")
    print()
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    if args.write:
        dest = path / "experiment_baseline.json"
        dest.write_text(out, encoding="utf-8")
        print(f"wrote: {dest} (baseline remains null)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
