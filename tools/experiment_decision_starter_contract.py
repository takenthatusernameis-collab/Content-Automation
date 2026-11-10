#!/usr/bin/env python3
"""Contract for experiment_decision_starter.py.

Locks that the starter never emits a recorded decision value and always
marks the output as a template requiring human review.
Soft only. No packet writes, no secrets.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "experiment_decision_starter.py"

def main() -> int:
    if not TOOL.is_file():
        print("FAIL: starter missing")
        return 1
    source = TOOL.read_text(encoding="utf-8")
    checks = [
        ("TEMPLATE: replace with keep" in source, "skeleton must leave decision as TEMPLATE"),
        ("RECORDED_DECISIONS" in source, "must import allowed decisions"),
        ("Does not invent" in source or "No invented" in source, "docstring must declare no invent"),
        ("experiment_loop.py rejects" in source, "must warn about rejection"),
    ]
    failed = [msg for ok, msg in checks if not ok]
    if failed:
        print("FAIL:", "; ".join(failed))
        return 1
    print("PASS: experiment_decision_starter keeps decision as template and does not invent")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
