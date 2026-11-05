#!/usr/bin/env python3
"""Reliability contract for tools/complete.py.

Creates a temporary empty packet and asserts the fail-closed incomplete
path (exit 2 + key phrases including gate: INCOMPLETE_MEDIA, action: HOLD_MEDIA).
Soft only; does not invent media, metrics, video IDs, or experiment results.
Locks the completion gate so markdown-only packets cannot be claimed COMPLETE
while the long OAuth stall continues.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "complete.py"

REQUIRED = [
    "gate: INCOMPLETE_MEDIA",
    "action: HOLD_MEDIA",
    "complete.py never invents media, uploads, metrics, or experiment results",
    "markdown-only packets stay INCOMPLETE_*",
    "selected_vo_present",
]


def main() -> int:
    if not TOOL.is_file():
        print("CONTRACT FAIL: complete.py missing")
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
            print("COMPLETE CONTRACT FAIL")
            for m in missing:
                print(f"  missing: {m}")
            print(f"  exit {proc.returncode} (expected 2)")
            return 1
    print("COMPLETE CONTRACT PASS (INCOMPLETE_MEDIA path locked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
