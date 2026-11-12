#!/usr/bin/env python3
"""Print complete ready-to-adapt example JSON for experiment_baseline.json and experiment_decision.json.

Shows full structures with valid source phrasing (avoids rejected words) and clear placeholders.
Does not invent numeric values, decisions, video ids, or dates. Does not write files,
poll secrets, or call APIs. Reduces sequential lookup of separate source-example tools
and starter skeletons when preparing the experiment loop after a real comparison.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

# Valid source examples (same style as baseline_source_example / decision_source_example)
BASELINE_SOURCE = (
    "YouTube Studio analytics for the prior video titled '<exact title>' retrieved on YYYY-MM-DD"
)
DECISION_SOURCE = (
    "Human review of YouTube Studio analytics for video '<exact title>' (id <PROVIDER_VIDEO_ID>) "
    "on YYYY-MM-DD after the observation window"
)

def example_baseline() -> dict:
    return {
        "_example": "ready-to-adapt; replace angle-brackets and YYYY-MM-DD with real values; set numeric baseline",
        "hypothesis": "A hook that names the exact stall '<mechanism excerpt>' in the first 15 seconds will raise average view duration on the first 30 seconds",
        "change": "hook",
        "primary_metric": "average_view_duration_seconds",
        "baseline": None,  # MUST replace with real number from documented source
        "source": BASELINE_SOURCE,
        "notes": "change must be one of the allowed single variables; baseline must be numeric before use"
    }

def example_decision() -> dict:
    return {
        "_example": "ready-to-adapt; replace placeholders; choose keep/discard/retest only after real numeric comparison",
        "decision": "keep",  # or discard / retest; do not invent
        "reason": "Average view duration improved relative to the documented baseline after the observation window",
        "source": DECISION_SOURCE,
        "primary_metric": "average_view_duration_seconds",
        "notes": "source must be a documented review; do not use invented/assumed/placeholder/guess"
    }

def main() -> int:
    print("EXPERIMENT JSON EXAMPLES (soft; no invented numbers, decisions, or ids)")
    print()
    print("These structures use source phrasing that passes experiment_loop.py's rejected-words check.")
    print("Copy, replace all angle-bracket and YYYY-MM-DD placeholders with real documented values,")
    print("and set a real numeric baseline before writing to a packet.")
    print()
    print("--- experiment_baseline.json example ---")
    print(json.dumps(example_baseline(), indent=2))
    print()
    print("--- experiment_decision.json example ---")
    print(json.dumps(example_decision(), indent=2))
    print()
    print("Next steps after you have real metrics and a comparison:")
    print("  1. Adapt the baseline example, set numeric baseline, write to packet/experiment_baseline.json")
    print("  2. python3 tools/experiment_template_validator.py <packet>/experiment_baseline.json")
    print("  3. After comparison, adapt the decision example and validate similarly")
    print("  4. python3 tools/next_from_decision.py <packet>")
    print()
    print("See also: tools/baseline_source_example.py and tools/decision_source_example.py for more phrasing options.")
    print("Do not invent baselines or decisions. Human OAuth remains the blocker for first publish.")
    print("EXPERIMENT JSON EXAMPLES complete.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
