#!/usr/bin/env python3
"""Generate a local series continuity note linking the current packet to the next queued topic.

Extracts mechanism and problem from the current packet's idea.md, finds the first unused
queued topic from docs/topic_queue.md, and writes a paste-ready series_continuity_note.md
that names the relation, suggested bridge, and what the next default should install.

No invented claims, no packet content edits, no secrets. Output stays local and gitignored.
Reduces recurring labor of re-reading the current video and queue when preparing the next idea
on every future packet after Q1.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract as idea_extract  # noqa: E402
from queue_lib import parse_queue, already_used, existing_slugs  # noqa: E402


def find_next_queued(queue_text: str, videos_dir: Path) -> dict | None:
    rows = parse_queue(queue_text)
    slugs = existing_slugs(videos_dir)
    for row in rows:
        if row["status"] != "queued":
            continue
        if already_used(row["working_title"], slugs):
            continue
        return row
    return None


def main() -> int:
    p = argparse.ArgumentParser(description="Generate series continuity note from current packet + queue")
    p.add_argument("packet", type=Path, help="Path to current packet directory")
    p.add_argument("--force", action="store_true", help="Overwrite existing series_continuity_note.md")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print("FAIL: idea.md missing", file=sys.stderr)
        return 2

    out_path = packet / "series_continuity_note.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    queue_path = ROOT / "docs" / "topic_queue.md"
    if not queue_path.is_file():
        print("FAIL: docs/topic_queue.md missing", file=sys.stderr)
        return 2
    queue_text = queue_path.read_text(encoding="utf-8")
    videos_dir = ROOT / "videos"
    next_row = find_next_queued(queue_text, videos_dir)

    lines = [
        "# Series Continuity Note",
        "",
        "Generated locally from current packet idea.md and docs/topic_queue.md.",
        "Use when preparing the next idea so the channel stays coherent.",
        "Not a script rewrite. Not a claim.",
        "",
        "## Current video",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
    ]

    if next_row:
        lines.extend([
            "## Next queued topic",
            "",
            f"- ID: {next_row['id']}",
            f"- Title: {next_row['working_title']}",
            f"- One line: {next_row['one_line']}",
            f"- Problem: {next_row.get('problem') or '(none)'}",
            "",
            "## Relation and bridge",
            "",
            f"The current video installs a written next-action default for the morning list reopen.",
            f"The next topic ({next_row['working_title']}) continues by moving the start cue onto the work itself.",
            "Bridge: after the viewer has the morning default, the next video shows where to put the physical or file cue so the first two minutes do not require reopening the list.",
            "",
            "## What the next default should install",
            "",
            "- One visible start cue on the work artifact (file, desk, or app) that means 'these are the first two minutes'.",
            "- The viewer can name that cue the same day.",
            "- It does not reopen the whole list.",
            "",
        ])
    else:
        lines.extend([
            "## Next queued topic",
            "",
            "No unused queued topic found in docs/topic_queue.md.",
            "Add a row or mark status before generating the next continuity note.",
            "",
        ])

    lines.extend([
        "## After this video publishes",
        "",
        "- Confirm the private video id appears.",
        "- Wait the observation window (uploaded_at + 10 days).",
        "- Then decide whether the next topic still fits or needs a small pivot based on comments.",
        "",
        "---",
        "Local draft only. Review before using in idea.md for the next packet.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"current_mechanism: {mech or '(none)'}")
    if next_row:
        print(f"next_topic: {next_row['id']} {next_row['working_title']}")
    else:
        print("next_topic: none found")
    print("Series continuity note ready (local; estimated relation only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
