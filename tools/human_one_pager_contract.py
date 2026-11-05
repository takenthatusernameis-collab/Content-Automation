#!/usr/bin/env python3
"""Reliability contract for tools/human_one_pager.py.

Runs the one-pager on the default Q1 packet and confirms key human-step
phrases surface (stall flag, dispatch command, success criteria).
Soft only; does not poll secrets, dispatch, or modify files.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PAGER = TOOLS / "human_one_pager.py"
DEFAULT_PACKET = Path(__file__).resolve().parents[1] / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def main() -> int:
    if not PAGER.is_file():
        print("human_one_pager_contract FAIL: pager missing", file=sys.stderr)
        return 1
    if not DEFAULT_PACKET.is_dir():
        print("human_one_pager_contract FAIL: default packet missing", file=sys.stderr)
        return 1
    result = subprocess.run(
        [sys.executable, str(PAGER), str(DEFAULT_PACKET)],
        capture_output=True,
        text=True,
    )
    out = (result.stdout or "") + (result.stderr or "")
    required = [
        "STALL_OAUTH_IDLE",
        "LONG STALL SUSPICIOUS",
        "gh workflow dispatch",
        "execute=true",
        "provider_video_id",
        "Videos published moves from 0",
    ]
    missing = [r for r in required if r not in out]
    if result.returncode != 0 or missing:
        print("human_one_pager_contract FAIL", file=sys.stderr)
        if missing:
            print(f"missing phrases: {missing}", file=sys.stderr)
        print(out, file=sys.stderr)
        return 1
    print("human_one_pager_contract PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
