#!/usr/bin/env python3
"""Generate a local 1920x1080 captions preview PNG from packet captions.srt.

Parses SRT cues (index, timing, text) and renders a clean visual list of the
first ~15 cues with start times and truncated text. No invented claims.
Output is local only (gitignored). Reduces recurring human labor of scanning
the full SRT to review caption timing and text quality on every packet.
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


def parse_srt(text: str) -> list[dict]:
    """Parse SRT into list of {start, end, text}."""
    cues = []
    blocks = re.split(r"\n\s*\n", text.strip())
    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if len(lines) < 3:
            continue
        # Skip index
        timing = lines[1]
        m = re.match(r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})", timing)
        if not m:
            continue
        start, end = m.groups()
        text_lines = lines[2:]
        body = " ".join(text_lines).strip()
        if body:
            cues.append({"start": start, "end": end, "text": body})
    return cues


def _short_time(ts: str) -> str:
    """HH:MM:SS,mmm -> M:SS or MM:SS."""
    parts = ts.split(":")
    if len(parts) == 3:
        h, m, s_ms = parts
        s = s_ms.split(",")[0]
        total_m = int(h) * 60 + int(m)
        return f"{total_m}:{s.zfill(2)}"
    return ts


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
    srt_path = packet / "captions.srt"
    if not srt_path.is_file():
        raise FileNotFoundError(f"No captions.srt in {packet}")
    text = srt_path.read_text(encoding="utf-8")

    cues = parse_srt(text)
    if not cues:
        cues = [{"start": "00:00:00,000", "end": "00:00:01,000", "text": "No captions found"}]

    Image, ImageDraw, _ = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    title_font = _font(32)
    head_font = _font(18)
    body_font = _font(15)
    small_font = _font(14)

    # Header
    draw.text((40, 30), "CAPTIONS PREVIEW", fill=ACCENT, font=title_font)
    draw.text((40, 80), packet.name, fill=MUTED, font=small_font)
    draw.text((40, 110), f"{len(cues)} cues  |  first {min(15, len(cues))} shown from captions.srt", fill=MUTED, font=small_font)

    # List of first 15 cues
    y = 160
    draw.text((40, y), "First cues (timing + text for review):", fill=ACCENT, font=head_font)
    y += 36
    max_cues = 15
    for cue in cues[:max_cues]:
        start_short = _short_time(cue["start"])
        text_short = cue["text"][:120] + ("..." if len(cue["text"]) > 120 else "")
        line = f"{start_short}  {text_short}"
        lines = _wrap(draw, line, body_font, WIDTH - 120)
        for i, ln in enumerate(lines[:2]):
            draw.rectangle([40, y - 4, WIDTH - 40, y + 28], fill=PANEL_BG, outline=BORDER, width=1)
            draw.text((60, y), ln, fill=FG, font=body_font)
            y += 30
        y += 8
        if y > HEIGHT - 80:
            break

    if len(cues) > max_cues:
        draw.text((40, HEIGHT - 50), f"... and {len(cues) - max_cues} more cues (full file on disk)", fill=MUTED, font=small_font)

    out = out or (packet / "captions_preview.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG")
    return out


def main():
    p = argparse.ArgumentParser(description="Generate local captions preview PNG")
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
