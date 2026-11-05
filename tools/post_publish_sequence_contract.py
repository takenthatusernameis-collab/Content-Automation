#!/usr/bin/env python3
"""Contract for post_publish_sequence.py HOLD path (no provider_video_id).

Asserts key phrases so the fail-closed reminder does not silently regress.
Does not require a video id, poll secrets, or write production files.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "post_publish_sequence.py"

REQUIRED = [
    "POST PUBLISH SEQUENCE",
    "NO provider_video_id yet",
    "Videos published stay 0",
    "human OAuth step",
    "POST PUBLISH SEQUENCE HOLD (no id)",
]


def main() -> int:
    if not TOOL.is_file():
        print("CONTRACT FAIL: post_publish_sequence.py missing")
        return 1
    proc = subprocess.run(
        [sys.executable, str(TOOL)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    out = proc.stdout + proc.stderr
    missing = [p for p in REQUIRED if p not in out]
    if missing or proc.returncode != 0:
        print("CONTRACT FAIL")
        for m in missing:
            print(f"  missing: {m}")
        if proc.returncode != 0:
            print(f"  exit {proc.returncode}")
        return 1
    print("POST PUBLISH SEQUENCE CONTRACT PASS (HOLD path locked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
