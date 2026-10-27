#!/usr/bin/env python3
"""Generate a local contact sheet of the main review preview PNGs.

Looks for a fixed set of gitignored preview images produced by other tools
(hook, claims, title variants, packet status, storyboard, pacing, etc.)
and composites the ones that exist into a single multi-panel overview PNG.
Output: packet/review_contact_sheet.png (gitignored).

No invented content. Deterministic layout. Reduces recurring human labor of
opening many separate preview files after running preview_all.py on every
future packet. One glanceable sheet for the common review set.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Preferred order; skip missing
CANDIDATES = [
    ("hook", "hook_preview.png"),
    ("claims", "claims_preview.png"),
    ("structure", "structure_preview.png"),
    ("title", "title_variants_preview.png"),
    ("status", "packet_status_card.png"),
    ("storyboard", "storyboard_preview.png"),
    ("pacing", "pacing_timeline.png"),
    ("assets", "assets_preview.png"),
    ("chapters", "chapters_preview.png"),
]

CELL_W, CELL_H = 420, 236  # scaled down from typical 1280x720
GAP = 16
LABEL_H = 32
BG = (24, 24, 28)
FG = (230, 228, 222)
ACCENT = (232, 196, 104)
MUTED = (140, 136, 130)


def _font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    candidates = (
        f"/usr/share/fonts/truetype/dejavu/{name}",
        f"/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    )
    for p in candidates:
        if Path(p).is_file():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


def main() -> int:
    p = argparse.ArgumentParser(description="Create a contact sheet of available review previews")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    found = []
    for label, fname in CANDIDATES:
        path = packet / fname
        if path.is_file():
            try:
                img = Image.open(path).convert("RGB")
                found.append((label, img))
            except Exception:
                continue

    if not found:
        print("ERROR: no review preview PNGs found. Run tools/preview_all.py first.", file=sys.stderr)
        return 1

    n = len(found)
    cols = min(4, n)
    rows = (n + cols - 1) // cols
    sheet_w = cols * CELL_W + (cols + 1) * GAP
    sheet_h = rows * (CELL_H + LABEL_H) + (rows + 1) * GAP + 60  # header space

    sheet = Image.new("RGB", (sheet_w, sheet_h), BG)
    draw = ImageDraw.Draw(sheet)
    title_font = _font(28, bold=True)
    label_font = _font(18)
    draw.text((GAP, 12), "REVIEW CONTACT SHEET", font=title_font, fill=ACCENT)
    draw.text((GAP, 48), f"{packet.name} — {n} previews", font=_font(16), fill=MUTED)

    for i, (label, img) in enumerate(found):
        r, c = divmod(i, cols)
        x = GAP + c * (CELL_W + GAP)
        y = 80 + r * (CELL_H + LABEL_H + GAP)
        resized = img.resize((CELL_W, CELL_H), Image.Resampling.LANCZOS)
        sheet.paste(resized, (x, y))
        # Label bar
        draw.rectangle((x, y + CELL_H, x + CELL_W, y + CELL_H + LABEL_H), fill=(40, 40, 46))
        bbox = draw.textbbox((0, 0), label, font=label_font)
        tw = bbox[2] - bbox[0]
        draw.text((x + (CELL_W - tw) // 2, y + CELL_H + 6), label, font=label_font, fill=FG)

    out = packet / "review_contact_sheet.png"
    sheet.save(out, "PNG")
    print(f"wrote: {out}")
    print(f"size: {out.stat().st_size} bytes")
    print(f"panels: {n} (gitignored)")
    print("Review contact sheet ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
