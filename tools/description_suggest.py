#!/usr/bin/env python3
"""Suggest a mechanism-aligned video description that avoids filler and engagement bait.

Reads idea.md for mechanism, problem, and topic. Proposes a short, calm,
operational description for the ## Description section of publish.md that names
the concrete default, the stall, and the under-two-minute install action.
Avoids the high-precision anti-slop phrases and description-specific bait
tracked by description_scan.py. Does not write any files. A suggestion is a
starting point for publish.md, not a final description.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from phrase_utils import shorten as _shorten

ROOT = Path(__file__).resolve().parents[1]

MECH_RE = re.compile(r"mechanism[^\n]*:\s*(.+)", re.I)
PROBLEM_RE = re.compile(r"problem:\s*(.+)", re.I)
TOPIC_RE = re.compile(r"topic:\s*(.+)", re.I)

def extract(idea_text: str) -> tuple[str, str, str]:
    mech = ""
    problem = ""
    topic = ""
    for line in idea_text.splitlines():
        m = MECH_RE.search(line)
        if m:
            mech = m.group(1).strip().rstrip(".")
        p = PROBLEM_RE.search(line)
        if p:
            problem = p.group(1).strip().rstrip(".")
        t = TOPIC_RE.search(line)
        if t:
            topic = t.group(1).strip().rstrip(".")
    return mech, problem, topic

def suggest(mech: str, problem: str, topic: str) -> str:
    """Return a short description grounded in the packet."""
    if not mech:
        mech = "the written next-action default"
    core = _shorten(mech, 55)
    base = core.lower()
    problem_part = f" The stall is {problem.lower()}." if problem else ""
    desc = (
        f"Write the exact words of the {base} on a sticky note or device note "
        f"and put it where the stall starts. Do that before you open the next tab."
        f"{problem_part} "
        f"That installs the default in under two minutes."
    )
    return desc.strip()

def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest a mechanism-aligned description.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    desc = suggest(mech, problem, topic)
    print("DESCRIPTION SUGGESTION (mechanism-aligned; calm/operational; no filler or engagement bait)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    if topic:
        print(f"topic: {topic}")
    print()
    print("Suggested ## Description:")
    print(desc)
    print()
    print("Paste into the ## Description section of publish.md.")
    print("Run tools/description_scan.py after to confirm no filler or bait.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
