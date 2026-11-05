#!/usr/bin/env python3
"""Reliability contract for tools/assemble.py.

Creates a temporary empty packet and asserts the fail-closed missing-media
path (exit 2 + key phrases including gate: HOLD_MEDIA).
Soft only; does not invent media, run ffmpeg, or bump status. Locks the
pre-upload assembly planner so the HOLD_MEDIA refuse cannot silently regress
while the long OAuth stall continues.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "assemble.py"

REQUIRED = [
    "gate: HOLD_MEDIA",
    "ready_to_assemble: no",
    "assemble never invents media, never bumps status, and default mode never runs ffmpeg",
    "repo-root vo/ is not Selected VO",
]


def main() -> int:
    if not TOOL.is_file():
        print("CONTRACT FAIL: assemble.py missing")
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
        if missing or proc.returncode != 2:
            print("ASSEMBLE CONTRACT FAIL")
            for m in missing:
                print(f"  missing: {m}")
            print(f"  exit {proc.returncode} (expected 2)")
            return 1
    print("ASSEMBLE CONTRACT PASS (HOLD_MEDIA path locked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
