#!/usr/bin/env python3
"""Print the next queued topic and the scaffold commands. Read-only."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "docs" / "topic_queue.md"
VIDEOS = ROOT / "videos"


def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:60] or "untitled"


def next_id(videos_dir: Path) -> str:
    highest = 0
    if videos_dir.is_dir():
        for p in videos_dir.iterdir():
            if not p.is_dir() or p.name.startswith("_"):
                continue
            m = re.match(r"^(?:sample-)?(\d+)", p.name)
            if m:
                highest = max(highest, int(m.group(1)))
    return f"{highest + 1:03d}"


def existing_slugs() -> set[str]:
    found: set[str] = set()
    if not VIDEOS.is_dir():
        return found
    for p in VIDEOS.iterdir():
        if not p.is_dir() or p.name.startswith("_"):
            continue
        found.add(p.name.lower())
        m = re.match(r"^(?:sample-)?\d+-(.+)$", p.name)
        if m:
            found.add(m.group(1).lower())
    return found


def parse_queue(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.startswith("| Q"):
            continue
        parts = [c.strip() for c in line.strip("|").split("|")]
        if len(parts) < 4:
            continue
        rows.append(
            {
                "id": parts[0],
                "status": parts[1].lower(),
                "working_title": parts[2],
                "one_line": parts[3],
            }
        )
    return rows


def already_used(title: str, slugs: set[str]) -> bool:
    slug = slugify(title)
    if slug in slugs:
        return True
    for existing in slugs:
        if slug and slug in existing:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print the next queued topic (read-only; does not scaffold)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Print every queued row that is not already a packet",
    )
    args = parser.parse_args()

    if not QUEUE.is_file():
        print(f"Missing queue: {QUEUE}", file=sys.stderr)
        return 1

    rows = parse_queue(QUEUE.read_text(encoding="utf-8"))
    slugs = existing_slugs()
    available = [
        r
        for r in rows
        if r["status"] == "queued" and not already_used(r["working_title"], slugs)
    ]

    print("This command writes nothing.")
    print("Queue file: docs/topic_queue.md")
    print(f"Queued unused: {len(available)} / {len(rows)}")
    if not available:
        print("No unused queued topic. Add a row to docs/topic_queue.md or reuse an existing packet.")
        return 0

    predicted_id = next_id(VIDEOS)
    show = available if args.all else available[:1]
    for i, row in enumerate(show):
        title = row["working_title"]
        slug = slugify(title)
        vid = f"{int(predicted_id) + i:03d}" if args.all else predicted_id
        dest = f"videos/{vid}-{slug}"
        print(f"Next: {row['id']} — {title}")
        print(f"One-line: {row['one_line']}")
        print(f"Predicted path: {dest}")
        print("Scaffold (human / instructed agent only; not the fixture):")
        print(f'  python3 tools/new_packet.py "{title}"')
        print(f'  python3 tools/new_idea.py "{row["one_line"]}"')
        print(f"  python3 tools/doctor.py {dest}")
        print("After the folder exists (dry-run first):")
        print(f"  python3 tools/mark_topic.py --id {row['id']}")
        print(f"  # python3 tools/mark_topic.py --id {row['id']} --write")
        print("Do not apply WORDS to sample-001. Do not invent a script here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
