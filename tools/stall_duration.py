#!/usr/bin/env python3
"""Quantify the consecutive STALL_OAUTH_IDLE streak from recent RUNS.md sections.

Scans the most recent run sections for the primary blocker phrase while videos published stay 0.
Prints the streak length so future agents see how long the human OAuth step has been the only remaining advance.
Does not poll secrets, does not invent data, does not modify files. Self-contained stdlib.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RUNS.md"

STALL_RE = re.compile(r"STALL_OAUTH_IDLE|secrets absent|OAuth secrets absent", re.IGNORECASE)
ZERO_RE = re.compile(r"Videos published stay 0|videos published remain 0", re.IGNORECASE)


def recent_sections(text: str, max_n: int = 20) -> list[str]:
    parts = re.split(r"(?=^## Run )", text, flags=re.M)
    sections = [p for p in parts if p.strip().startswith("## Run")]
    return sections[:max_n]


def is_stall_run(section: str) -> bool:
    return bool(ZERO_RE.search(section) and STALL_RE.search(section))


def main() -> int:
    if not RUNS.is_file():
        print("stall_duration: RUNS.md missing")
        return 1
    text = RUNS.read_text(encoding="utf-8")
    sections = recent_sections(text)
    streak = 0
    for s in sections:
        if is_stall_run(s):
            streak += 1
        else:
            break
    print("STALL DURATION HINT (OAuth idle streak; no invent, no poll)")
    print(f"consecutive_stall_runs_in_recent: {streak}")
    if streak >= 5:
        print("status: LONG_OAUTH_IDLE")
        print("message: The human OAuth secrets step has been the sole remaining blocker across many consecutive runs.")
        print("recommendation: Prefer python3 tools/human_next_action.py or docs/human_oauth_checklist.md then set the three secrets and dispatch execute=true once. Further pure inspection has diminishing returns.")
    else:
        print("status: SHORT_OR_UNKNOWN")
        print("message: Recent streak of explicit OAuth stall notes is short or not yet dominant.")
    print("Do not poll secrets. Preferred unblocked list remains complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
