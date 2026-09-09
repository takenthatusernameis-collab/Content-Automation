#!/usr/bin/env python3
"""Create a video packet folder from the standard template."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "videos" / "_template"


def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:60] or "untitled"


def next_id(videos_dir: Path) -> str:
    highest = 0
    for p in videos_dir.iterdir():
        if not p.is_dir() or p.name.startswith("_"):
            continue
        m = re.match(r"^(?:sample-)?(\d+)", p.name)
        if m:
            highest = max(highest, int(m.group(1)))
    return f"{highest + 1:03d}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new video packet")
    parser.add_argument("title", help="Working title or topic")
    parser.add_argument("--id", help="Numeric id like 002 (default: next)")
    parser.add_argument(
        "--no-generate",
        action="store_true",
        help="Copy template only; do not write generated qa.md / research.md",
    )
    args = parser.parse_args()

    if not TEMPLATE.is_dir():
        print(f"Template missing: {TEMPLATE}", file=sys.stderr)
        return 1

    videos_dir = ROOT / "videos"
    vid = args.id or next_id(videos_dir)
    slug = slugify(args.title)
    dest = videos_dir / f"{vid}-{slug}"
    if dest.exists():
        print(f"Already exists: {dest}", file=sys.stderr)
        return 1

    shutil.copytree(TEMPLATE, dest)
    today = dt.date.today().isoformat()
    packet = dest / "packet.md"
    text = packet.read_text(encoding="utf-8")
    text = text.replace("- id:", f"- id: {vid}", 1)
    text = text.replace("- slug:", f"- slug: {slug}", 1)
    text = text.replace("- working_title:", f"- working_title: {args.title}", 1)
    text = text.replace("- created:", f"- created: {today}", 1)
    text = text.replace("- updated:", f"- updated: {today}", 1)
    packet.write_text(text, encoding="utf-8")
    print(dest.relative_to(ROOT))

    if not args.no_generate:
        sys.path.insert(0, str(ROOT / "tools"))
        from after_scaffold import generate

        for line in generate(dest, draft=True):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
