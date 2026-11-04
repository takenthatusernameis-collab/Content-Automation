#!/usr/bin/env python3
"""Soft thumbnail bytes match for a packet.

Checks on-disk thumbnail.png file size against YouTube preferred max 2 MiB.
When present and over limit, surfaces a ready dry-run ffmpeg compression command.
Does not change hard gates, invent media, run ffmpeg, poll secrets, or write files.
Reusable across packets. Complements thumbnail_size_match and media_qa soft reports.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
MAX_BYTES = 2 * 1024 * 1024  # 2 MiB YouTube limit


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"not a directory: {packet}", file=sys.stderr)
        return 1

    thumb = packet / "thumbnail.png"
    print("THUMBNAIL BYTES MATCH (soft only; gates unchanged)")
    print(f"Packet: {packet.name}")
    print()

    if not thumb.is_file():
        print("thumbnail.png: not present")
        print("THUMBNAIL BYTES MATCH PASS (soft)")
        return 0

    size = thumb.stat().st_size
    print(f"Current bytes: {size}")
    print(f"Max preferred: {MAX_BYTES} (2 MiB)")
    if size <= MAX_BYTES:
        print("BYTES MATCH: yes")
    else:
        print("BYTES MATCH: no")
        cmd = "ffmpeg -y -i thumbnail.png -q:v 5 thumbnail-compressed.png"
        print(f"Suggested dry-run (does not execute): {cmd}")
        print("NOTE: adjust -q:v or use pngquant/optipng as needed; soft only; review size and quality")
    print()
    print("Human next: docs/human_oauth_checklist.md or python3 tools/human_one_pager.py")
    print("THUMBNAIL BYTES MATCH PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
