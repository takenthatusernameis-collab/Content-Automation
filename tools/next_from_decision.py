#!/usr/bin/env python3
"""Print a next-video direction skeleton from a filled experiment_decision.json.

After a real comparison and decision exist, this tool reads the decision,
reason, and primary_metric and prints a short structured suggestion for the
next packet's topic direction. Does not invent a full idea.md, metrics,
or a new hypothesis. Does not write files or call APIs. Soft only.
Usage:
  python3 tools/next_from_decision.py path/to/experiment_decision.json
  python3 tools/next_from_decision.py videos/<packet>/experiment_decision.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from experiment_loop import RECORDED_DECISIONS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print next-video direction from a filled experiment decision. No invent."
    )
    parser.add_argument("path", help="Path to experiment_decision.json")
    args = parser.parse_args()
    path = Path(args.path)
    if not path.is_file():
        print(f"FAIL: file not found: {path}")
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL: not valid JSON: {e}")
        return 1
    if not isinstance(data, dict):
        print("FAIL: must be a JSON object")
        return 1
    decision = str(data.get("decision") or "").strip().lower()
    reason = str(data.get("reason") or "").strip()
    source = str(data.get("source") or "").strip()
    metric = str(data.get("primary_metric") or "").strip()
    if decision not in RECORDED_DECISIONS:
        print(f"HOLD: decision {decision!r} not in {sorted(RECORDED_DECISIONS)}; fill a real decision first.")
        print("Use the template at docs/experiment_decision.template.json and validate with experiment_template_validator.py.")
        return 0
    if not reason or not source:
        print("HOLD: reason or source missing; do not invent a direction.")
        return 0
    print("NEXT FROM DECISION (skeleton only; no invented topic or idea.md)")
    print(f"decision: {decision}")
    print(f"primary_metric: {metric or '(none)'}")
    print(f"reason: {reason[:120]}{'...' if len(reason) > 120 else ''}")
    print()
    print("Suggested next direction (edit before scaffolding; do not copy as-is):")
    direction_snippets = {
        "keep": "Apply the same winning change (that improved {metric}) to a closely related viewer problem while testing one new constraint. Preserve the mechanism that moved the metric in the desirable direction.",
        "discard": "Return to the prior baseline and avoid the tested change that moved {metric} in an undesirable direction. Document the failed variable so future packets do not repeat it.",
        "retest": "Retest the same change on a different but comparable topic to isolate the variable more cleanly or gather a second observation window before deciding keep or discard.",
    }
    snippet = direction_snippets.get(decision, "Review the decision and reason before choosing a next topic.")
    if decision == "keep":
        print("- Keep the tested change and apply the same mechanism to a closely related viewer problem.")
        print("- Next topic should preserve the winning variable while testing one new constraint.")
    elif decision == "discard":
        print("- Discard the tested change and return to the prior baseline mechanism.")
        print("- Next topic should avoid the failed variable and document why it was dropped.")
    else:  # retest
        print("- Retest the same change on a different but comparable topic.")
        print("- Next topic should isolate the variable more cleanly or collect a second observation window.")
    print()
    print("Ready direction snippet (copy/edit as starting language):")
    print(snippet.format(metric=metric or "the primary metric"))
    print()
    print("Next commands (after you write a one-line topic):")
    print("  python3 tools/new_idea.py 'your one-line topic here'")
    print("  python3 tools/local_packet_bootstrap.py videos/<new-packet>")
    print("Do not invent metrics. Do not scaffold until a real decision exists.")
    print("Complements experiment_template_validator.py and post_publish_sequence.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
