#!/usr/bin/env python3
"""Unified local metadata prep suite.

Runs the key no-write metadata scanners (title_scan, description_scan,
tags_scan, first_comment_scan, chapters_scan, thumbnail_scan, end_screen_scan)
with --strict and reports a single overall PASS/FAIL based on their exit codes.

Hits under --strict become FAIL signals. Reduces sequential invocation
labor before promoting titles, descriptions, tags, chapters, thumbnails,
or end-screens. Does not rewrite, invent, or write files.
Does not poll secrets.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

CHECKS = [
    ("title_scan.py", ["--strict"]),
    ("description_scan.py", ["--strict"]),
    ("tags_scan.py", ["--strict"]),
    ("first_comment_scan.py", ["--strict"]),
    ("chapters_scan.py", ["--strict"]),
    ("thumbnail_scan.py", ["--strict"]),
    ("end_screen_scan.py", ["--strict"]),
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
        print("Usage: metadata_prep_suite.py PACKET", file=sys.stderr)
        return 1
    packet = sys.argv[1]
    path = Path(packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("METADATA PREP SUITE (strict scanners; unified PASS/FAIL; no invent)")
    print(f"packet: {path.name}")
    print("Runs title_scan --strict, description_scan --strict, tags_scan --strict,")
    print("first_comment_scan --strict, chapters_scan --strict, thumbnail_scan --strict, end_screen_scan --strict.")
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
    print("Hits under --strict are revision signals. Revise the relevant metadata files if FAIL, then re-run.")
    print("See docs/content_quality.md and packet publish.md / titles.md / thumbnail.md / chapters.md.")
    return 1 if overall_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
