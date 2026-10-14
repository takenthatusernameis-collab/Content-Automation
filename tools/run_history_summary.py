#!/usr/bin/env python3
"""Print a concise summary of the last N runs from RUNS.md.

Reduces rediscovery of recent agent actions, objectives, and results without opening the full history file.
Does not poll secrets, dispatch, or modify files.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RUNS.md"


def extract_last_runs(text: str, n: int = 3) -> list[str]:
    sections = []
    current = []
    in_section = False
    for line in text.splitlines():
        if line.startswith("## Run "):
            if current and in_section:
                sections.append("\n".join(current).strip())
            current = [line]
            in_section = True
        elif in_section:
            current.append(line)
            if line.startswith("## ") and not line.startswith("## Run "):
                sections.append("\n".join(current[:-1]).strip())
                current = []
                in_section = False
    if current and in_section:
        sections.append("\n".join(current).strip())
    return sections[:n]


def main() -> int:
    n = 3
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            pass
    if not RUNS.is_file():
        print("RUNS.md missing")
        return 1
    text = RUNS.read_text(encoding="utf-8")
    sections = extract_last_runs(text, n)
    if not sections:
        print("No run sections found")
        return 0
    print(f"LAST {len(sections)} RUNS SUMMARY (from RUNS.md; do not invent)")
    for sec in sections:
        lines = sec.splitlines()
        header = lines[0] if lines else ""
        print(header)
        for line in lines[1:6]:
            if line.strip().startswith("- "):
                print(line)
            if len([l for l in lines if l.startswith("- ")]) > 4:
                break
        print()
    print("Full history in RUNS.md and docs/runs_archive.md. Prefer new reusable capability over restatement if pattern repeats with no progress.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
