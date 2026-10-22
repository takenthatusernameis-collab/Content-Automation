#!/usr/bin/env python3
"""Suggest mechanism-aligned hook text that names the stall or default.

Reads idea.md for mechanism, problem, and topic. Proposes 3-5 short hook
candidates (target 20-35 spoken words) that name the concrete default or
stall, stay calm/operational, and avoid high-precision anti-slop patterns.
Does not write any files. A suggestion is a starting point for the ## Hook
WORDS of draft.md, not a final script.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from idea_utils import extract
from phrase_utils import shorten as _shorten

ROOT = Path(__file__).resolve().parents[1]

WEAK = (
    "unlock your potential",
    "in today's fast-paced",
    "let's dive in",
    "without further ado",
    "the key is",
    "in this video",
    "you will learn",
    "work smarter",
)

def suggest(mech: str, problem: str, topic: str) -> list[str]:
    """Return 3-5 hook candidates grounded in the packet."""
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    stall = problem.lower() if problem else "the stall"
    # Concrete, operational openings that name the mechanism
    candidates = [
        f"You already know what to work on. The stall is still there when it is time to start. Write the {_shorten(base, 40)} where the decision happens.",
        f"The list is ready. The next action is not. Put the {_shorten(base, 35)} on disk before you open the first tab.",
        f"Same decision, same delay. Name the stall in one sentence and install the {_shorten(base, 30)} as the default.",
        f"Planning finished. Starting did not. The {_shorten(base, 40)} is the under-two-minute install that ends the reopen.",
        f"You open the list and the stall starts. Write the exact words of the {_shorten(base, 25)} where you can see them.",
    ]
    # Filter weak patterns, reasonable length, dedupe
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK):
            continue
        words = c.split()
        if len(words) > 45 or len(words) < 12:
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:5]

def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest mechanism-aligned hook text.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    hooks = suggest(mech, problem, topic)
    print("HOOK SUGGESTIONS (mechanism-aligned; calm; no anti-slop)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    print()
    for i, h in enumerate(hooks, 1):
        print(f"{i}. {h}")
    print()
    print("Paste into the ## Hook WORDS of draft.md.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
