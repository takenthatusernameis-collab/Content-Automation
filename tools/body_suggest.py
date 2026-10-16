#!/usr/bin/env python3
"""Suggest mechanism-aligned body beat starters / example scenes.

Reads idea.md for mechanism, problem, and topic. Proposes 3-4 short concrete
body beat fragments (target 40-90 spoken words each) that show the mechanism
in action, name the stall or default, include a distinction or test, and avoid
high-precision anti-slop patterns. Does not write any files. A suggestion is
a starting point for a ## Beat N WORDS section of draft.md, not a final script.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MECH_RE = re.compile(r"mechanism[^\n]*:\s*(.+)", re.I)
PROBLEM_RE = re.compile(r"problem:\s*(.+)", re.I)
TOPIC_RE = re.compile(r"topic:\s*(.+)", re.I)

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
)

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

def suggest(mech: str, problem: str, topic: str) -> list[str]:
    """Return 3-4 body beat starter candidates grounded in the packet."""
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    stall = problem.lower() if problem else "the list reopens"
    candidates = [
        f"You open the file and the stall starts. The list is still the whole page. Write the exact next action from the {base[:40]} at the top of the document before you scroll. That single line is the difference between reopening the decision and starting the first two minutes.",
        f"The tab is open. The work is not. Put the {base[:35]} on a sticky note on the monitor edge where the cursor already lives. When the stall hits, the note is the only thing visible. No new list. No extra decision.",
        f"Same morning, same delay. The planned task has no cue. Name one physical object that already sits on the desk and write the {base[:30]} on it. The object becomes the start signal. Opening the list is no longer the first action.",
        f"Competing lists each claim the next step. Collapse them. Write one verb from the {base[:40]} into a single note that stays open. Close every other list. The remaining note is the only place the decision can finish.",
    ]
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK):
            continue
        words = c.split()
        if len(words) > 120 or len(words) < 25:
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:4]

def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest mechanism-aligned body beat starters.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    beats = suggest(mech, problem, topic)
    print("BODY SUGGESTION (mechanism-aligned; concrete scene or distinction; operational)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    if topic:
        print(f"topic: {topic}")
    print()
    print("Suggested Beat WORDS starters (expand inside existing ## Beat headings; 40-90 words each):")
    for i, t in enumerate(beats, 1):
        wc = len(t.split())
        print(f"{i}. {t}  ({wc} words)")
    print()
    print("Each beat must show the viewer using the mechanism on this packet's stall.")
    print("Prefer a concrete action, example, or test over abstract encouragement.")
    print("Run tools/quality_scan.py after drafting to confirm no anti-slop patterns.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
