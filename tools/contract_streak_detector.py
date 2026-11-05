#!/usr/bin/env python3
"""Detect consecutive runs that only added reliability contracts.

Flags a long streak of *contract.py additions while videos published remain 0
and STALL_OAUTH_IDLE continues. This makes the saturating pattern machine-visible
so future runs prefer the human OAuth step or a true new production capability
over further contract locks.
Soft only; does not invent data, poll secrets, or write files.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RUNS.md"
THRESHOLD = 5  # consecutive contract-addition runs before high suspicion

CONTRACT_RE = re.compile(r"added tools/\S+_contract\.py", re.I)
ZERO_RE = re.compile(r"Videos published stay 0|published stay 0", re.I)


def count_contract_streak(text: str) -> int:
    """Count consecutive recent run sections that added a contract."""
    sections = re.split(r"^## Run ", text, flags=re.M)
    streak = 0
    for sec in sections[1:]:
        if CONTRACT_RE.search(sec) and ZERO_RE.search(sec):
            streak += 1
        else:
            break
    return streak


def main() -> int:
    if not RUNS.is_file():
        print("contract_streak_detector: RUNS.md missing")
        return 1
    text = RUNS.read_text(encoding="utf-8")
    streak = count_contract_streak(text)
    print("CONTRACT STREAK DETECTOR (anti-saturation of reliability locks; no invent)")
    print(f"consecutive_contract_addition_runs: {streak}")
    if streak >= THRESHOLD:
        print("FLAG: CONTRACT_STREAK_SATURATING")
        print("Recent runs have successively added *contract.py locks while published remains 0.")
        print("Recommendation: prioritize the human OAuth step (python3 tools/human_starter.py).")
        print("Further pure contract locks have diminishing returns until after first publish.")
        print("Prefer a true new capability that advances media/QA/assembly or post-publish readiness.")
    else:
        print("FLAG: NORMAL")
        print("Contract streak below threshold; reliability locks remain useful.")
    print(f"Threshold: {THRESHOLD}. Full history in RUNS.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
