#!/usr/bin/env python3
"""Concise efficiency summary from recent PROGRESS.md notes.

Extracts measurable or reusable gains so agents see compounding progress
without opening the full file. No invent; read-only.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRESS = ROOT / "PROGRESS.md"


def main() -> int:
    if not PROGRESS.is_file():
        print("efficiency_summary: PROGRESS.md missing")
        return 1
    text = PROGRESS.read_text(encoding="utf-8")
    lines = text.splitlines()
    gains = []
    for line in lines[:80]:  # recent section only
        stripped = line.strip()
        if stripped.startswith(("- Reusable capability:", "- Human labor reduction:", "Reusable capability:", "Added reusable")):
            gains.append(stripped.lstrip("- ").strip())
        if len(gains) >= 5:
            break
    print("EFFICIENCY SUMMARY (recent from PROGRESS.md; no invent)")
    if not gains:
        print("no recent measurable gains found in first 80 lines")
    else:
        for i, g in enumerate(gains, 1):
            print(f"  {i}. {g[:200]}")
    print("Full notes in PROGRESS.md and docs/progress_archive.md.")
    print("Videos published remain 0; stall continues until human OAuth secrets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
