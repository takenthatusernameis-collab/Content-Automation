#!/usr/bin/env python3
"""Generate a local preview PNG summarizing script quality signals.

Extracts spoken WORDS from script.md, counts anti-slop pattern hits,
digit tokens, and hedge phrases, and renders a 1280x720 overview card.
Output: packet/quality_overview_preview.png (gitignored).
No invented content, no external services. Reduces recurring human labor
of running quality_scan + claim_scan and reading text output just to
confirm quality status on every future packet. One command produces a
glanceable quality overview image.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Try to import shared helpers; fall back to local if running outside repo layout
try:
    from phrase_utils import ANTI_SLOP_PATTERNS, HEDGE_PATTERNS, spoken_words, compile_word_boundary_patterns
except ImportError:
    # Minimal fallback for standalone test
    ANTI_SLOP_PATTERNS = ["in today's video", "let's dive in", "without further ado"]
    HEDGE_PATTERNS = ["might", "could", "possibly", "approximately"]
    def spoken_words(text: str) -> str:
        return text
    def compile_word_boundary_patterns(pats):
        return [re.compile(r"\b" + re.escape(p) + r"\b", re.I) for p in pats]

WIDTH, HEIGHT = 1280, 720
BG = (18, 18, 22)
FG = (245, 243, 238)
ACCENT = (232, 196, 104)
MUTED = (140, 136, 130)
LINE = (58, 56, 52)
OK = (120, 180, 120)
WARN = (220, 140, 80)


def _font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    candidates = (
        f"/usr/share/fonts/truetype/dejavu/{name}",
        f"/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    )
    for p in candidates:
        if Path(p).is_file():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def count_anti_slop(body: str) -> list[tuple[str, int]]:
    res = compile_word_boundary_patterns(ANTI_SLOP_PATTERNS)
    hits = []
    for phrase, cre in zip(ANTI_SLOP_PATTERNS, res):
        count = len(list(cre.finditer(body)))
        if count:
            hits.append((phrase, count))
    return hits


def count_digits(body: str) -> int:
    return len(re.findall(r"\b\d+(?:\.\d+)?%?\b", body))


def count_hedges(body: str) -> list[tuple[str, int]]:
    res = compile_word_boundary_patterns(HEDGE_PATTERNS)
    hits = []
    for phrase, cre in zip(HEDGE_PATTERNS, res):
        count = len(list(cre.finditer(body)))
        if count:
            hits.append((phrase, count))
    return hits


def main() -> int:
    p = argparse.ArgumentParser(description="Generate local quality overview preview PNG")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    script = packet / "script.md"
    if not script.is_file():
        print("ERROR: script.md missing", file=sys.stderr)
        return 1

    text = script.read_text(encoding="utf-8")
    body = spoken_words(text)
    word_count = len(body.split()) if body else 0
    anti = count_anti_slop(body)
    digits = count_digits(body)
    hedges = count_hedges(body)
    anti_total = sum(c for _, c in anti)
    hedge_total = sum(c for _, c in hedges)
    issues = anti_total + (1 if digits else 0) + hedge_total  # simple signal count

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((20, 20, WIDTH - 20, HEIGHT - 20), outline=LINE, width=3)
    draw.text((40, 30), "QUALITY OVERVIEW", font=_font(28, bold=True), fill=ACCENT)

    status = "CLEAR" if issues == 0 else f"ISSUES ({issues})"
    status_color = OK if issues == 0 else WARN
    draw.text((40, 80), status, font=_font(36, bold=True), fill=status_color)

    y = 140
    draw.text((40, y), f"Spoken words: {word_count}", font=_font(22), fill=FG)
    y += 40
    draw.text((40, y), f"Anti-slop hits: {anti_total}", font=_font(22), fill=FG)
    y += 40
    draw.text((40, y), f"Digit tokens: {digits}", font=_font(22), fill=FG)
    y += 40
    draw.text((40, y), f"Hedge phrases: {hedge_total}", font=_font(22), fill=FG)

    y += 50
    draw.text((40, y), "Top signals (first few):", font=_font(18, bold=True), fill=MUTED)
    y += 30
    shown = 0
    for phrase, count in anti[:3]:
        draw.text((50, y), f"- {phrase} x{count}", font=_font(18), fill=FG)
        y += 28
        shown += 1
    for phrase, count in hedges[:2]:
        if shown >= 5:
            break
        draw.text((50, y), f"- hedge: {phrase} x{count}", font=_font(18), fill=FG)
        y += 28
        shown += 1
    if digits and shown < 5:
        draw.text((50, y), f"- digits present ({digits})", font=_font(18), fill=FG)

    draw.text((40, HEIGHT - 40), "Quality signals from spoken WORDS — gitignored preview (not a full scan)", font=_font(14), fill=MUTED)

    out = packet / "quality_overview_preview.png"
    img.save(out, "PNG")
    print(f"wrote: {out}")
    print(f"size: {out.stat().st_size} bytes")
    print(f"status: {status}")
    print("Quality overview preview ready (gitignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
