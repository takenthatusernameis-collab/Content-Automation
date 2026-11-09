#!/usr/bin/env python3
"""Contract for long_stall_report.py.

Verifies the report surfaces key phrases (HIGH, 1000+, human step, published 0) on the live repo.
Soft only.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "long_stall_report.py"


def main() -> int:
    result = subprocess.run(
        [sys.executable, str(TOOL)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    out = result.stdout + result.stderr
    required = [
        "HIGH",
        "1000+",
        "Videos published: 0",
        "human_starter.py",
        "LONG STALL REPORT HIGH",
    ]
    missing = [p for p in required if p not in out]
    if result.returncode != 0 or missing:
        print("CONTRACT FAIL")
        print(f"exit: {result.returncode}")
        print(f"missing: {missing}")
        return 1
    print("CONTRACT PASS: long_stall_report surfaces key stall phrases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
