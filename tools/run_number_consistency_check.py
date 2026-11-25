#!/usr/bin/env python3
"""Check consistency of the latest Run number across durable tracking files.

Addresses potential drift in run history (STATE.md, RUNS.md, PROGRESS.md, HANDOFF.md).
Extracts the highest Run NNNN from each and reports if they match.
Soft informational; exit 1 only on clear mismatch. Does not invent data or rewrite files.
Useful after any remote update. Compounds reliability of durable run memory.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    "STATE.md",
    "RUNS.md",
    "PROGRESS.md",
    "HANDOFF.md",
]

def extract_max_run(text: str) -> int | None:
    """Return the highest Run number found, or None."""
    matches = re.findall(r"Run\s+(\d+)", text)
    if not matches:
        return None
    return max(int(m) for m in matches)

def main() -> int:
    print("RUN NUMBER CONSISTENCY CHECK (latest Run ID across tracking files; do not invent)")
    runs = {}
    for name in FILES:
        path = ROOT / name
        if not path.is_file():
            print(f"MISSING {name}")
            runs[name] = None
            continue
        text = path.read_text(encoding="utf-8")
        max_run = extract_max_run(text)
        runs[name] = max_run
        print(f"{name}: max Run {max_run}")
    values = [v for v in runs.values() if v is not None]
    if not values:
        print("FAIL: no Run numbers found")
        return 1
    unique = set(values)
    if len(unique) == 1:
        print(f"PASS: all files agree on latest Run {unique.pop()}")
        return 0
    print(f"FAIL: mismatched latest Run numbers {sorted(unique)}")
    print("Update tracking files so the most recent Run is consistent. See FAILURES.md pattern.")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
