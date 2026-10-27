#!/usr/bin/env python3
"""Generate a local contact sheet of deterministic title variants from the locked title.

Reads the title from publish.md and produces four calm, mechanism-aligned variants
(original, shortened, question, action). Renders them as a 2x2 title-card contact sheet PNG.
Output: packet/title_variants_preview.png (gitignored).
No invented claims, no clickbait, no external services. Reduces recurring human labor
of brainstorming and visually comparing title options on every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 720
CELL_W, CELL_H = 600, 280
GAP = 30
BG = (18, 18, 22)
FG = (245, 243, 238)
ACCENT = (232, 196, 104)
MUTED = (140, 136, 130)
LINE = (58, 56, 52)


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


def generate_variants(title: str) -> list[tuple[str, str]]:
    """Return (label, text) pairs. Deterministic, no external calls."""
    original = title.strip()
    # Shortened: keep first ~45 chars at word boundary
    words = original.split()
    short = original
    if len(original) > 50:
        acc = []
        for w in words:
            trial = " ".join(acc + [w])
            if len(trial) <= 48:
                acc.append(w)
            else:
                break
        short = " ".join(acc) if acc else original[:45]
    # Question form
    q = original.rstrip(".")
    if not q.endswith("?"):
        if q.lower().startswith(("how", "why", "what", "when")):
            question = q + "?"
        else:
            question = "How to " + q[0].lower() + q[1:] + "?"
    else:
        question = q
    # Action form
    action = original
    if not original.lower().startswith(("stop", "write", "install", "use", "make")):
        action = "Write the " + original[0].lower() + original[1:]
    return [
        ("Original", original),
        ("Short", short),
        ("Question", question),
        ("Action", action),
    ]


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


def render_card(label: str, text: str) -> Image.Image:
    img = Image.new("RGB", (CELL_W, CELL_H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, CELL_W - 1, CELL_H - 1), outline=LINE, width=2)
    draw.text((16, 12), label, font=_font(18, bold=True), fill=ACCENT)
    font = _font(28)
    lines = _wrap(draw, text, font, CELL_W - 40)
    y = 50
    for line in lines[:4]:  # max 4 lines
        draw.text((20, y), line, font=font, fill=FG)
        bbox = font.getbbox(line or "X")
        y += (bbox[3] - bbox[1]) + 8
    return img


def main() -> int:
    p = argparse.ArgumentParser(description="Generate local title variants contact sheet")
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

    variants = generate_variants(title)
    cards = []
    for label, text in variants:
        cards.append(render_card(label, text))
        print(f"  {label}: {text[:60]}...")

    sheet_w = CELL_W * 2 + GAP * 3
    sheet_h = CELL_H * 2 + GAP * 3
    sheet = Image.new("RGB", (sheet_w, sheet_h), (12, 12, 16))
    positions = [
        (GAP, GAP),
        (GAP + CELL_W + GAP, GAP),
        (GAP, GAP + CELL_H + GAP),
        (GAP + CELL_W + GAP, GAP + CELL_H + GAP),
    ]
    for card, pos in zip(cards, positions):
        sheet.paste(card, pos)

    out = packet / "title_variants_preview.png"
    sheet.save(out, "PNG")
    print(f"wrote: {out}")
    print(f"size: {out.stat().st_size} bytes")
    print("Title variants contact sheet ready (gitignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
