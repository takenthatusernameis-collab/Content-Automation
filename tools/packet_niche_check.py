#!/usr/bin/env python3
"""Soft niche-alignment check for a single packet's idea.md.

Extracts mechanism, problem, and topic via idea_utils. Counts operational niche
keywords (same set as topic_queue_mechanism_check) in the combined text.
Prints soft notes when the packet under-represents the systems-for-focused-work
focus. Useful before further packet work or after scaffold.
Does not write files, invent content, poll secrets, or scaffold.
Reduces recurring labor of manually verifying idea.md consistency with
docs/channel.md across future packets.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract  # noqa: E402

# Same operational keywords as topic_queue_mechanism_check.py
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
    if len(sys.argv) < 2:
        print("usage: python3 tools/packet_niche_check.py <packet_dir>")
        print("example: python3 tools/packet_niche_check.py videos/002-stop-deciding-what-to-work-on-every-morning")
        return 1
    packet = Path(sys.argv[1])
    if not packet.is_dir():
        print(f"packet directory not found: {packet}")
        return 1
    idea = packet / "idea.md"
    if not idea.is_file():
        print(f"idea.md missing in {packet}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    combined = f"{mech} {problem} {topic}".lower()
    hits = [k for k in NICHE_KEYS if k in combined]

    print("PACKET NICHE CHECK (soft; idea.md alignment; no invent, no writes)")
    print(f"Packet: {packet}")
    print(f"Channel niche (from docs/channel.md): systems for doing focused work; name the stall, install one default.")
    print(f"Checked keywords: {', '.join(sorted(NICHE_KEYS))}")
    print()
    print(f"topic: {topic or '(empty)'}")
    print(f"problem: {problem or '(empty)'}")
    print(f"mechanism: {mech or '(empty)'}")
    print(f"niche hits: {len(hits)} ({', '.join(hits) or 'none'})")
    if len(hits) < 2:
        print("soft note: fewer than 2 niche keywords; consider reinforcing stall/default/cue language if it still fits the idea")
    else:
        print("soft note: operational niche language present. Good.")
    print()
    print("Human: signal only. Preserve specific ideas. Do not auto-edit idea.md.")
    print("Related: python3 tools/topic_queue_mechanism_check.py")
    print("Human OAuth remains the publish blocker for Q1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
