#!/usr/bin/env python3
"""Suggest a candidate experiment_decision.json skeleton once a numeric comparison exists.

Reuses inspect_experiment from experiment_loop.py. When a comparison is present
(gate COMPARED or action COMPARED), prints printable JSON stubs for keep / discard / retest
with the observed delta and direction noted. Source and reason left for human documentation.
Does not invent a decision, write files, or call APIs. Fail-closed if no comparison.
Reduces recurring labor of manually formatting the decision file after every future comparison.
Also surfaces a ready source_snippet so the human can document the observation source without inventing phrasing.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from experiment_loop import inspect_experiment, ALLOWED_DECISIONS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print candidate experiment_decision.json stubs from an existing comparison. No writes, no invent."
    )
    parser.add_argument("packet", help="Packet folder")
    args = parser.parse_args()
    packet = Path(args.packet).resolve()
    if not packet.is_dir():
        print(f"not a directory: {packet}", file=sys.stderr)
        return 1

    report = inspect_experiment(packet)
    comparison = report.get("record", {}).get("comparison")
    if not comparison or not isinstance(comparison, dict):
        print("HOLD: no numeric comparison yet (run experiment_loop.py after baseline + metrics; do not invent)")
        print("Fail-closed. Decision stays pending until comparison exists.")
        return 2

    direction = comparison.get("direction", "unknown")
    metric = comparison.get("primary_metric", "metric")
    delta = comparison.get("delta")
    observed = comparison.get("observed")
    baseline = comparison.get("baseline")

    print("CANDIDATE DECISION STUBS (print only; review and choose one before writing experiment_decision.json)")
    print(f"Comparison: {metric} observed {observed} vs baseline {baseline} ({direction}, delta={delta})")
    print("Higher/lower depends on whether the metric is desirable. Human must decide.")
    print()

    note = (
        f"Observed {metric} is {direction} than baseline ({observed} vs {baseline}, delta={delta}). "
        "Choose keep if the change improved the desired outcome, discard if it did not, or retest if uncertain. "
        "Do not invent."
    )

    # Short ready reason snippets so the human can start from grounded language
    reason_snippets = {
        "keep": f"The observed {metric} moved in a desirable direction ({direction}, delta={delta}). Keep the change for future packets unless a larger sample contradicts it.",
        "discard": f"The observed {metric} moved in an undesirable direction ({direction}, delta={delta}). Discard the change and revert or try a different intervention.",
        "retest": f"The observed {metric} change is small or ambiguous ({direction}, delta={delta}). Retest with a clearer metric, larger sample, or refined change before deciding.",
    }

    # Ready source snippet grounded in the comparison so the human can document the observation without inventing phrasing
    source_snippet = (
        f"Documented after observation window from experiment comparison of {metric} "
        f"(observed {observed} vs baseline {baseline}, {direction}, delta={delta}). "
        "Filled from Studio/Analytics export and full comment review."
    )

    for decision in ("keep", "discard", "retest"):
        snippet = reason_snippets.get(decision, "Review the full comparison and comments before deciding.")
        stub = {
            "_suggested_from_comparison": True,
            "_comment": "SUGGESTION ONLY. Copy the chosen stub to experiment_decision.json, replace reason and source with documented human review, then validate. Do not invent.",
            "decision": decision,
            "primary_metric": metric,
            "reason": f"PENDING: document why {decision} based on the {direction} result and full review",
            "source": "PENDING: replace with documented source from human review of analytics or Studio after the observation window",
            "notes": note,
            "_suggested_reason_snippet": snippet,
        }
        print(f"--- Candidate for {decision} ---")
        print(json.dumps(stub, indent=2))
        print(f"  suggested_reason_snippet: {snippet}")
        print(f"  ready source_snippet (copy/edit into the source field): {source_snippet}")
        print()

    print("Next human steps:")
    print("1. Review the full comparison with: python3 tools/experiment_loop.py", packet)
    print("2. Choose one stub above, copy to", packet / "experiment_decision.json")
    print("3. Fill real reason (use suggested_reason_snippet) and documented source (use ready source_snippet).")
    print("4. python3 tools/experiment_template_validator.py", packet / "experiment_decision.json")
    print("5. python3 tools/next_from_decision.py", packet / "experiment_decision.json")
    print("Do not invent decisions or results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
