#!/usr/bin/env python3
"""Reprint suggested idea.md fields for an existing packet.

Read-only. Does not write idea.md, the queue, or packets.
Recovers the new_packet idea_followup after scaffold stdout is gone.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from new_packet import idea_followup  # noqa: E402


def field(text: str, name: str) -> str:
    pat = rf"^- {re.escape(name)}:[ \t]*(.*)$"
    m = re.search(pat, text, re.M)
    if m:
        return m.group(1).strip()
    if name == "mechanism":
        m = re.search(
            r"^- mechanism \(the system, not the pep talk\):[ \t]*(.*)$",
            text,
            re.M,
        )
        if m:
            return m.group(1).strip()
    return ""


def working_title(path: Path) -> str:
    packet = path / "packet.md"
    if packet.is_file():
        m = re.search(r"^- working_title:[ \t]*(.*)$", packet.read_text(encoding="utf-8"), re.M)
        if m and m.group(1).strip():
            return m.group(1).strip()
    idea = path / "idea.md"
    if idea.is_file():
        t = field(idea.read_text(encoding="utf-8"), "topic")
        if t:
            return t
    return path.name.split("-", 1)[-1].replace("-", " ")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only idea.md reprint. Does not write idea.md."
    )
    parser.add_argument("packet", help="Packet folder")
    args = parser.parse_args()
    path = Path(args.packet)
    if not path.is_dir():
        print(f"not a packet folder: {path}", file=sys.stderr)
        return 1

    title = working_title(path)
    idea_path = path / "idea.md"
    current = idea_path.read_text(encoding="utf-8") if idea_path.is_file() else ""
    print(f"Packet: {path.name}")
    print(f"Title: {title}")
    print("Current idea.md:")
    print(f"  - topic: {field(current, 'topic') or '(blank)'}")
    print(f"  - problem: {field(current, 'problem') or '(blank)'}")
    print(f"  - mechanism: {field(current, 'mechanism') or '(blank)'}")
    print("Suggested paste (does not write idea.md):")
    for line in idea_followup(title):
        print(line)
    if "sample-001" in path.name:
        print("Fixture lock: do not treat this packet as the first real video.")
    print("This command writes nothing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
