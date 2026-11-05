#!/usr/bin/env python3
"""Reliability contract for tools/oauth_setup.py.

Runs the setup recipe printer with OAuth env vars deliberately unset and asserts
the fail-closed missing-secrets path (exit 3 + key phrases including MISSING and
core recipe text). Soft only; no real secrets are ever set or printed. Locks the
human OAuth setup guidance so it cannot silently regress while the long OAuth
stall continues.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "oauth_setup.py"

REQUIRED = [
    "YouTube OAuth setup recipe (no secret values)",
    "MISSING YOUTUBE_CLIENT_ID,YOUTUBE_CLIENT_SECRET,YOUTUBE_REFRESH_TOKEN",
    "gh secret set YOUTUBE_CLIENT_ID",
    "python3 tools/oauth_exchange.py",
    "Do not dispatch either input while any secret is empty",
]


def main() -> int:
    if not TOOL.is_file():
        print("CONTRACT FAIL: oauth_setup.py missing")
        return 1

    # Clean environment: strip any OAuth keys so the missing path is exercised.
    env = os.environ.copy()
    for key in ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"):
        env.pop(key, None)

    proc = subprocess.run(
        [sys.executable, str(TOOL)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    out = proc.stdout + proc.stderr
    missing = [p for p in REQUIRED if p not in out]
    if missing or proc.returncode != 3:
        print("OAUTH SETUP CONTRACT FAIL")
        for m in missing:
            print(f"  missing: {m}")
        print(f"  exit {proc.returncode} (expected 3)")
        return 1
    print("OAUTH SETUP CONTRACT PASS (missing-secrets path and recipe locked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
