#!/usr/bin/env python3
"""Reliability contract for human_preflight.py.

Runs the preflight and asserts key phrases surface. Soft only.
Does not require external tools to pass; checks the printer itself.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "human_preflight.py"


def main() -> int:
    if not SCRIPT.is_file():
        print("CONTRACT FAIL: human_preflight.py missing")
        return 1
    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except Exception as exc:
        print(f"CONTRACT FAIL: could not run script ({exc})")
        return 1

    out = result.stdout + result.stderr
    required = [
        "HUMAN PREFLIGHT",
        "python3",
        "gh CLI",
        "HUMAN PREFLIGHT PASS" if result.returncode == 0 else "HUMAN PREFLIGHT FAIL",
    ]
    missing = [p for p in required if p not in out]
    if missing:
        print(f"CONTRACT FAIL: missing phrases {missing}")
        print("--- output ---")
        print(out[:2000])
        return 1

    print("CONTRACT PASS: human_preflight surfaces expected phrases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
