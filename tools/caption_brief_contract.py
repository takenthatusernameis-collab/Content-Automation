#!/usr/bin/env python3
"""Contract for caption_brief.py cue text. Does not call YouTube."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "caption_brief.py"


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
            "Close the window before the next block starts.\n\n"
            "VISUAL:\n*Open window card*\n\n"
            "## Beat 1\n"
            "WORDS:\nThe draft pulls attention before the first line.\n\n"
            "VISUAL:\n*Desk card*\n\n"
            "## Beat 2\n"
            "WORDS: Do not *reopen* the inbox until the block ends.\n"
            "ON SCREEN: STOP\n\n"
            "## Beat 3\n"
            "- Close the lid.\n"
            "- Leave the charger in the kitchen.\n"
            "*Lid card*\n",
            encoding="utf-8",
        )
        result = run(packet)
        out = result.stdout
        if result.returncode != 0:
            failures.append(f"dry-run exit {result.returncode}: {result.stderr}")
        if "Close the window before the next block starts." not in out:
            failures.append("plain beat must fill the cue, not an empty dash")
        if "The draft pulls attention before the first line." not in out:
            failures.append("WORDS beat must still fill the cue")
        if "Open window card" in out or "Desk card" in out or "Lid card" in out:
            failures.append("visual note must not become a cue")
        if "reopen" not in out or "Do not the inbox" in out:
            failures.append("inline emphasis must keep the spoken word")
        if "ON SCREEN" in out or "STOP" in out:
            failures.append("on-screen label must not become a cue")
        if "— - Close" in out or "- Close the lid. - Leave" in out:
            failures.append("list markers must not stay in the cue")
        if "Close the lid. Leave the charger in the kitchen." not in out:
            failures.append("bullet beat must still speak both lines")
        if "— \n" in out or out.rstrip().endswith("—"):
            failures.append(f"empty cue still printed:\n{out}")
    if failures:
        print("CAPTION BRIEF CONTRACT FAIL")
        for item in failures:
            print(f"- {item}")
        return 1
    print("CAPTION BRIEF CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
