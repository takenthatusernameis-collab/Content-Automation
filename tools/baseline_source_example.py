#!/usr/bin/env python3
"""Print example documented source strings for experiment baselines.

Provides ready-to-adapt phrasing that will pass experiment_loop.py's source check
(not containing invented/assumed/placeholder/guess). Grounded in YouTube Studio
analytics access patterns. Does not invent numeric baselines, video ids, dates,
or results. Does not write files, poll secrets, or call APIs.
Reusable to reduce the labor of phrasing a valid source field across future experiments.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

# Example source patterns that satisfy the documented-observation requirement.
# Human must replace the placeholders with real video title/id and retrieval date.
EXAMPLES = [
    "YouTube Studio analytics for the prior video titled '<exact title>' retrieved on YYYY-MM-DD",
    "YouTube Studio video analytics page for video id <PROVIDER_VIDEO_ID> exported on YYYY-MM-DD",
    "YouTube Analytics report for average view duration on video '<title>' as of YYYY-MM-DD",
    "Manual note from YouTube Studio Advanced Mode for metric <primary_metric> on <video> dated YYYY-MM-DD",
]

def main() -> int:
    print("BASELINE SOURCE EXAMPLE (valid phrasing only; no invented numbers or dates)")
    print()
    print("These patterns avoid rejected words (invented/assumed/placeholder/guess).")
    print("Replace the angle-bracket or YYYY-MM-DD parts with real documented values after you have them.")
    print("experiment_loop.py requires a non-empty source that is a documented observation.")
    print()
    for i, ex in enumerate(EXAMPLES, 1):
        print(f"{i}. {ex}")
    print()
    print("After a real private provider_video_id exists and the observation window has passed:")
    print("  1. Collect feedback so metrics are real.")
    print("  2. Fill experiment_baseline.json with numeric baseline + one of the above source styles.")
    print("  3. python3 tools/experiment_template_validator.py <packet>/experiment_baseline.json")
    print()
    print("Do not invent a baseline value or a video id. Human OAuth remains the blocker for first publish.")
    print("BASELINE SOURCE EXAMPLE complete.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
