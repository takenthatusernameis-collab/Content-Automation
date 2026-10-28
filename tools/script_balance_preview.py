#!/usr/bin/env python3
"""Generate a local preview PNG of script structure balance.

Extracts spoken WORDS per standard section (Hook, Body, Payoff, CTA) from script.md,
counts words, estimates duration at 150 wpm, and renders a 1280x720 balance card
with percentage bars.
Output: packet/script_balance_preview.png (gitignored).
No invented content, no external services. Reduces recurring human labor of
manually counting words per section and calculating pacing balance on every
future packet. One command produces a glanceable structure balance image.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

try:
    from phrase_utils import spoken_words
except ImportError:
    def spoken_words(text: str) -> str:
        return text

WIDTH, HEIGHT = 1280, 720
BG = (18, 18, 22)
FG = (245, 243, 238)
ACCENT = (232, 196, 104)
MUTED = (140, 136, 130)
LINE = (58, 56, 52)
OK = (120, 180, 120)
BAR = (80, 140, 200)

SECTIONS = ["Hook", "Body", "Payoff", "CTA"]
WPM = 150


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


def extract_section_words(text: str) -> dict[str, str]:
    """Rough extract of WORDS under common section headers."""
    sections: dict[str, str] = {s: "" for s in SECTIONS}
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("##"):
            header = stripped.lstrip("#").strip().lower()
            for s in SECTIONS:
                if s.lower() in header:
                    current = s
                    break
            else:
                current = None
            continue
        if current and (stripped.startswith("WORDS") or not stripped):
            continue
        if current:
            sections[current] += line + "\n"
    # Prefer spoken_words on whole if sections empty
    if not any(sections.values()):
        body = spoken_words(text)
        sections["Body"] = body
    else:
        for s in SECTIONS:
            if sections[s]:
                sections[s] = spoken_words(sections[s])
    return sections


def main() -> int:
    p = argparse.ArgumentParser(description="Generate local script balance preview PNG")
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
    secs = extract_section_words(text)
    counts = {s: len(secs[s].split()) if secs[s] else 0 for s in SECTIONS}
    total = sum(counts.values()) or 1
    est_sec = {s: round(counts[s] / WPM * 60) for s in SECTIONS}
    total_sec = sum(est_sec.values())

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((20, 20, WIDTH - 20, HEIGHT - 20), outline=LINE, width=3)
    draw.text((40, 30), "SCRIPT STRUCTURE BALANCE", font=_font(28, bold=True), fill=ACCENT)

    draw.text((40, 80), f"Total spoken words: {total}  |  Est. duration: {total_sec}s ({total_sec//60}:{total_sec%60:02d})", font=_font(20), fill=FG)

    y = 140
    bar_max = 800
    for s in SECTIONS:
        pct = counts[s] / total * 100
        bar_w = int(bar_max * counts[s] / total)
        draw.text((40, y), f"{s}: {counts[s]} words ({pct:.0f}%) ~{est_sec[s]}s", font=_font(20), fill=FG)
        draw.rectangle((40, y + 28, 40 + bar_w, y + 48), fill=BAR)
        y += 70

    draw.text((40, HEIGHT - 50), "Estimates at 150 wpm from section WORDS — gitignored preview (structure aid, not a rewrite)", font=_font(14), fill=MUTED)

    out = packet / "script_balance_preview.png"
    img.save(out, "PNG")
    print(f"wrote: {out}")
    print(f"size: {out.stat().st_size} bytes")
    print(f"total_words: {total}")
    print(f"est_duration_s: {total_sec}")
    print("Script balance preview ready (gitignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
