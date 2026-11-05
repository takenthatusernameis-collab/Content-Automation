#!/usr/bin/env python3
"""Reliability contract for tools/post_publish_sequence.py.

Runs the sequence printer on the default packet (no video id) and confirms
the pre-id HOLD path surfaces key phrases pointing back to the human step.
Soft only; does not invent a video id, poll secrets, dispatch, or modify files.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SEQUENCE = TOOLS / "post_publish_sequence.py"
DEFAULT_PACKET = Path(__file__).resolve().parents[1] / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def main() -> int:
    if not SEQUENCE.is_file():
        print("post_publish_sequence_contract FAIL: sequence tool missing", file=sys.stderr)
        return 1
    if not DEFAULT_PACKET.is_dir():
        print("post_publish_sequence_contract FAIL: default packet missing", file=sys.stderr)
        return 1
    result = subprocess.run(
        [sys.executable, str(SEQUENCE), str(DEFAULT_PACKET)],
        capture_output=True,
        text=True,
    )
    out = (result.stdout or "") + (result.stderr or "")
    required = [
        "NO provider_video_id yet",
        "human_one_pager.py",
        "POST PUBLISH SEQUENCE HOLD",
        "Videos published stay 0",
    ]
    missing = [r for r in required if r not in out]
    if result.returncode != 0 or missing:
        print("post_publish_sequence_contract FAIL", file=sys.stderr)
        if missing:
            print(f"missing phrases: {missing}", file=sys.stderr)
        print(out, file=sys.stderr)
        return 1
    print("post_publish_sequence_contract PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
