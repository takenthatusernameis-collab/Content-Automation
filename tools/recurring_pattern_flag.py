#!/usr/bin/env python3
"""Flag highly recurring stall patterns from RUNS.md for agent awareness.

Counts consecutive recent runs with videos_published=0 and OAuth idle.
If the streak exceeds a threshold, flags HIGHLY_SUSPICIOUS_STALL so future
runs treat pure anti-rediscovery restatements as lower priority and prefer
the human OAuth step or a capability that only becomes useful after publish.
Does not invent data, poll secrets, or write files.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RUNS.md"
THRESHOLD = 10  # consecutive zero-publish runs before high suspicion

ZERO_RE = re.compile(r"Videos published stay 0|videos_published: 0|published remain 0", re.I)
OAUTH_RE = re.compile(r"STALL_OAUTH_IDLE|secrets absent|OAuth.*absent", re.I)


def count_recent_zero_streak(text: str) -> int:
    """Count consecutive recent run sections that show zero published + OAuth stall."""
    sections = re.split(r"^## Run ", text, flags=re.M)
    streak = 0
    for sec in sections[1:]:
        if ZERO_RE.search(sec) and OAUTH_RE.search(sec):
            streak += 1
        else:
            break
    return streak


def main() -> int:
    if not RUNS.is_file():
        print("recurring_pattern_flag: RUNS.md missing")
        return 1
    text = RUNS.read_text(encoding="utf-8")
    streak = count_recent_zero_streak(text)
    print("RECURRING PATTERN FLAG (anti-rediscovery of stall saturation; no invent)")
    print(f"consecutive_zero_publish_oauth_runs: {streak}")
    if streak >= THRESHOLD:
        print("FLAG: HIGHLY_SUSPICIOUS_STALL")
        print("The zero-publish OAuth-idle pattern has repeated across many runs.")
        print("Recommendation: prioritize the human OAuth secret setup + one private dispatch.")
        print("Further pure anti-rediscovery one-liner tools have diminishing returns until after publish.")
        print("See python3 tools/human_next_action.py or python3 tools/next_suggestion.py.")
    else:
        print("FLAG: NORMAL")
        print("Streak below threshold; continue normal unblocked improvements.")
    print(f"Threshold: {THRESHOLD}. Full history in RUNS.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
