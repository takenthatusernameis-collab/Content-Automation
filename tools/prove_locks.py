#!/usr/bin/env python3
"""One command after a GitHub write of high-risk tools.

Runs placeholder_guard.py, then words_contract.py, then
verify_write_path.py. Stops on the first non-zero exit.
Writes nothing. Does not import apply_script or set_status.

Why this file exists:
- After a GitHub write, agents must remember three unmapped
  commands. Missing one is how emptied siblings stay "live".
- This wrapper makes the advertised post-write order a single
  copy-paste without mapping needed.py.

This is not a substitute for the three files it runs.
Do not drop them because this exists.
Do not treat PASS as apply --write or Q1 scaffold.
Do not map this file in needed.py.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
STEPS = (
    "placeholder_guard.py",
    "words_contract.py",
    "verify_write_path.py",
)


def run_one(name: str) -> int:
    path = TOOLS / name
    print(f"--- {name} ---")
    if not path.is_file():
        print("PROVE LOCKS FAIL")
        print(f"  missing {name}")
        return 1
    proc = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(TOOLS.parent),
    )
    return int(proc.returncode)


def main() -> int:
    print("Prove locks: placeholder_guard then words_contract then verify_write_path")
    for name in STEPS:
        code = run_one(name)
        if code != 0:
            print("PROVE LOCKS FAIL")
            print(f"  {name} exited {code}")
            print("This command writes nothing.")
            return code if code != 0 else 1
    print("PROVE LOCKS PASS")
    print("All three steps exited 0. This command writes nothing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
