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

try:
    from operator_pin_contract import Q1_PROBLEM  # noqa: E402
except Exception:  # pragma: no cover - reconstruct trees may omit the pin
    Q1_PROBLEM = "they reopen the whole work list every morning instead of starting"

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


def idea_followup(title: str) -> list[str]:
    """Reprint suggested idea.md fields. Does not write idea.md."""
    lines = [
        "This command does not write idea.md.",
        "Before expand_prompt, paste these into idea.md if the template fields are still blank:",
        f"  - topic: {title}",
    ]
    row = None
    if QUEUE.is_file():
        rows = parse_queue(QUEUE.read_text(encoding="utf-8"))
        row = matching_queue_row(title, rows)
    if row and row.get("id") == "Q1" and Q1_PROBLEM:
        lines.append(f"  - problem: {Q1_PROBLEM}")
    elif row:
        lines.append(
            "  - problem: (no locked problem line for this id; write one before expand)"
        )
    else:
        lines.append("  - problem: (no matching queue row; write one before expand)")
    if row and row.get("one_line"):
        lines.append(
            f"  - mechanism (the system, not the pep talk): {row['one_line']}"
        )
    else:
        lines.append(
            "  - mechanism (the system, not the pep talk): (no matching queue one_line)"
        )
    lines.append("Do not treat those lines as spoken WORDS.")
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
    for line in idea_followup(args.title):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
