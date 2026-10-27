#!/usr/bin/env python3
"""Generate a local 1920x1080 pacing timeline PNG from packet script.md.

Estimates segment durations at 150 wpm from WORDS under each beat.
Renders a horizontal timeline with labels, word counts, and cumulative times.
No invented claims. Output is local only (gitignored).
Reduces human labor of calculating and visualizing pacing for every packet.
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
WPM = 150.0

def extract_beats(script_text: str) -> list[dict]:
    """Extract beat sections with word counts."""
    beats = []
    pattern = r"^##\s+(.+?)\s*\n(.*?)(?=^##|\Z)"
    for match in re.finditer(pattern, script_text, re.M | re.S):
        heading = match.group(1).strip()
        body = match.group(2).strip()
        words_match = re.search(r"WORDS:\s*\n(.*?)(?=\n\n|\nVISUAL:|\Z)", body, re.S)
        text = words_match.group(1).strip() if words_match else ""
        words = re.findall(r"\b\w+\b", text)
        word_count = len(words)
        duration_s = (word_count / WPM) * 60.0 if word_count else 8.0
        beats.append({
            "heading": heading[:36],
            "words": word_count,
            "duration": duration_s,
            "text_preview": text[:40] + "..." if len(text) > 40 else text,
        })
    return [b for b in beats if b["words"] > 0 or "hook" in b["heading"].lower() or "cta" in b["heading"].lower()]

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
    script_path = packet / "script.md"
    if not script_path.exists():
        raise FileNotFoundError(f"No script.md in {packet}")
    script_text = script_path.read_text(encoding="utf-8")
    beats = extract_beats(script_text)
    if not beats:
        beats = [{"heading": "Script", "words": 0, "duration": 60.0, "text_preview": "No beats"}]

    total_duration = sum(b["duration"] for b in beats)
    total_words = sum(b["words"] for b in beats)

    Image, ImageDraw, _ = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    title_font = _font(36)
    head_font = _font(18)
    body_font = _font(14)

    # Header
    draw.text((40, 30), "PACING TIMELINE", fill=ACCENT, font=title_font)
    draw.text((40, 80), f"{packet.name}  |  ~{total_words} words  |  ~{total_duration/60:.1f} min at {WPM:.0f} wpm", fill=MUTED, font=body_font)

    # Timeline bar
    bar_y = 160
    bar_h = 80
    bar_x0 = 60
    bar_x1 = WIDTH - 60
    draw.rectangle([bar_x0, bar_y, bar_x1, bar_y + bar_h], fill=PANEL_BG, outline=BORDER, width=2)

    # Segments
    x = bar_x0
    usable = bar_x1 - bar_x0
    cumulative = 0.0
    for i, beat in enumerate(beats):
        frac = beat["duration"] / total_duration if total_duration else 1.0 / len(beats)
        seg_w = max(40, usable * frac)
        color = BAR if i % 2 == 0 else (50, 90, 140)
        draw.rectangle([x, bar_y + 4, x + seg_w - 2, bar_y + bar_h - 4], fill=color)
        # Label above
        label = beat["heading"][:20]
        draw.text((x + 4, bar_y - 28), label, fill=FG, font=head_font)
        # Time below
        cum_str = f"{int(cumulative//60)}:{int(cumulative%60):02d}"
        draw.text((x + 4, bar_y + bar_h + 8), cum_str, fill=MUTED, font=body_font)
        x += seg_w
        cumulative += beat["duration"]

    # Detail list
    y = 320
    draw.text((40, y), "Segments (estimated):", fill=ACCENT, font=head_font)
    y += 40
    for beat in beats:
        line = f"{beat['heading'][:28]:<30}  {beat['words']:>4}w  ~{beat['duration']:.0f}s"
        draw.text((60, y), line, fill=FG, font=body_font)
        y += 28
        if y > HEIGHT - 60:
            break

    out = out or (packet / "pacing_timeline.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG")
    return out

def main():
    p = argparse.ArgumentParser(description="Generate local pacing timeline PNG")
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
