#!/usr/bin/env python3
"""Generate a local 1920x1080 storyboard preview PNG from packet script.md.

Extracts main beats (Hook, Payoff, Beats, CTA) and renders short labels + first-sentence summaries
in a multi-panel grid. No invented claims. Output is local only (gitignored).
Reduces human labor of scanning the full script for structure overview on every packet.
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


def extract_beats(script_text: str) -> list[dict]:
    """Extract beat sections with titles and short summaries."""
    beats = []
    # Match ## Heading then content until next ##
    pattern = r"^##\s+(.+?)\s*\n(.*?)(?=^##|\Z)"
    for match in re.finditer(pattern, script_text, re.M | re.S):
        heading = match.group(1).strip()
        body = match.group(2).strip()
        # Prefer WORDS section
        words_match = re.search(r"WORDS:\s*\n(.*?)(?=\n\n|\nVISUAL:|\Z)", body, re.S)
        text = words_match.group(1).strip() if words_match else body
        # First sentence or first 90 chars
        first = re.split(r"[.!?]", text)[0].strip()
        summary = (first[:90] + "...") if len(first) > 90 else first
        if not summary:
            summary = heading[:60]
        beats.append({"heading": heading[:40], "summary": summary})
    # Limit to main ones: Hook, Payoff, numbered Beats, CTA
    main = []
    for b in beats:
        h = b["heading"].lower()
        if any(k in h for k in ("hook", "payoff", "beat", "cta", "end")):
            main.append(b)
    return main[:8]  # max 8 panels


def _pil():
    from PIL import Image, ImageDraw, ImageFont
    return Image, ImageDraw, ImageFont


def _font(size: int):
    Image, ImageDraw, ImageFont = _pil()
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
        beats = [{"heading": "Script", "summary": "No structured beats found"}]

    Image, ImageDraw, ImageFont = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    title_font = _font(36)
    head_font = _font(22)
    body_font = _font(16)

    # Header
    draw.text((40, 30), "STORYBOARD PREVIEW", fill=ACCENT, font=title_font)
    draw.text((40, 80), packet.name, fill=MUTED, font=body_font)

    # Grid: up to 2 rows x 4 cols
    n = len(beats)
    cols = min(4, n)
    rows = (n + cols - 1) // cols
    panel_w = (WIDTH - 80 - (cols - 1) * 20) // cols
    panel_h = (HEIGHT - 180 - (rows - 1) * 20) // max(rows, 1)

    for i, beat in enumerate(beats):
        r, c = divmod(i, cols)
        x = 40 + c * (panel_w + 20)
        y = 140 + r * (panel_h + 20)
        # Panel
        draw.rectangle([x, y, x + panel_w, y + panel_h], fill=PANEL_BG, outline=BORDER, width=2)
        # Heading
        draw.text((x + 12, y + 12), beat["heading"], fill=ACCENT, font=head_font)
        # Summary wrapped
        words = beat["summary"].split()
        lines = []
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if len(test) > 28:
                if line:
                    lines.append(line)
                line = w
            else:
                line = test
        if line:
            lines.append(line)
        for li, ln in enumerate(lines[:5]):
            draw.text((x + 12, y + 50 + li * 22), ln, fill=FG, font=body_font)

    out = out or (packet / "storyboard_preview.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG")
    return out


def main():
    p = argparse.ArgumentParser(description="Generate local storyboard preview PNG")
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
