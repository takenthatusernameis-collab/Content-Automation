#!/usr/bin/env python3
"""Read-only topic-queue vs videos/ board.

Does not write docs/topic_queue.md, does not scaffold, does not invent WORDS.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from queue_lib import existing_dirs, match_folder, next_id, parse_queue, slugify  # noqa: E402

QUEUE = ROOT / "docs" / "topic_queue.md"
VIDEOS = ROOT / "videos"


def classify(row: dict[str, str], folders: list[str]) -> tuple[str, str]:
    """Return (code, note). Never mutates."""
    folder = match_folder(row["working_title"], folders)
    status = row["status"]
    if folder and "sample-001" in folder:
        return "fixture-refuse", f"matches fixture {folder}; do not mark used"
    if status == "queued" and folder:
        return "mark-needed", f"folder videos/{folder} exists; dry-run mark_topic"
    if status == "used" and not folder:
        return "missing-folder", "marked used but no matching videos/ folder"
    if status == "used" and folder:
        return "ok-used", f"videos/{folder}"
    if status == "parked":
        note = f"videos/{folder}" if folder else "no folder; stay parked"
        return "parked", note
    if status == "queued":
        return "ok-queued", "available to scaffold"
    return "unknown-status", f"status {status!r} is not queued/used/parked"


def report(text: str, folders: list[str], predicted_id: str) -> str:
    rows = parse_queue(text)
    lines = [
        "This command writes nothing.",
        "Queue file: docs/topic_queue.md",
        f"Packets: {', '.join(folders) or '(none besides template)'}",
        f"{'ID':<4} {'STATUS':<8} {'CODE':<16} SLUG / NOTE",
        "-" * 88,
    ]
    counts = {"mark-needed": 0, "missing-folder": 0, "ok-queued": 0, "ok-used": 0, "parked": 0}
    first_queued: dict[str, str] | None = None
    mark_cmds: list[str] = []
    for row in rows:
        code, note = classify(row, folders)
        slug = slugify(row["working_title"])
        lines.append(f"{row['id']:<4} {row['status']:<8} {code:<16} {slug} — {note}")
        if code in counts:
            counts[code] += 1
        if code == "ok-queued" and first_queued is None:
            first_queued = row
        if code == "mark-needed":
            mark_cmds.append(f"  python3 tools/mark_topic.py --id {row['id']}")
            mark_cmds.append(f"  # python3 tools/mark_topic.py --id {row['id']} --write")
    lines.append("")
    lines.append(
        f"queued-ready: {counts['ok-queued']}  "
        f"mark-needed: {counts['mark-needed']}  "
        f"used-missing-folder: {counts['missing-folder']}  "
        f"used-ok: {counts['ok-used']}  "
        f"parked: {counts['parked']}"
    )
    if first_queued:
        slug = slugify(first_queued["working_title"])
        dest = f"videos/{predicted_id}-{slug}"
        lines.append(f"Next scaffold: {first_queued['id']} -> {dest}")
        lines.append(f'  python3 tools/new_packet.py "{first_queued["working_title"]}"')
        lines.append("  (human / instructed agent only; do not auto-scaffold)")
    else:
        lines.append("No unused queued topic.")
    if mark_cmds:
        lines.append("Close queue drift (dry-run first):")
        lines.extend(mark_cmds)
    lines.append("Do not treat this board as permission to write the queue or invent WORDS.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only topic-queue vs videos/ board. No writes."
    )
    parser.parse_args()
    if not QUEUE.is_file():
        print(f"Missing queue: {QUEUE}", file=sys.stderr)
        return 1
    text = QUEUE.read_text(encoding="utf-8")
    folders = existing_dirs(VIDEOS)
    sys.stdout.write(report(text, folders, next_id(VIDEOS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
