#!/usr/bin/env python3
"""Generate a local preview PNG of the CTA text.

Prefers ranked End screen text from recommended_publish_fill.md when present
(compounding the metadata ranking/fill work); falls back to script.md CTA WORDS.
Renders it as a large, readable text card PNG. Output: packet/cta_preview.png (gitignored).
No invented content, no external services. Reduces recurring human labor of
scrolling to the end of the script just to review the closing CTA on every future packet.
One command produces a glanceable CTA image aligned with selected metadata when available.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from phrase_utils import extract_recommended_end_screen, extract_cta_from_script

WIDTH, HEIGHT = 1280, 720
BG = (18, 18, 22)
FG = (245, 243, 238)
ACCENT = (232, 196, 104)
MUTED = (140, 136, 130)
LINE = (58, 56, 52)



def _font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    candidates = (
        f"/usr/share/fonts/truetype/dejavu/{name}",
        f"/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    )
    for p in candidates:
        if Path(p).is_file():
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                pass
    return ImageFont.load_default()


def _wrap(draw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines = []
    cur = words[0]
    for w in words[1:]:
        trial = f"{cur} {w}"
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def main() -> int:
    p = argparse.ArgumentParser(description="Generate local CTA preview PNG preferring ranked End screen text")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    cta = None
    source = "script"
    fill_path = packet / "recommended_publish_fill.md"
    if fill_path.is_file():
        rec = extract_recommended_end_screen(fill_path.read_text(encoding="utf-8"))
        if rec:
            cta = rec
            source = "recommended-fill"

    if not cta:
        script = packet / "script.md"
        if not script.is_file():
            print("ERROR: script.md missing and no recommended end-screen text", file=sys.stderr)
            return 1
        cta = extract_cta_from_script(script.read_text(encoding="utf-8"))
        source = "script"

    print(f"packet: {packet.name}")
    print(f"cta source: {source}")
    print(f"cta: {cta[:80]}...")

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((20, 20, WIDTH - 20, HEIGHT - 20), outline=LINE, width=3)
    draw.text((40, 40), "CTA PREVIEW", font=_font(22, bold=True), fill=ACCENT)

    font = _font(36)
    lines = _wrap(draw, cta, font, WIDTH - 100)
    y = 100
    for line in lines[:8]:  # max 8 lines
        draw.text((50, y), line, font=font, fill=FG)
        bbox = font.getbbox(line or "X")
        y += (bbox[3] - bbox[1]) + 12

    footer = "CTA from recommended fill or script.md — gitignored preview"
    draw.text((40, HEIGHT - 50), footer, font=_font(16), fill=MUTED)

    out = packet / "cta_preview.png"
    img.save(out, "PNG")
    print(f"wrote: {out}")
    print(f"size: {out.stat().st_size} bytes")
    print("CTA preview ready (gitignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
