#!/usr/bin/env python3
"""Soft thumbnail format match for a packet.

Checks on-disk thumbnail.png PNG IHDR color type and bit depth against YouTube preferred
(8-bit truecolor or truecolor+alpha). When present and mismatched, surfaces a ready dry-run
ffmpeg conversion command. Complements thumbnail_size_match and thumbnail_bytes_match.
Does not change hard gates, invent media, run ffmpeg, poll secrets, or write files.
Reusable across packets.
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
# PNG color types: 0=grayscale, 2=truecolor (RGB), 3=indexed, 4=grayscale+alpha, 6=truecolor+alpha (RGBA)
PREFERRED_COLOR_TYPES = {2, 6}
PREFERRED_BIT_DEPTH = 8


def png_ihdr(path: Path) -> tuple[int, int, int] | None:
    """Return (bit_depth, color_type, interlace) or None if not a valid PNG."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) < 29 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    # IHDR is first chunk: length(4) + "IHDR"(4) + data(13)
    if data[12:16] != b"IHDR":
        return None
    # data[16:29] = width(4) height(4) bit_depth(1) color_type(1) compression(1) filter(1) interlace(1)
    bit_depth = data[24]
    color_type = data[25]
    interlace = data[28]
    return bit_depth, color_type, interlace


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"not a directory: {packet}", file=sys.stderr)
        return 1

    thumb = packet / "thumbnail.png"
    print("THUMBNAIL FORMAT MATCH (soft only; gates unchanged)")
    print(f"Packet: {packet.name}")
    print()

    if not thumb.is_file():
        print("thumbnail.png: not present")
        print("THUMBNAIL FORMAT MATCH PASS (soft)")
        return 0

    info = png_ihdr(thumb)
    if info is None:
        print("thumbnail.png: present but not a valid PNG (or IHDR unreadable)")
        print("Suggested dry-run (does not execute): ffmpeg -y -i thumbnail.png thumbnail-fixed.png")
        print("THUMBNAIL FORMAT MATCH PASS (soft)")
        return 0

    bit_depth, color_type, interlace = info
    color_names = {
        0: "grayscale",
        2: "truecolor (RGB)",
        3: "indexed-color",
        4: "grayscale+alpha",
        6: "truecolor+alpha (RGBA)",
    }
    cname = color_names.get(color_type, f"unknown({color_type})")
    print(f"bit_depth: {bit_depth}")
    print(f"color_type: {color_type} ({cname})")
    print(f"interlace: {interlace}")
    print(f"Preferred: 8-bit truecolor or truecolor+alpha")

    match = bit_depth == PREFERRED_BIT_DEPTH and color_type in PREFERRED_COLOR_TYPES
    if match:
        print("FORMAT MATCH: yes")
    else:
        print("FORMAT MATCH: no")
        # Suggest conversion to RGB (drop alpha if present) or to standard
        if color_type in (4, 6):
            cmd = "ffmpeg -y -i thumbnail.png -pix_fmt rgb24 thumbnail-rgb.png"
            print(f"Suggested dry-run (does not execute; drops alpha): {cmd}")
        else:
            cmd = "ffmpeg -y -i thumbnail.png -pix_fmt rgb24 thumbnail-rgb.png"
            print(f"Suggested dry-run (does not execute): {cmd}")
        print("NOTE: YouTube accepts PNG; RGB is safer and often smaller. Soft only; review visual quality.")
    print()
    print("Human next: docs/human_oauth_checklist.md or python3 tools/human_one_pager.py")
    print("THUMBNAIL FORMAT MATCH PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
