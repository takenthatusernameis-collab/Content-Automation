#!/usr/bin/env python3
"""Draft a 1280x720 thumbnail PNG from thumbnail.md on-image text.

Not an approval. Does not check boxes. Does not call thumbnails.set.
Missing or over-long on-image text refuses. A generated card is not a design sign-off.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

WIDTH = 1280
HEIGHT = 720
BG = (28, 25, 23)
INK = (245, 240, 230)
ACCENT = (196, 122, 66)
MAX_WORDS = 5
TEXT_RE = re.compile(r"^On-image text(?:\s*\([^)]*\))?\s*:\s*(.+)$", re.M)


def _pil():
    from PIL import Image, ImageDraw, ImageFont

    return Image, ImageDraw, ImageFont


def _font(size: int):
    _, _, ImageFont = _pil()
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(path).is_file():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def on_image_text(text: str) -> str:
    match = TEXT_RE.search(text)
    if not match:
        raise SystemExit("REFUSE: thumbnail on-image text missing")
    line = match.group(1).strip()
    words = line.split()
    if not words:
        raise SystemExit("REFUSE: thumbnail on-image text missing")
    if len(words) > MAX_WORDS:
        raise SystemExit(f"REFUSE: thumbnail text has {len(words)} words, max {MAX_WORDS}")
    return line


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def render_png(label: str):
    Image, ImageDraw, _ImageFont = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, WIDTH, 18), fill=ACCENT)
    small = _font(28)
    draw.text((48, 48), "GENERATED DRAFT", fill=ACCENT, font=small)
    font = _font(92)
    words = label.split()
    lines = [" ".join(words[:3])]
    if len(words) > 3:
        lines.append(" ".join(words[3:]))
    y = 230
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        width = bbox[2] - bbox[0]
        draw.text(((WIDTH - width) / 2, y), line, fill=INK, font=font)
        y += 120
    return img


def review_text(packet: Path, label: str, sha: str) -> str:
    return (
        "# Thumbnail review\n\n"
        "Generated draft. Not an approval. Not uploaded.\n"
        "thumbnails.set is not called. An agent must not check the design box.\n\n"
        f"- Packet: `{packet.name}`\n"
        f"- File: `thumbnail.png`\n"
        f"- Size: {WIDTH}x{HEIGHT}\n"
        f"- On-image text: {label}\n"
        f"- SHA256: `{sha}`\n"
        "- approval: false\n\n"
        "Human check (do not treat this file as the check):\n"
        "- readable on a phone-sized crop\n"
        "- contrast holds without the GENERATED DRAFT label\n"
        "- text matches the locked title promise\n"
    )


def build(packet: Path) -> dict:
    brief = packet / "thumbnail.md"
    if not brief.is_file():
        raise SystemExit("REFUSE: thumbnail.md missing")
    label = on_image_text(brief.read_text(encoding="utf-8"))
    img = render_png(label)
    dest = packet / "thumbnail.png"
    img.save(dest, format="PNG")
    sha = _sha256(dest)
    (packet / "thumbnail_review.md").write_text(review_text(packet, label, sha), encoding="utf-8")
    return {
        "label": label,
        "words": len(label.split()),
        "width": WIDTH,
        "height": HEIGHT,
        "sha256": sha,
        "approval": False,
        "uploaded": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Draft a thumbnail PNG from thumbnail.md")
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    info = build(args.packet)
    print(
        "THUMBNAIL_DRAFT "
        f"words={info['words']} size={info['width']}x{info['height']} "
        f"approval={info['approval']} uploaded={info['uploaded']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
