#!/usr/bin/env python3
"""Unified local quality prep suite.

Runs the key no-write script quality scanners (quality_scan, claim_scan,
cadence_repetition_scan, mechanism_align_scan) with --strict and reports
a single overall PASS/FAIL based on their exit codes.

Hits under --strict become FAIL signals. Reduces sequential invocation
labor before promoting a script. Does not rewrite, invent, or write files.
Does not poll secrets.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

CHECKS = [
    ("quality_scan.py", ["--strict"]),
    ("claim_scan.py", ["--strict"]),
    ("cadence_repetition_scan.py", ["--strict"]),
    ("mechanism_align_scan.py", ["--strict"]),
]


def run_check(script: str, extra: list[str], packet: str) -> tuple[int, str]:
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), packet] + extra
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.strip()
    except Exception as e:
        return 1, f"EXCEPTION: {e}"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: quality_prep_suite.py PACKET", file=sys.stderr)
        return 1
    packet = sys.argv[1]
    path = Path(packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("QUALITY PREP SUITE (strict scanners; unified PASS/FAIL; no invent)")
    print(f"packet: {path.name}")
    print("Runs quality_scan --strict, claim_scan --strict, cadence_repetition_scan --strict, mechanism_align_scan --strict.")
    print("Overall FAIL if any scanner exits non-zero under --strict.")
    print("=" * 72)
    print()

    overall_fail = False
    for script, extra in CHECKS:
        print(f"## {script}")
        rc, output = run_check(script, extra, str(path))
        status = "PASS" if rc == 0 else "FAIL"
        print(f"status: {status} (exit {rc})")
        if output:
            print(output[:2000])  # truncate long output
        print()
        if rc != 0:
            overall_fail = True

    print("=" * 72)
    overall = "FAIL" if overall_fail else "PASS"
    print(f"overall: {overall}")
    print("Hits under --strict are revision signals. Revise script.md WORDS if FAIL, then re-run.")
    print("See docs/content_quality.md. Do not pad word count.")
    return 1 if overall_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
