#!/usr/bin/env python3
"""Lock quality_scan: it reports hits and does not write script.md."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "quality_scan.py"


def fail(msg: str) -> int:
    print("QUALITY SCAN CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("quality_scan.py missing")
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "packet"
        packet.mkdir()
        script = packet / "script.md"
        script.write_text(
            "# Script\n\n## Hook\nWORDS:\n"
            "In today's fast-paced world you will learn to unlock your potential.\n\n"
            "VISUAL:\n*card*\n",
            encoding="utf-8",
        )
        before = script.read_text(encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet), "--strict"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        after = script.read_text(encoding="utf-8")
        if after != before:
            return fail("scanner wrote script.md")
        if proc.returncode != 1:
            return fail(f"strict slop must exit 1, got {proc.returncode}: {proc.stdout}")
        if "unlock your potential" not in proc.stdout or "you will learn" not in proc.stdout:
            return fail(proc.stdout)
        script.write_text(
            "# Script\n\n## Hook\nWORDS:\nWrite the next action on the card before you close the list.\n",
            encoding="utf-8",
        )
        clean = subprocess.run(
            [sys.executable, str(TOOL), str(packet), "--strict"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if clean.returncode != 0 or "clear" not in clean.stdout:
            return fail(clean.stdout + clean.stderr)
    print("QUALITY SCAN CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
