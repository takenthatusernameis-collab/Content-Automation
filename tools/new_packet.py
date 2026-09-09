#!/usr/bin/env python3
"""Create a video packet folder from the standard template."""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from queue_lib import matching_queue_row, next_id, parse_queue, slugify  # noqa: E402

TEMPLATE = ROOT / "videos" / "_template"
QUEUE = ROOT / "docs" / "topic_queue.md"


def mark_followup(title: str) -> list[str]:
    lines = [
        "This command does not mark the topic queue used.",
        "After the folder exists, dry-run mark_topic, then --write:",
    ]
    if not QUEUE.is_file():
        lines.append("  python3 tools/mark_topic.py")
        lines.append("  # python3 tools/mark_topic.py --write")
        return lines
    rows = parse_queue(QUEUE.read_text(encoding="utf-8"))
    row = matching_queue_row(title, rows)
    if row:
        lines.append(f"  python3 tools/mark_topic.py --id {row['id']}")
        lines.append(f"  # python3 tools/mark_topic.py --id {row['id']} --write")
    else:
        lines.append("  python3 tools/mark_topic.py")
        lines.append("  # python3 tools/mark_topic.py --write")
    return lines


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
        from after_scaffold import generate

        for line in generate(dest, draft=True):
            print(line)

    for line in mark_followup(args.title):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
