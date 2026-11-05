#!/usr/bin/env python3
"""Reliability contract for tools/timeline.py.

Creates a temporary empty packet and asserts the fail-closed missing-script.md
path (exit 1 + key phrase "missing script.md").
Soft only; does not invent media, run ffmpeg, or bump status. Locks the
edit timeline planner so the missing-script refuse cannot silently regress
while the long OAuth stall continues.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "timeline.py"

REQUIRED = [
    "missing script.md",
]


def main() -> int:
    if not TOOL.is_file():
        print("CONTRACT FAIL: timeline.py missing")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "empty-packet"
        packet.mkdir()
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        out = proc.stdout + proc.stderr
        missing = [p for p in REQUIRED if p not in out]
        if missing or proc.returncode != 1:
            print("TIMELINE CONTRACT FAIL")
            for m in missing:
                print(f"  missing: {m}")
            print(f"  exit {proc.returncode} (expected 1)")
            print(f"  output:\n{out}")
            return 1
    print("TIMELINE CONTRACT PASS (missing-script.md path locked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
