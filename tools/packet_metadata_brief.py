#!/usr/bin/env python3
"""Packet metadata brief aggregator.

Prints combined results from title_scan, thumbnail_scan, description_scan, and
end_screen_scan for a packet. One command replaces sequential metadata quality
checks before filling or finalizing titles.md, thumbnail.md, publish.md, or
end-screen/CTA sections.
Does not invent titles, descriptions, or CTAs. Does not write files.
Does not call APIs. Reduces recurring labor of running four separate scanners
before locking publish metadata on every future packet.
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
    ("END-SCREEN / CTA SCAN", "end_screen_scan.py"),
]


def run_tool(script: str, packet: str) -> tuple[int, str]:
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), packet]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.strip()
    except Exception as e:
        return 1, f"EXCEPTION {script}: {e}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate title, thumbnail, description, and end-screen scans. No invented metadata."
    )
    parser.add_argument("packet", help="Packet folder")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("PACKET METADATA BRIEF (title + thumbnail + description + end-screen; revision signals only)")
    print("Use this before finalizing publish.md or titles.md. Hits are signals for human revision.")
    print("Does not invent titles, descriptions, or CTAs.")
    print("=" * 72)

    overall = 0
    for title, script in SECTIONS:
        print(f"\n## {title}")
        print("-" * 40)
        rc, out = run_tool(script, str(path))
        print(out or "(no output)")
        if rc != 0:
            overall = max(overall, rc)

    print("\n" + "=" * 72)
    print("NEXT: revise any hits in titles.md, thumbnail.md, or publish.md sections.")
    print("Then re-run this brief or the individual scanners with --strict if a hard gate is wanted.")
    print("See docs/content_quality.md for patterns. This tool writes nothing.")
    return overall


if __name__ == "__main__":
    sys.exit(main())
