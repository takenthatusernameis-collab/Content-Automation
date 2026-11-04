#!/usr/bin/env python3
"""Soft thumbnail size match for a packet.

Checks on-disk thumbnail.png dimensions against YouTube preferred 1280x720.
When present and wrong size, surfaces a ready dry-run ffmpeg scale command.
Does not change hard gates, invent media, run ffmpeg, poll secrets, or write files.
Reusable across packets. Complements media_qa soft reports.
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
TARGET_W = 1280
TARGET_H = 720


def png_size(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return int(w), int(h)


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"not a directory: {packet}", file=sys.stderr)
        return 1

    thumb = packet / "thumbnail.png"
    print("THUMBNAIL SIZE MATCH (soft only; gates unchanged)")
    print(f"Packet: {packet.name}")
    print()

    if not thumb.is_file():
        print("thumbnail.png: not present")
        print("THUMBNAIL SIZE MATCH PASS (soft)")
        return 0

    size = png_size(thumb)
    if size is None:
        print("thumbnail.png: present but unreadable PNG header")
        print("THUMBNAIL SIZE MATCH PASS (soft)")
        return 0

    w, h = size
    print(f"Current size: {w}x{h}")
    print(f"Target size: {TARGET_W}x{TARGET_H}")
    if (w, h) == (TARGET_W, TARGET_H):
        print("SIZE MATCH: yes")
    else:
        print("SIZE MATCH: no")
        cmd = (
            f"ffmpeg -y -i thumbnail.png -vf scale={TARGET_W}:{TARGET_H}:force_original_aspect_ratio=decrease,"
            f"pad={TARGET_W}:{TARGET_H}:(ow-iw)/2:(oh-ih)/2 thumbnail-{TARGET_W}x{TARGET_H}.png"
        )
        print(f"Suggested dry-run (does not execute): {cmd}")
        print("NOTE: review crop/pad visually before using; soft only")
    print()
    print("Human next: docs/human_oauth_checklist.md or python3 tools/human_one_pager.py")
    print("THUMBNAIL SIZE MATCH PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
