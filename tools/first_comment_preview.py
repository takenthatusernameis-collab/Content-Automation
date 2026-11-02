#!/usr/bin/env python3
"""Generate a local preview PNG of the first-comment text.

Prefers ranked First comment text from recommended_publish_fill.md when present
(compounding the metadata ranking/fill work); falls back to publish.md first-comment
section when available. Renders a large, readable text card PNG.
Output: packet/first_comment_preview.png (gitignored).
No invented content, no external services. Reduces recurring human labor of
opening publish.md just to review the pinned first comment on every future packet.
One command produces a glanceable first-comment image aligned with selected metadata
when the fill file exists.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from phrase_utils import extract_recommended_first_comment

WIDTH, HEIGHT = 1280, 720
BG = (18, 18, 22)
FG = (245, 243, 238)
ACCENT = (232, 196, 104)
MUTED = (140, 136, 130)
LINE = (58, 56, 52)


def extract_first_comment_from_publish(publish_text: str) -> str | None:
    """Pull first-comment body from publish.md if present."""
    match = re.search(
        r"^##\s+First comment(?:\s+to (?:post|pin))?\s*\n(.+?)(?:\n##|\n\n\n|\Z)",
        publish_text,
        re.M | re.S | re.I,
    )
    if match:
        text = match.group(1).strip()
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()
        text = re.sub(r"^(Text|Comment|Body)\s*:\s*", "", text, flags=re.I).strip()
        if text and len(text.split()) >= 4:
            return text
    return None


def _font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    candidates = (
        f"/usr/share/fonts/truetype/dejavu/{name}",
        (
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
        ),
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
    p = argparse.ArgumentParser(
        description="Generate local first-comment preview PNG preferring ranked fill"
    )
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    text = None
    source = "none"
    fill_path = packet / "recommended_publish_fill.md"
    if fill_path.is_file():
        rec = extract_recommended_first_comment(fill_path.read_text(encoding="utf-8"))
        if rec:
            text = rec
            source = "recommended-fill"

    if not text:
        publish = packet / "publish.md"
        if publish.is_file():
            text = extract_first_comment_from_publish(publish.read_text(encoding="utf-8"))
            if text:
                source = "publish"

    if not text:
        print(
            "ERROR: no first-comment text (need recommended_publish_fill.md or publish.md)",
            file=sys.stderr,
        )
        return 1

    print(f"packet: {packet.name}")
    print(f"first_comment source: {source}")
    preview = text if len(text) <= 100 else text[:97] + "..."
    print(f"first_comment: {preview}")

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((20, 20, WIDTH - 20, HEIGHT - 20), outline=LINE, width=3)
    draw.text((40, 40), "FIRST COMMENT PREVIEW", font=_font(22, bold=True), fill=ACCENT)

    font = _font(32)
    lines = _wrap(draw, text, font, WIDTH - 100)
    y = 100
    for line in lines[:10]:
        draw.text((50, y), line, font=font, fill=FG)
        bbox = font.getbbox(line or "X")
        y += (bbox[3] - bbox[1]) + 10

    footer = "First comment from recommended fill or publish.md — gitignored preview"
    draw.text((40, HEIGHT - 50), footer, font=_font(16), fill=MUTED)

    out = packet / "first_comment_preview.png"
    img.save(out, "PNG")
    print(f"wrote: {out}")
    print(f"size: {out.stat().st_size} bytes")
    print("First comment preview ready (gitignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
