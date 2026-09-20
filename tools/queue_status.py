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

Q1_HOLD = (
    "# Q1 remaining labor is docs/gate_machine.md; do not scaffold Q2"
)


def packet_status(videos: Path, folder: str | None) -> str:
    """Read packet.md status only. Never mutates. Missing file is not invented ready."""
    if not folder:
        return "-"
    path = videos / folder / "packet.md"
    if not path.is_file():
        return "no-packet"
    for ln in path.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if s.startswith("- status:"):
            value = s.split(":", 1)[1].strip()
            return value or "empty"
    return "no-status"


def classify(row: dict[str, str], folders: list[str]) -> tuple[str, str, str | None]:
    """Return (code, note, folder). Never mutates."""
    folder = match_folder(row["working_title"], folders)
    status = row["status"]
    if folder and "sample-001" in folder:
        return "fixture-refuse", f"matches fixture {folder}; do not mark used", folder
    if status == "queued" and folder:
        return "mark-needed", f"folder videos/{folder} exists; dry-run mark_topic", folder
    if status == "used" and not folder:
        return "missing-folder", "marked used but no matching videos/ folder", None
    if status == "used" and folder:
        return "ok-used", f"videos/{folder}", folder
    if status == "parked":
        note = f"videos/{folder}" if folder else "no folder; stay parked"
        return "parked", note, folder
    if status == "queued":
        return "ok-queued", "available to scaffold", None
    return "unknown-status", f"status {status!r} is not queued/used/parked", folder


def queue_next_footer(text: str, folders: list[str], predicted_id: str) -> str:
    """First ok-queued reprint only. Never prints --queue for mark-needed."""
    rows = parse_queue(text)
    for row in rows:
        code, _, _folder = classify(row, folders)
        if code != "ok-queued":
            continue
        slug = slugify(row["working_title"])
        dest = f"videos/{predicted_id}-{slug}"
        return (
            "Queue next (not the fixture):\n"
            f"  python3 tools/idea_brief.py --queue {row['id']}\n"
            f'  python3 tools/new_packet.py "{row["working_title"]}"\n'
            f"  # predicted {dest}; human only; do not auto-scaffold\n"
            f"  {Q1_HOLD}\n"
        )
    return (
        "Queue next: no unused queued topic.\n"
        f"{Q1_HOLD}\n"
    )


def report(text: str, folders: list[str], predicted_id: str, videos: Path) -> tuple[str, dict[str, int]]:
    rows = parse_queue(text)
    lines = [
        "This command writes nothing.",
        "Queue file: docs/topic_queue.md",
        f"Packets: {', '.join(folders) or '(none besides template)'}",
        f"{'ID':<4} {'STATUS':<8} {'CODE':<16} {'PACKET':<16} SLUG / NOTE",
        "-" * 96,
    ]
    counts = {
        "mark-needed": 0,
        "missing-folder": 0,
        "ok-queued": 0,
        "ok-used": 0,
        "parked": 0,
        "fixture-refuse": 0,
        "unknown-status": 0,
    }
    first_queued: dict[str, str] | None = None
    mark_cmds: list[str] = []
    mark_folders: list[str] = []
    for row in rows:
        code, note, folder = classify(row, folders)
        slug = slugify(row["working_title"])
        pkt = packet_status(videos, folder)
        lines.append(
            f"{row['id']:<4} {row['status']:<8} {code:<16} {pkt:<16} {slug} — {note}"
        )
        if code in counts:
            counts[code] += 1
        if code == "ok-queued" and first_queued is None:
            first_queued = row
        if code == "mark-needed":
            mark_cmds.append(f"  python3 tools/mark_topic.py --id {row['id']}")
            mark_cmds.append(f"  # python3 tools/mark_topic.py --id {row['id']} --write")
            if folder:
                mark_folders.append(folder)
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
        lines.append(
            f"  python3 tools/idea_brief.py --queue {first_queued['id']}"
        )
        lines.append("  (optional pre-scaffold reprint; writes nothing; no folder required)")
        lines.append(f'  python3 tools/new_packet.py "{first_queued["working_title"]}"')
        lines.append("  (human / instructed agent only; do not auto-scaffold)")
        lines.append(f"  {Q1_HOLD}")
    else:
        lines.append("No unused queued topic.")
        lines.append(Q1_HOLD)
    if mark_cmds:
        lines.append("Close queue drift (dry-run first):")
        lines.extend(mark_cmds)
        lines.append("After that folder exists, fill idea.md from idea_brief (writes nothing):")
        seen: set[str] = set()
        for folder in mark_folders:
            if folder in seen:
                continue
            seen.add(folder)
            path = f"videos/{folder}"
            lines.append(f"  python3 tools/idea_brief.py {path} --block")
            lines.append(f"  # paste into {path}/idea.md by hand")
            lines.append(f"  python3 tools/idea_brief.py {path} --check")
    lines.append("Do not treat this board as permission to write the queue or invent WORDS.")
    return "\n".join(lines) + "\n", counts


def exit_code(counts: dict[str, int], strict: bool) -> int:
    """Default 0 so a clean human glance is not an error. --strict monitors drift."""
    if not strict:
        return 0
    if counts.get("missing-folder", 0):
        return 2
    if counts.get("mark-needed", 0) or counts.get("unknown-status", 0):
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only topic-queue vs videos/ board. No writes."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 2 on missing-folder, 1 on mark-needed/unknown-status. Still writes nothing.",
    )
    args = parser.parse_args()
    if not QUEUE.is_file():
        print(f"Missing queue: {QUEUE}", file=sys.stderr)
        return 1
    text = QUEUE.read_text(encoding="utf-8")
    folders = existing_dirs(VIDEOS)
    body, counts = report(text, folders, next_id(VIDEOS), VIDEOS)
    sys.stdout.write(body)
    return exit_code(counts, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
