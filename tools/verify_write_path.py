#!/usr/bin/env python3
"""One command after reconstructing the write-path tools.

Runs tools/contract_shape.py, then tools/write_path_contract.py.
Stops on the first non-zero exit. Writes nothing. Does not import
apply_script, set_status, or write_path_contract.

Why this file exists:
- Run 068/069 require shape then contract as two commands.
- A reconstructed tree can still run write_path_contract.py alone
  and print PASS while contract_shape.py was never fetched.
- This wrapper makes the advertised order a single copy-paste.

This is not a substitute for the two files it runs. Do not drop
contract_shape.py or write_path_contract.py because this exists.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
STEPS = ("contract_shape.py", "write_path_contract.py")


def run_one(name: str) -> int:
    path = TOOLS / name
    print(f"--- {name} ---")
    if not path.is_file():
        print("VERIFY WRITE PATH FAIL")
        print(f"  missing {name}")
        return 1
    proc = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(TOOLS.parent),
    )
    return int(proc.returncode)


def main() -> int:
    print("Verify write path: contract_shape.py then write_path_contract.py")
    for name in STEPS:
        code = run_one(name)
        if code != 0:
            print("VERIFY WRITE PATH FAIL")
            print(f"  {name} exited {code}")
            print("This command writes nothing.")
            return code if code != 0 else 1
    print("VERIFY WRITE PATH PASS")
    print("Both steps exited 0. This command writes nothing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
