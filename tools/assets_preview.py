#!/usr/bin/env python3
"""Generate a local 1920x1080 assets preview PNG from packet assets.md.

Parses the ## Cards markdown table (Beat, Need, Type, Suggested file, Source, Status)
and renders a clean visual list of the planned cards. No invented claims.
Output is local only (gitignored). Reduces recurring human labor of scanning
assets.md to review the visual plan and card status on every future packet.
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


def parse_cards_table(text: str) -> list[dict]:
    """Extract rows from the Cards table."""
    # Find the table after ## Cards
    match = re.search(r"^## Cards\s*\n(.*?)(?=^##|\Z)", text, re.M | re.S)
    if not match:
        return []
    table = match.group(1)
    lines = [ln.strip() for ln in table.splitlines() if ln.strip()]
    cards = []
    for line in lines:
        if not line.startswith("|") or line.startswith("|------") or "Beat" in line:
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) >= 6:
            cards.append({
                "beat": parts[0],
                "need": parts[1],
                "type": parts[2],
                "file": parts[3],
                "source": parts[4],
                "status": parts[5],
            })
    return cards


def _pil():
    from PIL import Image, ImageDraw, ImageFont
    return Image, ImageDraw, ImageFont


def _font(size: int):
    _, _, ImageFont = _pil()
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except Exception:
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


def generate(packet: Path, out: Path | None = None) -> Path:
    assets_path = packet / "assets.md"
    if not assets_path.is_file():
        raise FileNotFoundError(f"No assets.md in {packet}")
    text = assets_path.read_text(encoding="utf-8")

    cards = parse_cards_table(text)
    if not cards:
        cards = [{"beat": "—", "need": "No cards table found", "type": "—", "file": "—", "source": "—", "status": "—"}]

    Image, ImageDraw, _ = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    title_font = _font(32)
    head_font = _font(18)
    body_font = _font(14)
    small_font = _font(13)

    # Header
    draw.text((40, 30), "ASSETS PREVIEW", fill=ACCENT, font=title_font)
    draw.text((40, 80), packet.name, fill=MUTED, font=small_font)
    draw.text((40, 110), f"{len(cards)} planned cards from assets.md", fill=MUTED, font=small_font)

    y = 160
    draw.text((40, y), "Planned cards (beat · type · status · need):", fill=ACCENT, font=head_font)
    y += 36

    for card in cards:
        beat = card["beat"][:40]
        typ = card["type"][:12]
        status = card["status"][:12]
        need_short = card["need"][:100] + ("..." if len(card["need"]) > 100 else "")
        header = f"{beat}  ·  {typ}  ·  {status}"
        draw.rectangle([40, y - 4, WIDTH - 40, y + 22], fill=PANEL_BG, outline=BORDER, width=1)
        draw.text((60, y), header, fill=ACCENT, font=body_font)
        y += 28
        need_lines = _wrap(draw, need_short, body_font, WIDTH - 140)
        for ln in need_lines[:2]:
            draw.text((70, y), ln, fill=FG, font=body_font)
            y += 20
        y += 12
        if y > HEIGHT - 80:
            break

    if len(cards) > 7:
        draw.text((40, HEIGHT - 50), f"... {len(cards)} cards total (full table on disk)", fill=MUTED, font=small_font)

    out = out or (packet / "assets_preview.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG")
    return out


def main():
    p = argparse.ArgumentParser(description="Generate local assets preview PNG")
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
