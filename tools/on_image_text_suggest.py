#!/usr/bin/env python3
"""Suggest concise on-image text for YouTube thumbnails from the locked title.

Uses phrase_utils.shorten to produce a natural short phrase (<= ~5 words / 40 chars)
suitable for on-image readability and CTR. Does not invent new claims or text.
Prints the suggested On-image text line and whether thumbnail.md already has a short one.
Optionally --write updates the On-image text line in thumbnail.md if missing or longer.
Local text only. No media, no secrets, no packet content invention.
Reduces recurring human labor of manually shortening titles for thumbnail text on every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Import shared shorten so suggestions stay consistent with other tools.
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from phrase_utils import shorten
except ImportError:
    def shorten(text: str, max_len: int = 40) -> str:
        words = text.split()
        return " ".join(words[:5]) if len(words) > 5 else text


def extract_title(publish_text: str) -> str:
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


def extract_on_image(thumb_text: str) -> str | None:
    match = re.search(
        r"On-image text(?: \(max 5 words\))?:\s*(.+)",
        thumb_text,
        re.I,
    )
    if match:
        text = match.group(1).strip()
        return text if text else None
    return None


def suggest_short(title: str) -> str:
    # Prefer <=5 words or ~40 chars for thumbnail readability
    short = shorten(title, max_len=40)
    words = short.split()
    if len(words) > 5:
        short = " ".join(words[:5])
    return short.strip()


def update_thumbnail_md(thumb_path: Path, short_text: str) -> bool:
    """Update or insert the On-image text line. Returns True if changed."""
    if not thumb_path.is_file():
        content = f"# Thumbnail\n\nOn-image text (max 5 words): {short_text}\n"
        thumb_path.write_text(content, encoding="utf-8")
        return True
    text = thumb_path.read_text(encoding="utf-8")
    current = extract_on_image(text)
    if current and len(current.split()) <= 6 and current == short_text:
        return False  # already good
    # Replace existing line or insert after header
    new_line = f"On-image text (max 5 words): {short_text}"
    if current is not None:
        text = re.sub(
            r"On-image text(?: \(max 5 words\))?:.*",
            new_line,
            text,
            count=1,
            flags=re.I,
        )
    else:
        # Insert after first heading or at top
        if text.startswith("#"):
            text = re.sub(r"(# Thumbnail\s*\n+)", r"\1" + new_line + "\n\n", text, count=1)
        else:
            text = new_line + "\n\n" + text
    thumb_path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    p = argparse.ArgumentParser(
        description="Suggest short on-image text from title for better thumbnail CTR"
    )
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    p.add_argument("--write", action="store_true", help="Update thumbnail.md with the suggested short text if needed")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    publish = packet / "publish.md"
    if not publish.is_file():
        print("ERROR: publish.md missing", file=sys.stderr)
        return 1

    title = extract_title(publish.read_text(encoding="utf-8"))
    short = suggest_short(title)

    thumb_md = packet / "thumbnail.md"
    current = None
    if thumb_md.is_file():
        current = extract_on_image(thumb_md.read_text(encoding="utf-8"))

    print(f"packet: {packet.name}")
    print(f"title: {title}")
    print(f"suggested on-image text: {short}")
    if current:
        print(f"current on-image: {current} ({len(current.split())} words)")
        if len(current.split()) <= 6:
            print("status: already short (no change needed)")
        else:
            print("status: current is long; suggest replacing with short version")
    else:
        print("status: no on-image text found; suggest adding")

    if args.write:
        changed = update_thumbnail_md(thumb_md, short)
        if changed:
            print(f"updated: {thumb_md.name}")
        else:
            print("no write needed (already suitable)")

    print("\nUse the short text in thumbnail.md for thumbnail_generator.py / thumbnail_variants.py preference.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
