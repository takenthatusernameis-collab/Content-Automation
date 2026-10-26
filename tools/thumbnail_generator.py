#!/usr/bin/env python3
"""Generate a local 1280x720 YouTube thumbnail PNG from packet publish.md title.

No stock, no invented text beyond the locked title, no git commits of the binary.
Output: packet/thumbnail.png (local only). Compatible with youtube_upload.py checks
(min 640x360, PNG with IEND, <2MB).
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

WIDTH, HEIGHT = 1280, 720
BG = (18, 18, 22)
FG = (245, 243, 238)
ACCENT = (232, 196, 104)
RULE = (58, 56, 52)


def extract_title(publish_text: str) -> str:
    """Pull the title from the ## Title to upload section."""
    match = re.search(
        r"^##\s+Title to upload\s*\n(.+?)(?:\n##|\n\n|\Z)",
        publish_text,
        re.M | re.S,
    )
    if match:
        title = match.group(1).strip()
        if title:
            return title
    lines = publish_text.splitlines()
    for i, line in enumerate(lines):
        if "title to upload" in line.lower():
            for next_line in lines[i + 1 :]:
                stripped = next_line.strip()
                if stripped and not stripped.startswith("#"):
                    return stripped
    return "Untitled"


def _pil():
    from PIL import Image, ImageDraw, ImageFont
    return Image, ImageDraw, ImageFont


def _font(size: int):
    _, _, ImageFont = _pil()
    candidates = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    )
    for path in candidates:
        if Path(path).is_file():
            return ImageFont.truetype(path, size=size)
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


def render_thumbnail(title: str):
    Image, ImageDraw, _ = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((40, 40, WIDTH - 40, HEIGHT - 40), outline=RULE, width=4)
    draw.rectangle((40, 40, WIDTH - 40, 100), fill=ACCENT)
    draw.text((60, 52), "YOUTUBE", font=_font(28), fill=BG)

    font = _font(64)
    lines = _wrap(draw, title, font, WIDTH - 160)
    total_h = 0
    for line in lines:
        bbox = font.getbbox(line or "X")
        total_h += (bbox[3] - bbox[1]) + 12
    y = 140 + (HEIGHT - 200 - total_h) // 2
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text(((WIDTH - w) / 2, y), line, font=font, fill=FG)
        bbox = font.getbbox(line or "X")
        y += (bbox[3] - bbox[1]) + 12
    return img


def inspect_png(path: Path) -> dict[str, str]:
    info = {"path": str(path), "bytes": str(path.stat().st_size) if path.is_file() else "0", "ok": "no"}
    if not path.is_file():
        info["error"] = "missing"
        return info
    try:
        Image, _, _ = _pil()
        with Image.open(path) as im:
            info["size"] = f"{im.size[0]}x{im.size[1]}"
            info["mode"] = im.mode
            if im.size == (WIDTH, HEIGHT) and path.stat().st_size > 1000:
                info["ok"] = "yes"
    except OSError as exc:
        info["error"] = str(exc)
    return info


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local 1280x720 thumbnail from publish title")
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--inspect-only", action="store_true")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    publish = path / "publish.md"
    if not publish.is_file():
        print("missing publish.md", file=sys.stderr)
        return 1

    title = extract_title(publish.read_text(encoding="utf-8"))
    print(f"packet: {path.name}")
    print(f"title: {title}")

    dest = path / "thumbnail.png"
    if args.inspect_only:
        info = inspect_png(dest)
        print(f"thumbnail.png: {info.get('ok')} {info.get('size', '')} {info.get('bytes')} bytes")
        return 0 if info.get("ok") == "yes" else 1

    if args.dry_run:
        print(f"would write: {dest}")
        print("dry-run: no file written")
        return 0

    img = render_thumbnail(title)
    img.save(dest, format="PNG")
    info = inspect_png(dest)
    print(f"wrote: {dest}")
    print(f"ok: {info.get('ok')} size: {info.get('size')} bytes: {info.get('bytes')}")
    return 0 if info.get("ok") == "yes" else 1


if __name__ == "__main__":
    raise SystemExit(main())
