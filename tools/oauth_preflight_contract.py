#!/usr/bin/env python3
"""Reliability contract for tools/oauth_preflight.py.

Runs the preflight with OAuth env vars deliberately unset and asserts the
fail-closed missing-secrets path (exit 3 + key phrases). Soft only; no real
secrets are ever set or printed. Locks the authenticated-dispatch guard so it
cannot silently regress while the long OAuth stall continues.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "oauth_preflight.py"

REQUIRED = [
    "YOUTUBE_CLIENT_ID=missing",
    "YOUTUBE_CLIENT_SECRET=missing",
    "YOUTUBE_REFRESH_TOKEN=missing",
    "REFUSE: authenticated dispatch needs GitHub Actions secrets",
]


def main() -> int:
    if not TOOL.is_file():
        print("CONTRACT FAIL: oauth_preflight.py missing")
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
        print("OAUTH PREFLIGHT CONTRACT FAIL")
        for m in missing:
            print(f"  missing: {m}")
        print(f"  exit {proc.returncode} (expected 3)")
        return 1
    print("OAUTH PREFLIGHT CONTRACT PASS (missing-secrets path locked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
