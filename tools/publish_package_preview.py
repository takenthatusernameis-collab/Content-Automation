#!/usr/bin/env python3
"""Generate a local 1920x1080 publish-package preview PNG from packet publish.md.

Extracts locked title, description excerpt, tags, and first-comment candidate.
Renders them in a clean single-page layout for quick human review before upload.
No invented claims or text. Output is local only (gitignored).
Reduces recurring human labor of opening multiple sections to review the upload package.
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


def extract_section(text: str, heading: str) -> str:
    """Pull body under a ## Heading until the next ##."""
    pattern = rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##|\Z)"
    match = re.search(pattern, text, re.M | re.S)
    return match.group(1).strip() if match else ""


def extract_title(text: str) -> str:
    body = extract_section(text, "Title to upload")
    if body:
        return body.splitlines()[0].strip()
    return "Untitled"


def extract_description(text: str) -> str:
    body = extract_section(text, "Description")
    if not body:
        return ""
    # First ~280 chars, stop at double newline or end
    excerpt = body.split("\n\n")[0].strip()
    if len(excerpt) > 280:
        excerpt = excerpt[:277] + "..."
    return excerpt


def extract_tags(text: str) -> list[str]:
    body = extract_section(text, "Tags")
    tags = []
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("- "):
            tag = line[2:].strip()
            if tag and not tag.lower().startswith("removed"):
                tags.append(tag)
    return tags[:12]


def extract_first_comment(text: str) -> str:
    body = extract_section(text, "First comment (pin candidate)")
    if body:
        return body.splitlines()[0].strip()[:180]
    return ""


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
    publish_path = packet / "publish.md"
    if not publish_path.is_file():
        raise FileNotFoundError(f"No publish.md in {packet}")
    text = publish_path.read_text(encoding="utf-8")

    title = extract_title(text)
    desc = extract_description(text)
    tags = extract_tags(text)
    comment = extract_first_comment(text)

    Image, ImageDraw, _ = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    title_font = _font(32)
    head_font = _font(20)
    body_font = _font(16)
    small_font = _font(14)

    # Header
    draw.text((40, 30), "PUBLISH PACKAGE PREVIEW", fill=ACCENT, font=title_font)
    draw.text((40, 80), packet.name, fill=MUTED, font=small_font)

    y = 140
    # Title panel
    draw.rectangle([40, y, WIDTH - 40, y + 140], fill=PANEL_BG, outline=BORDER, width=2)
    draw.text((60, y + 16), "TITLE", fill=ACCENT, font=head_font)
    title_lines = _wrap(draw, title, _font(28), WIDTH - 160)
    ty = y + 50
    for line in title_lines[:2]:
        draw.text((60, ty), line, fill=FG, font=_font(28))
        ty += 36
    y += 160

    # Description panel
    draw.rectangle([40, y, WIDTH - 40, y + 280], fill=PANEL_BG, outline=BORDER, width=2)
    draw.text((60, y + 16), "DESCRIPTION (excerpt)", fill=ACCENT, font=head_font)
    desc_lines = _wrap(draw, desc, body_font, WIDTH - 160)
    dy = y + 50
    for line in desc_lines[:8]:
        draw.text((60, dy), line, fill=FG, font=body_font)
        dy += 24
    y += 300

    # Tags + First comment side-by-side
    col_w = (WIDTH - 100) // 2
    # Tags
    draw.rectangle([40, y, 40 + col_w, HEIGHT - 40], fill=PANEL_BG, outline=BORDER, width=2)
    draw.text((60, y + 16), "TAGS", fill=ACCENT, font=head_font)
    ty = y + 50
    for tag in tags[:10]:
        draw.text((60, ty), f"• {tag}", fill=FG, font=body_font)
        ty += 28
    # First comment
    draw.rectangle([60 + col_w, y, WIDTH - 40, HEIGHT - 40], fill=PANEL_BG, outline=BORDER, width=2)
    draw.text((80 + col_w, y + 16), "FIRST COMMENT", fill=ACCENT, font=head_font)
    comment_lines = _wrap(draw, comment, body_font, col_w - 80)
    cy = y + 50
    for line in comment_lines[:6]:
        draw.text((80 + col_w, cy), line, fill=FG, font=body_font)
        cy += 24

    out = out or (packet / "publish_package_preview.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG")
    return out


def main():
    p = argparse.ArgumentParser(description="Generate local publish-package preview PNG")
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
