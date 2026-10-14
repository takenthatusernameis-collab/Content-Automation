#!/usr/bin/env python3
"""Clear stall escalation summary for the long zero-publish OAuth idle streak.

Prints a concise, non-rediscovery message when the consecutive zero-publish
run count is high. Points directly at the human step without inventing data,
polling secrets, or modifying files. Use when stall suspicion is HIGH.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RUNS.md"
THRESHOLD = 10  # consecutive zero-publish runs to flag as highly suspicious


def count_consecutive_zero_publish(text: str) -> int:
    """Count leading consecutive run sections that report videos published stay 0."""
    runs = re.findall(r"## Run \d+ — .*?(?=\n## Run |\Z)", text, re.S)
    streak = 0
    for r in runs:
        if re.search(r"Videos published stay 0|videos published stay 0|published remain 0", r, re.I):
            streak += 1
        else:
            break
    return streak


def main() -> int:
    if not RUNS.is_file():
        print("stall_escalation: RUNS.md missing")
        return 1
    text = RUNS.read_text(encoding="utf-8")
    streak = count_consecutive_zero_publish(text)
    print("STALL ESCALATION SUMMARY")
    print(f"consecutive_zero_publish_runs: {streak}")
    if streak >= THRESHOLD:
        print("status: HIGHLY_SUSPICIOUS_STALL")
        print("message: The OAuth secret stall has persisted across many runs with zero videos published.")
        print("only_advancing_action: Human must set the three GitHub Actions secrets and dispatch execute=true.")
        print("exact_human_commands:")
        print("  python3 tools/human_next_action.py")
        print("  # or follow docs/human_oauth_checklist.md then:")
        print("  gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation")
        print("  gh secret set YOUTUBE_CLIENT_SECRET --repo takenthatusernameis-collab/Content-Automation")
        print("  gh secret set YOUTUBE_REFRESH_TOKEN --repo takenthatusernameis-collab/Content-Automation")
        print("  gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false")
        print("Do not poll secrets. Do not add more one-liner tools solely to restate this. Prefer human step.")
    else:
        print("status: not_yet_highly_suspicious")
        print("message: Streak below threshold; continue normal anti-rediscovery or human step as appropriate.")
    print("Full details in RUNS.md / STATE.md. No invent, no poll, no dispatch from agent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
