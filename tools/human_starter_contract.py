#!/usr/bin/env python3
"""Reliability contract for tools/human_starter.py.

Runs the starter and asserts key phrases surface so the single entry point
stays non-breaking across stalled runs. Soft only; no secrets, no dispatch.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    cmd = [sys.executable, str(ROOT / "tools" / "human_starter.py")]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    print(out)

    required = [
        "HUMAN STARTER",
        "HUMAN PREFLIGHT",
        "LONG STALL REPORT",
        "HUMAN ONE-PAGER",
        "HUMAN STARTER PASS",
        "docs/human_oauth_checklist.md",
    ]
    missing = [phrase for phrase in required if phrase not in out]
    if missing or proc.returncode != 0:
        print(f"HUMAN STARTER CONTRACT FAIL missing={missing} code={proc.returncode}")
        return 1
    print("HUMAN STARTER CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
