#!/usr/bin/env python3
"""Generate multiple local 1280x720 YouTube thumbnail PNG variants from the packet title.

Deterministic designs only. No stock, no invented text beyond the locked title,
no git commits of the binaries. Outputs: packet/thumbnail_variant_{1-4}.png
(gitignored). Compatible with basic YouTube thumbnail requirements.

Reduces recurring human labor of manually designing alternate thumbnail layouts
on every future packet. One command produces a small set of options for review.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WIDTH, HEIGHT = 1280, 720
BG_DARK = (18, 18, 22)
FG_LIGHT = (245, 243, 238)
ACCENT = (232, 196, 104)
RULE = (58, 56, 52)
BG_LIGHT = (245, 243, 238)
FG_DARK = (18, 18, 22)
ACCENT_DARK = (36, 42, 58)


def extract_title(publish_text: str) -> str:
    match = re.search(
        r"^##\s+Title to upload\s*\n(.+?)(?:\n##|\n\n|\Z)",
        publish_text,
        re.M | re.S,
    )
    if match:
        title = match.group(1).strip()
        if title:
            return title
    lines = publish_text.splitlines()
    for i, line in enumerate(lines):
        if "title to upload" in line.lower():
            for next_line in lines[i + 1 :]:
                stripped = next_line.strip()
                if stripped and not stripped.startswith("#"):
                    return stripped
    return "Untitled"


def _pil():
    from PIL import Image, ImageDraw, ImageFont
    return Image, ImageDraw, ImageFont


def _font(size: int, bold: bool = True):
    _, _, ImageFont = _pil()
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    candidates = (
        f"/usr/share/fonts/truetype/dejavu/{name}",
        f"/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    )
    for path in candidates:
        if Path(path).is_file():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def _wrap(draw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
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


def render_variant_1(title: str):
    """Dark background, top accent bar, centered text (classic)."""
    Image, ImageDraw, _ = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw.rectangle((40, 40, WIDTH - 40, HEIGHT - 40), outline=RULE, width=4)
    draw.rectangle((40, 40, WIDTH - 40, 110), fill=ACCENT)
    draw.text((60, 58), "NEXT ACTION", font=_font(32), fill=BG_DARK)

    font = _font(68)
    lines = _wrap(draw, title, font, WIDTH - 180)
    total_h = sum(font.getbbox(line or "X")[3] - font.getbbox(line or "X")[1] + 14 for line in lines)
    y = 160 + (HEIGHT - 220 - total_h) // 2
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text(((WIDTH - w) / 2, y), line, font=font, fill=FG_LIGHT)
        bbox = font.getbbox(line or "X")
        y += (bbox[3] - bbox[1]) + 14
    return img


def render_variant_2(title: str):
    """Light background, dark text, bottom accent bar."""
    Image, ImageDraw, _ = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, HEIGHT - 80, WIDTH, HEIGHT), fill=ACCENT)
    draw.text((40, HEIGHT - 62), "ONE WRITTEN DEFAULT", font=_font(28), fill=BG_DARK)

    font = _font(64)
    lines = _wrap(draw, title, font, WIDTH - 120)
    total_h = sum(font.getbbox(line or "X")[3] - font.getbbox(line or "X")[1] + 12 for line in lines)
    y = 80 + (HEIGHT - 200 - total_h) // 2
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text(((WIDTH - w) / 2, y), line, font=font, fill=FG_DARK)
        bbox = font.getbbox(line or "X")
        y += (bbox[3] - bbox[1]) + 12
    return img


def render_variant_3(title: str):
    """Split: left accent panel with keyword, right title."""
    Image, ImageDraw, _ = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 420, HEIGHT), fill=ACCENT)
    # Big keyword
    kw_font = _font(80)
    draw.text((40, 280), "STOP", font=kw_font, fill=BG_DARK)
    draw.text((40, 380), "DECIDING", font=_font(36), fill=BG_DARK)

    font = _font(56)
    lines = _wrap(draw, title, font, WIDTH - 500)
    y = 140
    for line in lines:
        draw.text((460, y), line, font=font, fill=FG_LIGHT)
        bbox = font.getbbox(line or "X")
        y += (bbox[3] - bbox[1]) + 16
    return img


def render_variant_4(title: str):
    """Minimal centered, thin rules, high contrast."""
    Image, ImageDraw, _ = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw.line((200, 180, WIDTH - 200, 180), fill=ACCENT, width=3)
    draw.line((200, HEIGHT - 180, WIDTH - 200, HEIGHT - 180), fill=ACCENT, width=3)

    font = _font(72)
    lines = _wrap(draw, title, font, WIDTH - 160)
    total_h = sum(font.getbbox(line or "X")[3] - font.getbbox(line or "X")[1] + 16 for line in lines)
    y = (HEIGHT - total_h) // 2
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text(((WIDTH - w) / 2, y), line, font=font, fill=FG_LIGHT)
        bbox = font.getbbox(line or "X")
        y += (bbox[3] - bbox[1]) + 16
    return img


VARIANTS = [
    ("1", render_variant_1),
    ("2", render_variant_2),
    ("3", render_variant_3),
    ("4", render_variant_4),
]


def main() -> int:
    p = argparse.ArgumentParser(description="Generate multiple local thumbnail PNG variants from title")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    publish = packet / "publish.md"
    if not publish.is_file():
        print("ERROR: publish.md missing", file=sys.stderr)
        return 1

    title = extract_title(publish.read_text(encoding="utf-8"))
    print(f"title: {title}")

    generated = 0
    for suffix, renderer in VARIANTS:
        try:
            img = renderer(title)
            out = packet / f"thumbnail_variant_{suffix}.png"
            img.save(out, "PNG")
            print(f"  wrote {out.name} ({out.stat().st_size} bytes)")
            generated += 1
        except Exception as e:
            print(f"  FAIL variant {suffix}: {e}", file=sys.stderr)

    print(f"\n{generated}/{len(VARIANTS)} variants generated (gitignored)")
    return 0 if generated > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
