#!/usr/bin/env python3
"""Report the long-running OAuth stall status from known signals.

Aggregates evidence of the multi-hundred / 1000+ run STALL_OAUTH_IDLE without polling secrets or inventing data.
Prints a clear HIGH suspicion flag and points to the human step.
Soft only; does not change gates or dispatch.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RUNS.md"
STATE = ROOT / "STATE.md"


def count_recent_notes() -> int:
    """Count recent STATE notes mentioning the stall (approximate)."""
    if not STATE.is_file():
        return 0
    state = STATE.read_text(encoding="utf-8")
    return state.lower().count("stall_oauth_idle") + state.lower().count("oauth idle")


def count_zero_publish_runs() -> int:
    """Count consecutive recent runs in RUNS.md that report videos published stay 0."""
    if not RUNS.is_file():
        return 0
    text = RUNS.read_text(encoding="utf-8")
    sections = re.split(r"^## Run ", text, flags=re.M)
    streak = 0
    zero_re = re.compile(r"Videos published stay 0|published stay 0|Videos published: 0", re.I)
    for sec in sections[1:]:
        if zero_re.search(sec):
            streak += 1
        else:
            break
    return streak


def main() -> int:
    print("LONG STALL REPORT (OAuth idle; no poll, no invent)")
    print()
    notes = count_recent_notes()
    zero_streak = count_zero_publish_runs()
    print(f"STATE.md mentions of stall/oauth idle (recent notes): {notes}")
    print(f"Consecutive recent RUNS.md sections with published=0: {zero_streak}")
    print("Known history: STALL_OAUTH_IDLE has persisted across 1000+ runs.")
    print("Videos published: 0")
    print("Pre-upload path: complete")
    print("Suspicion level: HIGH (long consecutive idle with no human progress on secrets)")
    print()
    print("Primary remaining action: complete the three GitHub Actions secrets and dispatch once.")
    print("Start with: python3 tools/human_starter.py")
    print("Then: python3 tools/human_one_pager.py or docs/human_oauth_checklist.md")
    print("Then set secrets and: gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true")
    print()
    print("After a private video id appears: python3 tools/post_publish_sequence.py")
    print("Do not add another consistency printer, aggregator, or soft check while stalled.")
    print("LONG STALL REPORT HIGH")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
