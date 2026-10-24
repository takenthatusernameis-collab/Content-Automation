#!/usr/bin/env python3
"""Aggregate editor operational suggestions into one brief.

Runs the existing no-write cue and text suggesters and prints a unified
editor prep brief. Reduces the recurring labor of invoking multiple
separate tools and collecting their outputs before an editor session.
Does not generate media, write files, invent content, or call external services.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

SECTIONS = [
    ("MUSIC / SFX CUES", "music_cue_suggest.py"),
    ("BROLL TEXTURE CUES", "broll_cue_suggest.py"),
    ("CARD TEXT SUGGESTIONS", "card_text_suggest.py"),
    ("CHAPTER SUGGESTIONS", "chapters_suggest.py"),
]


def run_tool(script: str, packet: str) -> tuple[int, str]:
    """Run one suggester and return (returncode, output)."""
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    try:
        proc = subprocess.run(
            [sys.executable, str(path), packet],
            capture_output=True,
            text=True,
            check=False,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.strip()
    except Exception as e:
        return 1, f"EXCEPTION running {script}: {e}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a unified editor operational brief from existing suggesters. No file writes."
    )
    parser.add_argument("packet", help="Packet folder containing assets.md or script.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("EDITOR PREP BRIEF (unified operational suggestions; no invented media)")
    print("Aggregates existing no-write suggesters. Use as starting points only.")
    print("Human decides final placement. Prefer empty optional tracks over distraction.")
    print("=" * 72)
    print()

    any_ok = False
    for title, script in SECTIONS:
        print(f"## {title}")
        print("-" * 40)
        rc, output = run_tool(script, str(path))
        if rc == 0 and output and "No assets.md" not in output and "MISSING" not in output:
            any_ok = True
            print(output)
        else:
            print(output or f"(no useful output from {script})")
        print()
        print()

    print("=" * 72)
    print("Next: apply preferred cues in the NLE. Run timeline.py --write and media_qa.py after assets exist.")
    print("Cards and VO carry the message. Optional tracks remain optional.")
    if not any_ok:
        print("No section produced useful suggestions. Ensure assets.md or script.md exists and run asset_brief.py first.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
