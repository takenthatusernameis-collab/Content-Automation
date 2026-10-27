#!/usr/bin/env python3
"""Generate a local preview PNG of the payoff promise from script.md.

Extracts the Payoff section WORDS block and renders it as a large, readable
text card PNG. Output: packet/payoff_preview.png (gitignored).
No invented content, no external services. Reduces recurring human labor of
scanning the script just to review the payoff promise on every future packet.
One command produces a glanceable payoff image.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 720
BG = (18, 18, 22)
FG = (245, 243, 238)
ACCENT = (120, 180, 220)
MUTED = (140, 136, 130)
LINE = (58, 56, 52)


def extract_payoff(script_text: str) -> str:
    """Extract the Payoff WORDS block."""
    payoff_match = re.search(
        r"^##\s+.*[Pp]ayoff.*?\n(.*?)(?=\n##|\Z)",
        script_text,
        re.M | re.S,
    )
    if payoff_match:
        section = payoff_match.group(1)
        words_match = re.search(
            r"^WORDS:\s*\n(.+?)(?=\n\n|\n##|\nVISUAL:|\Z)",
            section,
            re.M | re.S,
        )
        if words_match:
            payoff = words_match.group(1).strip()
            if payoff:
                return payoff
    return "No payoff promise found"


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
    p = argparse.ArgumentParser(description="Generate local payoff preview PNG")
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

    payoff = extract_payoff(script.read_text(encoding="utf-8"))
    print(f"payoff: {payoff[:80]}...")

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((20, 20, WIDTH - 20, HEIGHT - 20), outline=LINE, width=3)
    draw.text((40, 40), "PAYOFF PREVIEW", font=_font(22, bold=True), fill=ACCENT)

    font = _font(32)
    lines = _wrap(draw, payoff, font, WIDTH - 100)
    y = 100
    for line in lines[:9]:  # max 9 lines
        draw.text((50, y), line, font=font, fill=FG)
        bbox = font.getbbox(line or "X")
        y += (bbox[3] - bbox[1]) + 10

    draw.text((40, HEIGHT - 50), "Payoff WORDS from script.md \u2014 gitignored preview", font=_font(16), fill=MUTED)

    out = packet / "payoff_preview.png"
    img.save(out, "PNG")
    print(f"wrote: {out}")
    print(f"size: {out.stat().st_size} bytes")
    print("Payoff preview ready (gitignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
