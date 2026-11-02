#!/usr/bin/env python3
"""Generate a local 1920x1080 end-screen preview PNG.

Shows CTA text in the safe zone and marks lower-left / lower-right areas
reserved for YouTube end-screen elements (last 20s rule).
Prefers ranked End screen text from recommended_publish_fill.md when present
(after the recent metadata ranking work); falls back to script.md CTA.
No invented claims. Output is local only (gitignored).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from phrase_utils import extract_recommended_end_screen, extract_cta_from_script

WIDTH, HEIGHT = 1920, 1080
BG = (18, 18, 22)
FG = (245, 243, 238)
ACCENT = (232, 196, 104)
MUTED = (120, 116, 110)
SAFE = (40, 80, 40)
RESERVED = (80, 40, 40)



def _pil():
    from PIL import Image, ImageDraw, ImageFont
    return Image, ImageDraw, ImageFont


def _font(size: int):
    _, _, ImageFont = _pil()
    candidates = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    )
    for path in candidates:
        if Path(path).is_file():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def render_preview(cta: str):
    Image, ImageDraw, _ = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    # Safe center zone
    draw.rectangle((200, 120, WIDTH - 200, HEIGHT - 280), outline=SAFE, width=4)
    draw.text((220, 140), "SAFE ZONE (CTA stays readable)", font=_font(24), fill=SAFE)

    # Reserved lower-left and lower-right
    draw.rectangle((40, HEIGHT - 240, 480, HEIGHT - 40), outline=RESERVED, width=3)
    draw.text((60, HEIGHT - 220), "RESERVED\nlower-left\n(YouTube element)", font=_font(22), fill=RESERVED)

    draw.rectangle((WIDTH - 480, HEIGHT - 240, WIDTH - 40, HEIGHT - 40), outline=RESERVED, width=3)
    draw.text((WIDTH - 460, HEIGHT - 220), "RESERVED\nlower-right\n(YouTube element)", font=_font(22), fill=RESERVED)

    # CTA text
    font = _font(48)
    lines = []
    words = cta.split()
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= WIDTH - 500:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    y = 360
    for line in lines[:4]:
        w = draw.textlength(line, font=font)
        draw.text(((WIDTH - w) / 2, y), line, font=font, fill=FG)
        y += 70

    draw.text((WIDTH // 2 - 180, HEIGHT - 100), "End-screen preview (local only)", font=_font(20), fill=MUTED)
    return img


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local end-screen preview PNG with safe zones")
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    cta = None
    source = "script"
    fill_path = path / "recommended_publish_fill.md"
    if fill_path.is_file():
        rec = extract_recommended_end_screen(fill_path.read_text(encoding="utf-8"))
        if rec:
            cta = rec
            source = "recommended-fill"

    if not cta:
        script = path / "script.md"
        if not script.is_file():
            print("missing script.md and no recommended end-screen text", file=sys.stderr)
            return 1
        cta = extract_cta_from_script(script.read_text(encoding="utf-8"))
        source = "script"

    print(f"packet: {path.name}")
    print(f"cta source: {source}")
    print(f"cta: {cta}")

    dest = path / "end_screen_preview.png"
    if args.dry_run:
        print(f"would write: {dest}")
        return 0

    img = render_preview(cta)
    img.save(dest, format="PNG")
    print(f"wrote: {dest}")
    print(f"size: {dest.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
