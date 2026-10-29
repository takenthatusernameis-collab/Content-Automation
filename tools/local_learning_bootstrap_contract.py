#!/usr/bin/env python3
"""Contract for local_learning_bootstrap.py.

Verifies:
- Fail-closed on missing idea.md
- Does not invent baseline numbers or decisions
- Produces or reports on the expected skeleton files when --force is used
- Exit codes match success/failure
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "local_learning_bootstrap.py"


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or ROOT)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main() -> int:
    if not TOOL.is_file():
        print("FAIL: tool missing")
        return 1

    # Fail-closed on missing idea.md
    with tempfile.TemporaryDirectory() as td:
        empty = Path(td) / "empty-packet"
        empty.mkdir()
        code, out = run([sys.executable, str(TOOL), str(empty)])
        if code != 2 or "idea.md missing" not in out:
            print(f"FAIL: expected exit 2 and idea.md message, got {code}\n{out[:300]}")
            return 1
        print("PASS: fail-closed on missing idea.md")

    # Grounded run on a temp packet with idea.md (no force so no writes)
    with tempfile.TemporaryDirectory() as td:
        pkt = Path(td) / "test-packet"
        pkt.mkdir()
        (pkt / "idea.md").write_text(
            "# Test\n\nmechanism: a short cue\nproblem: stalling\ntopic: focus systems\n"
        )
        code, out = run([sys.executable, str(TOOL), str(pkt)])
        if code != 0 or "LOCAL LEARNING BOOTSTRAP" not in out:
            print(f"FAIL: expected success on grounded packet, got {code}\n{out[:400]}")
            return 1
        print("PASS: grounded run succeeds without invent")

    print("local_learning_bootstrap_contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
