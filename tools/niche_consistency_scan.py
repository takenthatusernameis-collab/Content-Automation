#!/usr/bin/env python3
"""Soft combined niche-alignment scan for topic queue + existing packets.

Reuses the operational keyword set from topic_queue_mechanism_check and packet_niche_check.
Scans docs/topic_queue.md (all relevant rows) then discovers non-template/non-sample
video packets and checks each idea.md via idea_utils.
Prints a unified soft summary. Useful as a single entry point before scaffolding or
packet work.
Does not write files, invent content, poll secrets, scaffold, or add hard gates.
Reduces recurring labor of running separate checks as the number of packets grows.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract  # noqa: E402
from queue_lib import parse_queue  # noqa: E402

QUEUE = ROOT / "docs" / "topic_queue.md"
VIDEOS = ROOT / "videos"

# Same operational keywords as the individual checks
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


def check_text(combined: str) -> tuple[int, list[str]]:
    hits = [k for k in NICHE_KEYS if k in combined.lower()]
    return len(hits), hits


def main() -> int:
    print("NICHE CONSISTENCY SCAN (soft; queue + packets; no invent, no writes)")
    print(f"Channel niche (from docs/channel.md): systems for doing focused work; name the stall, install one default.")
    print(f"Checked keywords: {', '.join(sorted(NICHE_KEYS))}")
    print()

    # Queue scan
    print("=== Topic queue ===")
    under_queue = []
    if not QUEUE.is_file():
        print("topic_queue.md missing")
    else:
        rows = parse_queue(QUEUE.read_text(encoding="utf-8"))
        if not rows:
            print("No topic rows parsed.")
        else:
            for row in rows:
                if row["status"] not in ("queued", "used", "parked"):
                    continue
                combined = f"{row.get('one_line', '')} {row.get('problem', '')}"
                n_hits, hits = check_text(combined)
                print(f"{row['id']} ({row['status']}): {row['working_title']}")
                print(f"  niche hits: {n_hits} ({', '.join(hits) or 'none'})")
                if n_hits < 2:
                    under_queue.append(row["id"])
                    print("  soft note: thin niche language")
                print()
            if under_queue:
                print(f"Queue soft summary: {len(under_queue)} row(s) thin ({', '.join(under_queue)}).")
            else:
                print("Queue soft summary: operational niche language present.")
    print()

    # Packet scan
    print("=== Video packets ===")
    under_packets = []
    if not VIDEOS.is_dir():
        print("videos/ missing")
    else:
        packets = [
            p for p in VIDEOS.iterdir()
            if p.is_dir() and not p.name.startswith("_") and not p.name.startswith("sample-")
        ]
        packets.sort()
        if not packets:
            print("No non-template/non-sample packets found.")
        else:
            for packet in packets:
                idea = packet / "idea.md"
                if not idea.is_file():
                    print(f"{packet.name}: idea.md missing")
                    continue
                text = idea.read_text(encoding="utf-8")
                mech, problem, topic = extract(text)
                combined = f"{mech} {problem} {topic}"
                n_hits, hits = check_text(combined)
                print(f"{packet.name}:")
                print(f"  topic: {topic or '(empty)'}")
                print(f"  niche hits: {n_hits} ({', '.join(hits) or 'none'})")
                if n_hits < 2:
                    under_packets.append(packet.name)
                    print("  soft note: thin niche language")
                print()
            if under_packets:
                print(f"Packets soft summary: {len(under_packets)} packet(s) thin ({', '.join(under_packets)}).")
            else:
                print("Packets soft summary: operational niche language present.")
    print()
    print("Overall: signal only. Preserve specific ideas. Do not auto-edit.")
    print("Related: python3 tools/topic_queue_mechanism_check.py   |   python3 tools/packet_niche_check.py <packet>")
    print("Human OAuth remains the publish blocker for Q1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
