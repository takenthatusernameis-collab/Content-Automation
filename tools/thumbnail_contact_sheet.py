#!/usr/bin/env python3
"""Generate a local contact sheet of the four thumbnail variants.

Reads thumbnail_variant_1.png through _4.png (produced by thumbnail_variants.py)
and composites them into a single 2x2 contact sheet PNG for faster visual review.
Output: packet/thumbnail_contact_sheet.png (gitignored).
No invented text. Deterministic layout. Reduces labor of opening four separate files.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CELL_W, CELL_H = 640, 360  # half of 1280x720
GAP = 20
LABEL_H = 40
BG = (30, 30, 34)
FG = (220, 220, 220)


def _font(size: int):
    candidates = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    )
    for p in candidates:
        if Path(p).is_file():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


def main() -> int:
    p = argparse.ArgumentParser(description="Create a 2x2 contact sheet of thumbnail variants")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    variants = []
    for i in range(1, 5):
        path = packet / f"thumbnail_variant_{i}.png"
        if not path.is_file():
            print(f"ERROR: missing {path.name}. Run tools/thumbnail_variants.py first.", file=sys.stderr)
            return 1
        variants.append(Image.open(path).convert("RGB"))

    sheet_w = CELL_W * 2 + GAP * 3
    sheet_h = (CELL_H + LABEL_H) * 2 + GAP * 3
    sheet = Image.new("RGB", (sheet_w, sheet_h), BG)
    draw = ImageDraw.Draw(sheet)
    font = _font(22)

    positions = [
        (GAP, GAP),
        (GAP + CELL_W + GAP, GAP),
        (GAP, GAP + CELL_H + LABEL_H + GAP),
        (GAP + CELL_W + GAP, GAP + CELL_H + LABEL_H + GAP),
    ]

    for idx, (img, (x, y)) in enumerate(zip(variants, positions), 1):
        resized = img.resize((CELL_W, CELL_H), Image.Resampling.LANCZOS)
        sheet.paste(resized, (x, y))
        label = f"Variant {idx}"
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((x + (CELL_W - tw) // 2, y + CELL_H + 8), label, font=font, fill=FG)

    out = packet / "thumbnail_contact_sheet.png"
    sheet.save(out, "PNG")
    print(f"wrote {out.name} ({out.stat().st_size} bytes)")
    print("Contact sheet ready for quick visual review (gitignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
