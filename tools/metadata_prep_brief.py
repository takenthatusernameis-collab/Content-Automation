#!/usr/bin/env python3
"""Aggregate publish metadata scans into one brief.

Runs the existing no-write title_scan, thumbnail_scan, description_scan,
end_screen_scan, first_comment_scan, chapters_scan, and mechanism_align_scan
and prints a unified metadata prep brief.
Reduces the recurring labor of invoking multiple separate scanners and
collecting their outputs before locking titles.md / publish.md / chapters.md.
Does not rewrite metadata, invent claims, or call external services.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

SECTIONS = [
    ("TITLE SCAN", "title_scan.py"),
    ("THUMBNAIL SCAN", "thumbnail_scan.py"),
    ("DESCRIPTION SCAN", "description_scan.py"),
    ("END SCREEN SCAN", "end_screen_scan.py"),
    ("FIRST COMMENT SCAN", "first_comment_scan.py"),
    ("CHAPTERS SCAN", "chapters_scan.py"),
    ("MECHANISM ALIGNMENT SCAN", "mechanism_align_scan.py"),
]


def run_tool(script: str, packet: str) -> tuple[int, str]:
    """Run one scanner and return (returncode, output)."""
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
        description="Print a unified publish metadata brief from existing scanners. No file writes."
    )
    parser.add_argument("packet", help="Packet folder containing titles.md / publish.md / idea.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("METADATA PREP BRIEF (unified publish metadata quality signals; revision signals only)")
    print("Aggregates existing no-write scanners. Hits are signals for human revision, not automatic rewrites.")
    print("Run individual scanners with --strict if a hard gate is required. Do not invent claims or clickbait.")
    print("=" * 72)
    print()

    any_ok = False
    for title, script in SECTIONS:
        print(f"## {title}")
        print("-" * 40)
        rc, output = run_tool(script, str(path))
        if output and "MISSING" not in output:
            any_ok = True
            print(output)
        else:
            print(output or f"(no useful output from {script})")
        print()
        print()

    print("=" * 72)
    print("Next: revise titles.md / publish.md / chapters.md if hits remain, then re-run this brief or the individual scanners.")
    print("Lock metadata only after clear title, thumbnail, description, end-screen, first-comment, chapter, and mechanism signals. See docs/content_quality.md.")
    if not any_ok:
        print("No section produced useful output. Ensure relevant packet files exist.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
