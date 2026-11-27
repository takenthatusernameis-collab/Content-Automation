#!/usr/bin/env python3
"""Print a structured human-friendly idea spot-check list.

Parses existing idea.md in a packet (does not rewrite or invent content).
Prints field presence, lengths, and soft flags (empty, too short/long, missing mechanism/problem)
so a human can scan faster than opening the raw file. Hard gates remain elsewhere
(apply_idea dry-run, queue locks). Reduces recurring research/idea review minutes across future videos.
Does not call YouTube, does not encode, does not write files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FIELDS = (
    "topic",
    "viewer",
    "problem",
    "mechanism (the system, not the pep talk)",
    "why now",
    "related videos to avoid repeating",
)


def _extract_field(text: str, field: str) -> str:
    needle = f"- {field}:"
    for line in text.splitlines():
        if line.startswith(needle):
            return line.split(":", 1)[1].strip()
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print structured idea spot-check list (no invent, no write)."
    )
    parser.add_argument("packet", type=Path, help="Packet folder")
    args = parser.parse_args()
    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}")
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print(f"No idea.md found in {packet}")
        print("Hard gates remain: apply_idea.py dry-run, queue locks.")
        return 1

    text = idea_path.read_text(encoding="utf-8", errors="replace")
    print("IDEA SPOTCHECK ASSISTANT (structured review list; no invent, no write)")
    print(f"Packet: {packet}")
    print("Source: idea.md")
    print("Hard gates remain: apply_idea.py (if present), queue_status, topic locks.")
    print("=" * 70)
    print()

    flags = []
    extracted = {}
    for field in FIELDS:
        value = _extract_field(text, field)
        extracted[field] = value
        short_name = field.split("(")[0].strip()
        if value:
            vlen = len(value)
            print(f"{short_name} ({vlen} chars): {value[:120]}{'...' if len(value) > 120 else ''}")
            if vlen < 10:
                flags.append(f"{short_name}_short")
            if vlen > 300:
                flags.append(f"{short_name}_long")
        else:
            print(f"{short_name}: (missing/empty)")
            flags.append(f"missing_{short_name.replace(' ', '_')}")

    # Soft channel-alignment hints (from docs/channel.md patterns)
    problem = extracted.get("problem", "").lower()
    mechanism = extracted.get("mechanism (the system, not the pep talk)", "").lower()
    if problem and "start" not in problem and "stall" not in problem and "list" not in problem:
        flags.append("problem_may_not_name_stall")
    if mechanism and "install" not in mechanism and "default" not in mechanism and "cue" not in mechanism and "constraint" not in mechanism:
        flags.append("mechanism_may_not_be_system")

    print()
    if flags:
        print("Soft flags (human still verifies):")
        for f in flags:
            print(f"  - {f}")
    else:
        print("No soft flags raised.")
    print()
    print("These flags are soft hints only. Review against channel voice in docs/channel.md.")
    print("Spot-check time is reduced by scanning this list instead of the raw idea.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
