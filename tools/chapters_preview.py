#!/usr/bin/env python3
"""Generate a local 1920x1080 chapters preview PNG from packet chapters.md.

Extracts YouTube chapter lines (timestamp + title) and renders a clean visual list
with a simple timeline bar. No invented claims. Output is local only (gitignored).
Reduces recurring human labor of scanning chapters.md to review the YouTube chapter list
before pasting into the description on every packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WIDTH, HEIGHT = 1920, 1080
BG = (18, 18, 22)
FG = (245, 243, 238)
ACCENT = (232, 196, 104)
MUTED = (120, 116, 110)
PANEL_BG = (28, 28, 32)
BORDER = (58, 56, 52)
BAR = (70, 120, 180)


def extract_youtube_lines(text: str) -> list[tuple[str, str]]:
    """Extract timestamp + title pairs from ## YouTube lines section."""
    pattern = r"^##\s+YouTube lines\s*\n(.*?)(?=^##|\Z)"
    match = re.search(pattern, text, re.M | re.S)
    if not match:
        return []
    body = match.group(1).strip()
    lines = []
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        m = re.match(r"^(\d+:\d{2})\s+(.+)$", line)
        if m:
            lines.append((m.group(1), m.group(2).strip()))
    return lines


def _parse_time(ts: str) -> float:
    """Convert M:SS or MM:SS to seconds."""
    parts = ts.split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    return 0.0


def _pil():
    from PIL import Image, ImageDraw, ImageFont
    return Image, ImageDraw, ImageFont


def _font(size: int):
    _, _, ImageFont = _pil()
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except Exception:
        return ImageFont.load_default()


def generate(packet: Path, out: Path | None = None) -> Path:
    chapters_path = packet / "chapters.md"
    if not chapters_path.is_file():
        raise FileNotFoundError(f"No chapters.md in {packet}")
    text = chapters_path.read_text(encoding="utf-8")

    chapters = extract_youtube_lines(text)
    if not chapters:
        chapters = [("0:00", "No chapters found")]

    Image, ImageDraw, _ = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    title_font = _font(32)
    head_font = _font(18)
    body_font = _font(16)
    small_font = _font(14)

    # Header
    draw.text((40, 30), "CHAPTERS PREVIEW", fill=ACCENT, font=title_font)
    draw.text((40, 80), packet.name, fill=MUTED, font=small_font)
    draw.text((40, 110), f"{len(chapters)} chapters  |  YouTube lines from chapters.md", fill=MUTED, font=small_font)

    # Timeline bar based on last timestamp
    if chapters:
        last_sec = _parse_time(chapters[-1][0])
        total = max(last_sec, 60.0)
    else:
        total = 60.0

    bar_y = 160
    bar_h = 40
    bar_x0 = 60
    bar_x1 = WIDTH - 60
    draw.rectangle([bar_x0, bar_y, bar_x1, bar_y + bar_h], fill=PANEL_BG, outline=BORDER, width=2)

    # Markers
    for ts, title in chapters:
        sec = _parse_time(ts)
        frac = sec / total if total else 0
        x = bar_x0 + (bar_x1 - bar_x0) * frac
        draw.line([(x, bar_y), (x, bar_y + bar_h)], fill=ACCENT, width=2)
        if frac < 0.95:
            short = title[:16]
            draw.text((x - 20, bar_y - 22), short, fill=FG, font=small_font)

    # List
    y = 240
    draw.text((40, y), "YouTube chapter lines (paste into description):", fill=ACCENT, font=head_font)
    y += 40
    for ts, title in chapters:
        line = f"{ts}  {title}"
        draw.rectangle([40, y - 4, WIDTH - 40, y + 32], fill=PANEL_BG, outline=BORDER, width=1)
        draw.text((60, y), line, fill=FG, font=body_font)
        y += 40
        if y > HEIGHT - 60:
            break

    out = out or (packet / "chapters_preview.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG")
    return out


def main():
    p = argparse.ArgumentParser(description="Generate local chapters preview PNG")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    try:
        result = generate(args.packet, args.out)
        print(f"Wrote {result} ({result.stat().st_size} bytes)")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
