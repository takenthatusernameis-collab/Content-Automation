#!/usr/bin/env python3
"""Generate a local preview PNG of the hook text from script.md.

Extracts the first WORDS: block (the hook) and renders it as a large, readable
text card PNG. Output: packet/hook_preview.png (gitignored).
No invented content, no external services. Reduces recurring human labor of
opening the script just to review the opening hook on every future packet.
One command produces a glanceable hook image.
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
    """Extract the first WORDS: block (hook)."""
    # Look for first WORDS: followed by text until blank line or next header
    match = re.search(
        r"^WORDS:\s*\n(.+?)(?=\n\n|\n##|\nVISUAL:|\Z)",
        script_text,
        re.M | re.S,
    )
    if match:
        hook = match.group(1).strip()
        if hook:
            return hook
    # Fallback: first non-empty paragraph after Hook header
    lines = script_text.splitlines()
    in_hook = False
    collected = []
    for line in lines:
        if "hook" in line.lower() and line.startswith("#"):
            in_hook = True
            continue
        if in_hook and line.strip().startswith("WORDS:"):
            continue
        if in_hook and line.strip() and not line.startswith("#") and not line.strip().startswith("*"):
            collected.append(line.strip())
            if len(collected) >= 3:
                break
        if in_hook and not line.strip() and collected:
            break
    return " ".join(collected) if collected else "No hook found"


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


def main() -> int:
    p = argparse.ArgumentParser(description="Generate local hook preview PNG")
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

    hook = extract_hook(script.read_text(encoding="utf-8"))
    print(f"hook: {hook[:80]}...")

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((20, 20, WIDTH - 20, HEIGHT - 20), outline=LINE, width=3)
    draw.text((40, 40), "HOOK PREVIEW", font=_font(22, bold=True), fill=ACCENT)

    font = _font(36)
    lines = _wrap(draw, hook, font, WIDTH - 100)
    y = 100
    for line in lines[:8]:  # max 8 lines
        draw.text((50, y), line, font=font, fill=FG)
        bbox = font.getbbox(line or "X")
        y += (bbox[3] - bbox[1]) + 12

    draw.text((40, HEIGHT - 50), "First WORDS block from script.md — gitignored preview", font=_font(16), fill=MUTED)

    out = packet / "hook_preview.png"
    img.save(out, "PNG")
    print(f"wrote: {out}")
    print(f"size: {out.stat().st_size} bytes")
    print("Hook preview ready (gitignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
