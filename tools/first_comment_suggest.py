#!/usr/bin/env python3
"""Suggest a concrete first-comment pin that states the mechanism assignment.

Reads idea.md for mechanism and problem. Proposes a short pinned comment
that installs the packet default as an assignment the viewer can do today
and avoids generic engagement bait or reply prompts. Does not write any files.
A suggestion is a starting point for the ## First comment section of publish.md.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from idea_utils import extract

ROOT = Path(__file__).resolve().parents[1]


def suggest(mech: str, problem: str) -> str:
    """Return a short first-comment assignment line."""
    if not mech:
        mech = "the written next-action default"
    # Concrete assignment that can be finished today; no reply prompt
    assignment = (
        f"Assignment: write the exact words of the {mech.lower()} "
        f"on a sticky note or device note and put it where the stall starts. "
        f"Do that before you open the next tab. That is the whole install."
    )
    return assignment

def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest a mechanism-aligned first comment.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, _ = extract(text)
    pin = suggest(mech, problem)
    print("FIRST COMMENT SUGGESTION (mechanism assignment; no engagement bait or reply prompt)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    print()
    print("Suggested first comment / pin:")
    print(pin)
    print()
    print("Paste into the ## First comment section of publish.md.")
    print("Run tools/first_comment_scan.py after to confirm no bait.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
