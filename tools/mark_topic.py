#!/usr/bin/env python3
"""Mark a topic-queue row used only when a matching videos/ folder exists.

Dry-run by default. Does not scaffold packets. Does not invent WORDS.
"""

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


def existing_dirs() -> list[str]:
    if not VIDEOS.is_dir():
        return []
    names: list[str] = []
    for p in VIDEOS.iterdir():
        if p.is_dir() and not p.name.startswith("_"):
            names.append(p.name)
    return sorted(names)


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
                "raw": line,
            }
        )
    return rows


def match_folder(title: str, folders: list[str]) -> str | None:
    slug = slugify(title)
    for name in folders:
        lower = name.lower()
        if lower == slug or lower.endswith("-" + slug):
            return name
        m = re.match(r"^(?:sample-)?\d+-(.+)$", lower)
        if m and (m.group(1) == slug or slug in m.group(1)):
            return name
    return None


def rewrite_status(line: str, new_status: str) -> str:
    parts = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(parts) < 4:
        return line
    parts[1] = new_status
    return "| " + " | ".join(parts) + " |"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mark queue rows used when a videos/ folder exists (dry-run default)"
    )
    parser.add_argument(
        "--id",
        help="Queue id like Q1. Default: every queued row that already has a folder.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write docs/topic_queue.md. Without this flag, print the plan only.",
    )
    args = parser.parse_args()

    if not QUEUE.is_file():
        print(f"Missing queue: {QUEUE}", file=sys.stderr)
        return 1

    text = QUEUE.read_text(encoding="utf-8")
    rows = parse_queue(text)
    folders = existing_dirs()

    if args.id:
        target = [r for r in rows if r["id"].upper() == args.id.upper()]
        if not target:
            print(f"Unknown queue id: {args.id}", file=sys.stderr)
            return 1
        rows_to_check = target
    else:
        rows_to_check = [r for r in rows if r["status"] == "queued"]

    planned: list[tuple[dict[str, str], str]] = []
    blocked: list[str] = []
    for row in rows_to_check:
        folder = match_folder(row["working_title"], folders)
        if folder is None:
            blocked.append(
                f"{row['id']} still has no videos/ folder matching "
                f"{slugify(row['working_title'])!r}; not marking used."
            )
            continue
        if "sample-001" in folder:
            blocked.append(f"{row['id']} matched fixture {folder}; refuse.")
            continue
        if row["status"] == "used":
            blocked.append(f"{row['id']} already used (folder {folder}).")
            continue
        planned.append((row, folder))

    print("This command does not scaffold packets and does not invent WORDS.")
    print("Default is dry-run. Pass --write to change docs/topic_queue.md.")
    print(f"Existing packets: {', '.join(folders) or '(none)'}")
    for msg in blocked:
        print(f"Skip: {msg}")
    if not planned:
        print("No queue row is eligible to mark used.")
        return 0

    for row, folder in planned:
        print(f"Plan: {row['id']} queued -> used  (folder videos/{folder})")

    if not args.write:
        print("# after the dry-run looks right:")
        if args.id:
            print(f"# python3 tools/mark_topic.py --id {args.id} --write")
        else:
            print("# python3 tools/mark_topic.py --write")
        return 0

    new_text = text
    for row, folder in planned:
        new_line = rewrite_status(row["raw"], "used")
        if row["raw"] not in new_text:
            print(f"Could not find original line for {row['id']}", file=sys.stderr)
            return 1
        new_text = new_text.replace(row["raw"], new_line, 1)
        print(f"Wrote: {row['id']} used because videos/{folder} exists")

    QUEUE.write_text(new_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
