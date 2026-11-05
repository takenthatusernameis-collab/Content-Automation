#!/usr/bin/env python3
"""Reliability contract for tools/youtube_upload.py.

Creates a temporary empty packet and asserts the fail-closed missing-local-media
and missing-OAuth path (exit 2 + key phrases including gate: FAIL, action: HOLD_LOCAL,
auth: YOUTUBE_AUTH_REQUIRED).
Soft only; does not invent media, call YouTube, or write state. Locks the
pre-upload uploader so the HOLD_LOCAL / AUTH refuse cannot silently regress
while the long OAuth stall continues.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "youtube_upload.py"

REQUIRED = [
    "gate: FAIL",
    "action: HOLD_LOCAL",
    "auth: YOUTUBE_AUTH_REQUIRED",
    "oauth_complete",
    "dry-run default; --execute performs authenticated API calls only after all local gates pass",
    "an API key alone is not upload authorization",
]


def main() -> int:
    if not TOOL.is_file():
        print("CONTRACT FAIL: youtube_upload.py missing")
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
            print("YOUTUBE_UPLOAD CONTRACT FAIL")
            for m in missing:
                print(f"  missing: {m}")
            print(f"  exit {proc.returncode} (expected 2)")
            return 1
    print("YOUTUBE_UPLOAD CONTRACT PASS (HOLD_LOCAL + AUTH path locked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
