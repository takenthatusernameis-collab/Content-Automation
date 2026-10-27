#!/usr/bin/env python3
"""Generate a local preview PNG of the three key moments from script.md.

Extracts the first WORDS (Hook), the Payoff section WORDS, and the CTA WORDS
and renders them stacked on a single 1280x720 card. Output: packet/key_moments_preview.png (gitignored).
No invented content, no external services. Reduces recurring human labor of
checking three separate previews or scrolling the script just to review the
critical retention points (open, promise, close) on every future packet.
One command produces a glanceable key-moments image.
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
ACCENT = (232, 196, 104)
MUTED = (140, 136, 130)
LINE = (58, 56, 52)


def extract_hook(script_text: str) -> str:
    match = re.search(
        r"^WORDS:\s*\n(.+?)(?=\n\n|\n##|\nVISUAL:|\Z)",
        script_text,
        re.M | re.S,
    )
    if match:
        return match.group(1).strip()
    return "No hook found"


def extract_payoff(script_text: str) -> str:
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
            return words_match.group(1).strip()
    return "No payoff found"


def extract_cta(script_text: str) -> str:
    cta_match = re.search(
        r"^##\s+.*[Cc][Tt][Aa].*?\n(.*?)(?=\n##|\Z)",
        script_text,
        re.M | re.S,
    )
    if cta_match:
        section = cta_match.group(1)
        words_match = re.search(
            r"^WORDS:\s*\n(.+?)(?=\n\n|\n##|\nVISUAL:|\Z)",
            section,
            re.M | re.S,
        )
        if words_match:
            return words_match.group(1).strip()
    matches = list(re.finditer(
        r"^WORDS:\s*\n(.+?)(?=\n\n|\n##|\nVISUAL:|\Z)",
        script_text,
        re.M | re.S,
    ))
    if matches:
        return matches[-1].group(1).strip()
    return "No CTA found"


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


def draw_section(draw, title: str, text: str, y_start: int, max_lines: int = 4) -> int:
    draw.text((40, y_start), title, font=_font(20, bold=True), fill=ACCENT)
    font = _font(22)
    lines = _wrap(draw, text, font, WIDTH - 100)
    y = y_start + 30
    for line in lines[:max_lines]:
        draw.text((50, y), line, font=font, fill=FG)
        bbox = font.getbbox(line or "X")
        y += (bbox[3] - bbox[1]) + 6
    return y + 10


def main() -> int:
    p = argparse.ArgumentParser(description="Generate local key moments preview PNG")
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
    hook = extract_hook(text)
    payoff = extract_payoff(text)
    cta = extract_cta(text)
    print(f"hook: {hook[:60]}...")
    print(f"payoff: {payoff[:60]}...")
    print(f"cta: {cta[:60]}...")

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((20, 20, WIDTH - 20, HEIGHT - 20), outline=LINE, width=3)
    draw.text((40, 30), "KEY MOMENTS PREVIEW", font=_font(24, bold=True), fill=ACCENT)

    y = 70
    y = draw_section(draw, "HOOK", hook, y)
    y = draw_section(draw, "PAYOFF", payoff, y)
    y = draw_section(draw, "CTA", cta, y)

    draw.text((40, HEIGHT - 40), "Hook + Payoff + CTA WORDS from script.md — gitignored preview", font=_font(14), fill=MUTED)

    out = packet / "key_moments_preview.png"
    img.save(out, "PNG")
    print(f"wrote: {out}")
    print(f"size: {out.stat().st_size} bytes")
    print("Key moments preview ready (gitignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
