#!/usr/bin/env python3
"""Print a structured human-friendly thumbnail spot-check list.

Looks for common thumbnail PNG/JPG files in the packet (does not invent or rewrite).
Prints file presence, size, and (when Pillow is available) dimensions, aspect ratio,
and soft flags for common YouTube issues (wrong size, not 16:9, large file, etc.).
Hard gates remain elsewhere. Reduces recurring thumbnail sensory review minutes
across future videos by giving a scannable checklist instead of raw file inspection.
Does not call YouTube, does not encode, does not write files.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PREFERRED = [(1280, 720), (1920, 1080)]
MAX_BYTES = 2 * 1024 * 1024  # 2 MB YouTube limit
MIN_BYTES = 10 * 1024
ASPECT_TOL = 0.05  # ~16:9

CANDIDATES = [
    "thumbnail.png",
    "thumb.png",
    "thumbnail.jpg",
    "thumb.jpg",
    "assets/thumbnail.png",
    "cards/thumbnail.png",
]


def find_thumbnail(packet: Path) -> Path | None:
    for name in CANDIDATES:
        p = packet / name
        if p.is_file():
            return p
    # Also check any *thumb*.png / *thumbnail*
    for p in packet.rglob("*thumb*.png"):
        if p.is_file():
            return p
    for p in packet.rglob("*thumbnail*.png"):
        if p.is_file():
            return p
    return None


def inspect_with_pillow(path: Path) -> dict:
    try:
        from PIL import Image
        with Image.open(path) as im:
            w, h = im.size
            mode = im.mode
            aspect = w / h if h else 0
            return {"width": w, "height": h, "mode": mode, "aspect": aspect, "ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print structured thumbnail spot-check (no invent, no write)."
    )
    parser.add_argument("packet", type=Path, help="Packet folder")
    args = parser.parse_args()
    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}")
        return 1

    path = find_thumbnail(packet)
    print("THUMBNAIL SPOTCHECK ASSISTANT (structured review list; no invent, no write)")
    print(f"Packet: {packet}")
    print("=" * 70)
    print()

    if path is None:
        print("No thumbnail file found (checked common names: thumbnail.png, thumb.png, etc.)")
        print("Soft flag: missing. Human still needs to supply or generate the PNG.")
        print("Suggested: place a 1280x720 or 1920x1080 16:9 PNG under 2 MB.")
        return 0

    size = path.stat().st_size
    print(f"File: {path.relative_to(packet)} ({size} bytes)")
    flags = []

    if size > MAX_BYTES:
        flags.append("too_large")
    if size < MIN_BYTES:
        flags.append("too_small")

    info = inspect_with_pillow(path)
    if info.get("ok"):
        w, h = info["width"], info["height"]
        aspect = info["aspect"]
        print(f"Dimensions: {w}x{h}  mode={info['mode']}  aspect={aspect:.3f}")
        target = 16 / 9
        if abs(aspect - target) > ASPECT_TOL:
            flags.append("not_16_9")
        if (w, h) not in PREFERRED and (h, w) not in PREFERRED:
            flags.append("non_preferred_size")
        if w < 1280 or h < 720:
            flags.append("below_min_recommended")
    else:
        print(f"Pillow inspect failed: {info.get('error', 'unknown')}")
        flags.append("unreadable")

    flag_str = ", ".join(flags) if flags else "none"
    print(f"Soft flags: {flag_str}")
    print()
    print("Soft flag summary (human still verifies sensory quality):")
    print(f"  too_large (>{MAX_BYTES} bytes): {'yes' if 'too_large' in flags else 'no'}")
    print(f"  too_small (<{MIN_BYTES} bytes): {'yes' if 'too_small' in flags else 'no'}")
    print(f"  not_16_9: {'yes' if 'not_16_9' in flags else 'no'}")
    print(f"  non_preferred_size (not 1280x720 or 1920x1080): {'yes' if 'non_preferred_size' in flags else 'no'}")
    print(f"  below_min_recommended: {'yes' if 'below_min_recommended' in flags else 'no'}")
    print()
    print("These flags are soft hints only. Sensory review (clarity, text, contrast) remains human.")
    print("Spot-check time is reduced by scanning this list instead of raw file properties.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
