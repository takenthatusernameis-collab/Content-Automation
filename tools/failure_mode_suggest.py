#!/usr/bin/env python3
"""Suggest mechanism-aligned failure mode starters.

Reads idea.md for mechanism, problem, and topic. Proposes 3-4 short concrete
failure-mode fragments (target 40-80 spoken words) that show what happens
when the default is missing, name the stall, and avoid high-precision
anti-slop patterns and generic lists. Does not write any files. A suggestion
is a starting point for a ## Beat N WORDS section of draft.md, not a final script.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from idea_utils import extract

WEAK = (
    "unlock your potential",
    "in today's fast-paced",
    "let's dive in",
    "the key is",
    "in this video",
    "you will learn",
    "work smarter",
    "in fact",
    "of course",
    "obviously",
    "to sum up",
    "many people",
    "most people",
)

def suggest(mech: str, problem: str, topic: str) -> list[str]:
    """Return 3-4 failure-mode starter candidates grounded in the packet."""
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    stall = problem.lower() if problem else "the list reopens"
    candidates = [
        f"Without the {base} the morning starts by reopening {stall}. The decision is made again from scratch. The first two minutes go to choosing instead of the work. The stall is the missing cue, not a lack of will.",
        f"The {base} is not written where the stall lives. Opening the list becomes the first action. Competing next steps stay open. The delay continues because nothing visible says start here.",
        f"You skip writing the {base}. The planned task has no start signal on the object or file you already touch. The list reopens. The under-two-minute install never happens and the day begins with the same reopen.",
        f"The default stays in your head. {stall.capitalize()} keeps winning. No sticky note, no open note, no constraint on the desk. The mechanism is known but not installed, so the stall repeats.",
    ]
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK):
            continue
        words = c.split()
        if len(words) > 100 or len(words) < 25:
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:4]

def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest mechanism-aligned failure mode starters.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    modes = suggest(mech, problem, topic)
    print("FAILURE MODE SUGGESTION (mechanism-aligned; concrete missing default; operational)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    if topic:
        print(f"topic: {topic}")
    print()
    print("Suggested failure-mode WORDS starters (use inside existing ## Beat headings; 40-80 words):")
    for i, t in enumerate(modes, 1):
        wc = len(t.split())
        print(f"{i}. {t}  ({wc} words)")
    print()
    print("Each failure mode must show the stall that occurs when this packet's mechanism is absent.")
    print("Prefer a concrete missing cue or constraint over a generic list that could fit any topic.")
    print("Run tools/quality_scan.py after drafting to confirm no anti-slop patterns.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
