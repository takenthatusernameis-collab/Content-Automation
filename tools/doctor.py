#!/usr/bin/env python3
"""Read-only one-command production health check.

Composes pipeline_status + next_action + hint + duration WARN.
Does not write files, bump status, create media, or call YouTube.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from hint import commands_for  # noqa: E402
from next_action import recommend  # noqa: E402
from pipeline_status import inspect, packet_dirs  # noqa: E402
from queue_lib import existing_dirs, next_id  # noqa: E402
from queue_status import queue_next_footer  # noqa: E402
from validate_packet import packet_duration_warning  # noqa: E402

QUEUE = ROOT / "docs" / "topic_queue.md"
VIDEOS = ROOT / "videos"


def format_block(path: Path, row: dict[str, object]) -> str:
    code, why = recommend(path, row)
    cmds = commands_for(path, row, code)
    dur = packet_duration_warning(path)
    drift = ",".join(row["drift"]) if row["drift"] else "—"
    lines = [
        f"Packet: {path.name}",
        f"Title: {row['title'] or '(empty)'}",
        f"Status: {row['status']}",
        f"Gate: {row['gate']}",
        f"Disk: {row['disk']} {row['present']}/{int(row['present']) + int(row['missing'])}",
        f"Open boxes: {row['open_human']}",
        f"Drift: {drift}",
        f"Code: {code}",
        f"Why: {why}",
        ]
    if dur:
        lines.append(f"Duration WARN: {dur}")
    if row["errors"]:
        for e in row["errors"]:
            lines.append(f"FAIL {e}")
    if row["incompletes"]:
        for i in row["incompletes"]:
            lines.append(f"DRAFT {i}")
    lines.append("Command:")
    if cmds:
        lines.extend(f"  {c}" for c in cmds)
    else:
        lines.append("  (none)")
    lines.append("This command writes nothing.")
    return "\n".join(lines) + "\n"


def format_summary(rows: list[dict[str, object]]) -> str:
    failed = sum(1 for r in rows if r["gate"] == "FAIL")
    draft = sum(1 for r in rows if r["gate"] == "DRAFT")
    drifted = sum(1 for r in rows if r["drift"])
    return (
        f"Packets: {len(rows)}  "
        f"FAIL: {failed}  DRAFT: {draft}  DRIFT: {drifted}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only health check: gate, drift, duration WARN, next-action CLI. "
            "Does not write files or bump status."
        )
    )
    parser.add_argument("packet", nargs="?", help="One packet folder (default: all videos/*)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any packet has FAIL gate or status drift",
    )
    args = parser.parse_args()

    if args.packet:
        targets = [Path(args.packet).resolve()]
        show_queue = False
    else:
        targets = packet_dirs(ROOT)
        show_queue = True
        if not targets:
            print("no packets under videos/", file=sys.stderr)
            return 1

    rows = []
    blocks = []
    for t in targets:
        row = inspect(t)
        rows.append(row)
        blocks.append(format_block(t, row))
    sys.stdout.write("\n".join(blocks))
    if len(targets) > 1:
        sys.stdout.write(format_summary(rows))
    if show_queue and QUEUE.is_file():
        text = QUEUE.read_text(encoding="utf-8")
        folders = existing_dirs(VIDEOS)
        sys.stdout.write(queue_next_footer(text, folders, next_id(VIDEOS)))
    if args.strict and any(r["gate"] == "FAIL" or r["drift"] for r in rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
