#!/usr/bin/env python3
"""Print example documented source strings for experiment decisions.

Provides ready-to-adapt phrasing that will pass experiment_loop.py's source check
(not containing invented/assumed/placeholder/guess). Grounded in YouTube Studio
or human review patterns after a real comparison. Does not invent decisions,
reasons, numeric results, video ids, or dates. Does not write files, poll secrets,
or call APIs. Reusable to reduce the labor of phrasing a valid source field
across future experiment decisions.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

# Example source patterns that satisfy the documented-review requirement.
# Human must replace the placeholders with real video title/id, metric, and review date.
EXAMPLES = [
    "Human review of YouTube Studio analytics for video '<exact title>' (id <PROVIDER_VIDEO_ID>) on YYYY-MM-DD after the observation window",
    "Documented comparison in YouTube Analytics Advanced Mode for primary metric <primary_metric> on <video> dated YYYY-MM-DD",
    "Manual notes from reviewing the experiment_loop.py comparison output plus Studio retention graph for video id <PROVIDER_VIDEO_ID> on YYYY-MM-DD",
    "YouTube Studio video analytics page reviewed for the keep/discard decision on '<title>' as of YYYY-MM-DD",
]

def main() -> int:
    print("DECISION SOURCE EXAMPLE (valid phrasing only; no invented decisions or results)")
    print()
    print("These patterns avoid rejected words (invented/assumed/placeholder/guess).")
    print("Replace the angle-bracket or YYYY-MM-DD parts with real documented values after you have them.")
    print("experiment_loop.py requires a non-empty source that is a documented review, not invented.")
    print()
    for i, ex in enumerate(EXAMPLES, 1):
        print(f"{i}. {ex}")
    print()
    print("After a real private provider_video_id, observation window, baseline, and numeric comparison exist:")
    print("  1. python3 tools/feedback_to_decision_suggest.py <packet>  # see candidate stubs")
    print("  2. Choose keep/discard/retest and fill experiment_decision.json with real reason + one of the above source styles.")
    print("  3. python3 tools/experiment_template_validator.py <packet>/experiment_decision.json")
    print("  4. python3 tools/next_from_decision.py <packet>/experiment_decision.json")
    print()
    print("Do not invent a decision, reason, or video id. Human OAuth remains the blocker for first publish.")
    print("DECISION SOURCE EXAMPLE complete.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
