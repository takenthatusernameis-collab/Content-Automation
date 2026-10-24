#!/usr/bin/env python3
"""Aggregate publish metadata suggestions into one brief.

Runs the existing no-write title, description, tags, thumbnail, end-screen,
first-comment, and CTA suggesters and prints a unified publish prep brief.
Reduces the recurring labor of invoking multiple separate tools and collecting
their outputs before locking publish.md. Does not write files, invent final
copy, or call external services.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

SECTIONS = [
    ("TITLE SUGGESTIONS", "title_suggest.py"),
    ("DESCRIPTION SUGGESTION", "description_suggest.py"),
    ("TAGS SUGGESTIONS", "tags_suggest.py"),
    ("THUMBNAIL SUGGESTIONS", "thumbnail_suggest.py"),
    ("END SCREEN / CTA SUGGESTIONS", "end_screen_suggest.py"),
    ("FIRST COMMENT SUGGESTION", "first_comment_suggest.py"),
    ("CTA SUGGESTION", "cta_suggest.py"),
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
        description="Print a unified publish metadata brief from existing suggesters. No file writes."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("PUBLISH PREP BRIEF (unified metadata suggestions; starting points only)")
    print("Aggregates existing no-write suggesters. Use as starting points for titles.md and publish.md.")
    print("Human locks final Primary, Description, Tags, Thumbnail text, End screen, and First comment.")
    print("Run the corresponding *_scan.py tools after pasting to confirm no weak patterns.")
    print("=" * 72)
    print()

    any_ok = False
    for title, script in SECTIONS:
        print(f"## {title}")
        print("-" * 40)
        rc, output = run_tool(script, str(path))
        if rc == 0 and output and "No idea.md" not in output and "MISSING" not in output:
            any_ok = True
            print(output)
        else:
            print(output or f"(no useful output from {script})")
        print()
        print()

    print("=" * 72)
    print("Next: paste chosen lines into titles.md and publish.md, then run title_scan.py, description_scan.py, thumbnail_scan.py, end_screen_scan.py, and first_comment_scan.py.")
    print("Do not treat suggestions as locked upload copy.")
    if not any_ok:
        print("No section produced useful suggestions. Ensure idea.md exists.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
