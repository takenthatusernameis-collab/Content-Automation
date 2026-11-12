#!/usr/bin/env python3
"""Soft niche-alignment check for the topic queue.

Reads docs/topic_queue.md and docs/channel.md. Extracts one_line (mechanism) and problem
for each queued/used row. Checks presence of operational niche keywords (stall, start,
default, cue, list, checklist, next, work). Prints soft notes when a row under-represents
the systems-for-focused-work focus.
Does not write files, invent topics, poll secrets, or scaffold packets.
Reduces recurring labor of manually reviewing the entire queue for channel consistency
before scaffolding future packets.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from queue_lib import parse_queue  # noqa: E402

QUEUE = ROOT / "docs" / "topic_queue.md"
CHANNEL = ROOT / "docs" / "channel.md"

# Operational keywords drawn from the working niche lock (systems for focused work, stall, default, cue)
NICHE_KEYS = {
    "stall",
    "start",
    "default",
    "cue",
    "list",
    "checklist",
    "next",
    "work",
    "morning",
    "constraint",
    "action",
}


def main() -> int:
    if not QUEUE.is_file():
        print("topic_queue.md missing")
        return 1
    text = QUEUE.read_text(encoding="utf-8")
    rows = parse_queue(text)
    if not rows:
        print("No topic rows parsed.")
        return 0

    print("TOPIC QUEUE MECHANISM CHECK (soft; niche alignment; no invent, no writes)")
    print(f"Channel niche (from docs/channel.md): systems for doing focused work; name the stall, install one default.")
    print(f"Checked keywords: {', '.join(sorted(NICHE_KEYS))}")
    print()

    under = []
    for row in rows:
        if row["status"] not in ("queued", "used", "parked"):
            continue
        mech = row.get("one_line", "").lower()
        problem = row.get("problem", "").lower()
        combined = f"{mech} {problem}"
        hits = [k for k in NICHE_KEYS if k in combined]
        print(f"{row['id']} ({row['status']}): {row['working_title']}")
        print(f"  one_line: {row['one_line'][:90]}")
        print(f"  niche hits: {len(hits)} ({', '.join(hits) or 'none'})")
        if len(hits) < 2:
            under.append(row["id"])
            print("  soft note: fewer than 2 niche keywords; consider reinforcing stall/default/cue language if it still fits the idea")
        print()

    if under:
        print(f"Soft summary: {len(under)} row(s) have thin niche language ({', '.join(under)}). Review before scaffolding.")
    else:
        print("Soft summary: queued topics show operational niche language. Good.")
    print("Human: signal only. Preserve specific ideas. Do not auto-edit the queue.")
    print("Next: python3 tools/next_topic.py   or   python3 tools/queue_status.py")
    print("Human OAuth remains the publish blocker for Q1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
