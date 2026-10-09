#!/usr/bin/env python3
"""Contract for asset_brief.py card needs. Does not call YouTube."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "asset_brief.py"


def run(packet: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), str(packet), "--dry-run"],
        capture_output=True,
        text=True,
    )


def main() -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as raw:
        packet = Path(raw)
        (packet / "script.md").write_text(
            "# Script\n\n## Hook\n"
            "WORDS: Face the phone down in another room before the block.\n"
            "VISUAL: phone face up\n"
            "ON SCREEN: FACE DOWN\n\n"
            "## Beat\n"
            "WORDS: Do not reopen the inbox.\n"
            "VISUAL:\n*Open window card*\n"
            "ON SCREEN: STOP\n",
            encoding="utf-8",
        )
        result = run(packet)
        out = result.stdout
        if result.returncode != 0:
            failures.append(f"dry-run exit {result.returncode}: {result.stderr}")
        if "phone face up" not in out:
            failures.append("visual need must stay the spoken card description")
        if "Open window card" not in out:
            failures.append("italic visual note must still become a card need")
        if "ON SCREEN" in out or "FACE DOWN" in out or "STOP" in out:
            failures.append("on-screen label must not become a card need or filename")
        if "on-screen" in out:
            failures.append("on-screen label must not enter the suggested filename")
    if failures:
        print("ASSET BRIEF CONTRACT FAIL")
        for item in failures:
            print(f"- {item}")
        return 1
    print("ASSET BRIEF CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
