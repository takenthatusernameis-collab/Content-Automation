#!/usr/bin/env python3
"""Contract for script_promotion_steps.py: grounded printer, no invent, no write."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "script_promotion_steps.py"


def main() -> int:
    if not TOOL.is_file():
        print("FAIL: script_promotion_steps.py missing")
        return 1
    # Run on default Q1 packet (exists) and a missing path
    r = subprocess.run([sys.executable, str(TOOL)], capture_output=True, text=True)
    out = r.stdout + r.stderr
    if r.returncode != 0:
        print(f"FAIL: exit {r.returncode} on default packet")
        print(out)
        return 1
    required = [
        "SCRIPT PROMOTION STEPS",
        "quality_prep_brief.py",
        "claim_source_table.py",
        "apply_script.py",
        "no invent",
        "Preferred current action remains human OAuth",
    ]
    missing = [s for s in required if s not in out]
    if missing:
        print(f"FAIL: missing phrases: {missing}")
        return 1
    # Missing packet must fail closed
    r2 = subprocess.run(
        [sys.executable, str(TOOL), "/tmp/nonexistent-packet-xyz"],
        capture_output=True,
        text=True,
    )
    if r2.returncode == 0:
        print("FAIL: should exit non-zero on missing packet")
        return 1
    if "packet dir missing" not in (r2.stdout + r2.stderr):
        print("FAIL: missing-packet message absent")
        return 1
    print("script_promotion_steps_contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
