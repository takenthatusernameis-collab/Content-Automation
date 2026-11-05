#!/usr/bin/env python3
"""One-command starter for the remaining human OAuth step.

Sequences human_preflight.py, long_stall_report.py, contract_streak_detector.py,
and human_one_pager.py so the human has a single entry point instead of remembering four commands.
Does not poll secrets, invent values, dispatch, or write files.
Soft only; does not change gates.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str) -> int:
    cmd = [sys.executable, str(ROOT / "tools" / script)]
    print(f"\n=== Running {script} ===\n")
    proc = subprocess.run(cmd, cwd=ROOT)
    return proc.returncode


def main() -> int:
    print("HUMAN STARTER (single entry for OAuth step; no secrets polled)")
    print("Sequences preflight + long stall report + contract streak detector + one-pager.")
    print()

    codes = []
    for script in ["human_preflight.py", "long_stall_report.py", "contract_streak_detector.py", "human_one_pager.py"]:
        code = run_tool(script)
        codes.append(code)
        if code != 0:
            print(f"\nHUMAN STARTER FAIL: {script} exited {code}")
            return code

    print("\nHUMAN STARTER PASS: environment ready, stall HIGH, contract streak checked, one-pager shown.")
    print("Next: follow the exact sequence printed above (oauth_exchange then gh secret set then one dispatch).")
    print("Full checklist: docs/human_oauth_checklist.md")
    print("Do not poll secrets from an agent. Do not add another consistency printer or contract lock.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
