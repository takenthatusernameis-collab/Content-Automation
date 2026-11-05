#!/usr/bin/env python3
"""Reliability contract for tools/media_qa.py.

Creates a temporary empty packet and asserts the fail-closed missing-Selected-VO
path (exit 2 + key phrases including gate: FAIL and selected_vo_present).
Soft only; does not invent media, run ffmpeg, or bump status. Locks the
pre-upload media QA gate so it cannot silently regress while the long OAuth
stall continues.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "media_qa.py"

REQUIRED = [
    "gate: FAIL",
    "selected_vo_present",
    "repo-root vo/ is not Selected VO",
    "media_qa never runs ffmpeg and never bumps status",
]


def main() -> int:
    if not TOOL.is_file():
        print("CONTRACT FAIL: media_qa.py missing")
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
            print("MEDIA QA CONTRACT FAIL")
            for m in missing:
                print(f"  missing: {m}")
            print(f"  exit {proc.returncode} (expected 2)")
            return 1
    print("MEDIA QA CONTRACT PASS (missing-Selected-VO path locked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
