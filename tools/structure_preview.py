#!/usr/bin/env python3
"""Generate a local preview PNG of script structure and word counts.

Extracts ## sections and spoken-word counts from script.md WORDS blocks and
renders a readable outline card. Highlights SHORT/OK/LONG relative to
explainer targets. Output: packet/structure_preview.png (gitignored).
No invented content. Reduces recurring human labor of opening the script
or running words.py just to review beat structure and lengths on every packet.
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
OK = (120, 180, 120)
SHORT = (220, 140, 80)
LONG = (200, 120, 120)

# Approximate targets for explainer-6-10min
TARGETS = {
    "hook": (20, 35),
    "payoff": (40, 70),
    "beat": (140, 220),
    "cta": (40, 80),
}


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


def spoken_words_in_section(text: str) -> str:
    m = re.search(r"^WORDS:\s*\n(.*?)(?=\n\n|\n##|\nVISUAL:|\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def classify(section: str, count: int) -> str:
    key = "beat"
    low = section.lower()
    if "hook" in low:
        key = "hook"
    elif "payoff" in low:
        key = "payoff"
    elif "cta" in low:
        key = "cta"
    lo, hi = TARGETS.get(key, (0, 9999))
    if count < lo:
        return "SHORT"
    if count > hi:
        return "LONG"
    return "OK"


def extract_sections(script: str) -> list[tuple[str, int, str]]:
    parts = re.split(r"(^## .+)$", script, flags=re.M)
    sections = []
    current_title = None
    current_body = ""
    for part in parts:
        if part.startswith("## "):
            if current_title is not None:
                words = spoken_words_in_section(current_body)
                count = len(words.split()) if words else 0
                status = classify(current_title, count)
                sections.append((current_title.strip(), count, status))
            current_title = part
            current_body = ""
        else:
            current_body += part
    if current_title is not None:
        words = spoken_words_in_section(current_body)
        count = len(words.split()) if words else 0
        status = classify(current_title, count)
        sections.append((current_title.strip(), count, status))
    return sections[:10]  # max 10 rows


def main() -> int:
    p = argparse.ArgumentParser(description="Generate structure overview PNG from script.md")
    p.add_argument("packet", type=Path)
    args = p.parse_args()

    packet = args.packet.resolve()
    script_path = packet / "script.md"
    if not script_path.is_file():
        print(f"ERROR: no script.md in {packet}", file=sys.stderr)
        return 1

    text = script_path.read_text(encoding="utf-8")
    sections = extract_sections(text)
    if not sections:
        print("ERROR: no ## sections found", file=sys.stderr)
        return 1

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    title_f = _font(36, bold=True)
    sub_f = _font(20)
    row_f = _font(22)
    small_f = _font(16)

    draw.text((40, 30), "SCRIPT STRUCTURE", fill=ACCENT, font=title_f)
    draw.text((40, 80), f"Packet: {packet.name}", fill=MUTED, font=sub_f)
    draw.line((40, 120, WIDTH - 40, 120), fill=LINE, width=2)

    y = 150
    for title, count, status in sections:
        color = OK if status == "OK" else SHORT if status == "SHORT" else LONG
        status_str = f"[{status}]"
        draw.text((40, y), title[:55], fill=FG, font=row_f)
        draw.text((700, y), f"{count:4d} words", fill=FG, font=row_f)
        draw.text((920, y), status_str, fill=color, font=row_f)
        y += 48
        if y > HEIGHT - 80:
            break

    total = sum(c for _, c, _ in sections)
    draw.text((40, HEIGHT - 50), f"Total spoken ~{total} words   (targets: hook 20-35, payoff 40-70, beats 140-220, CTA 40-80)", fill=MUTED, font=small_f)

    out = packet / "structure_preview.png"
    img.save(out, "PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes) — {len(sections)} sections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
