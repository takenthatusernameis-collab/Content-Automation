#!/usr/bin/env python3
"""Suggest mechanism-aligned end-screen / final CTA text that avoids engagement bait.

Reads idea.md for mechanism, problem, and topic. Proposes 2-4 short CTA candidates
that name the concrete default or stall, stay calm/operational, and avoid the
high-precision weak/engagement-bait patterns tracked by end_screen_scan.py.
Does not write any files. A suggestion is a starting point for the ## End screen
or ## CTA section of publish.md, not a final design.
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
    "smash the like",
    "don't forget to",
    "don’t forget to",
    "leave a comment",
    "subscribe for more",
    "hit the subscribe",
    "like and subscribe",
    "comment below",
    "what do you think",
    "let me know",
    "turn on notifications",
    "ring the bell",
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
    """Return 2-4 short end-screen / CTA candidates grounded in the packet."""
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    # Prefer concrete install / default actions, not engagement prompts
    candidates = [
        f"Write the {base[:30]} on disk today.",
        f"Install the {base[:25]} before the next decision.",
        "Name the stall in one sentence and write the default.",
        f"Same-day install: {base[:20]}",
        "One concrete default beats another open decision.",
    ]
    # Filter weak patterns, enforce reasonable length, dedupe
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK):
            continue
        words = c.split()
        if len(words) > 15 or len(words) < 4:
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:4]

def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest mechanism-aligned end-screen / CTA text.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    ctas = suggest(mech, problem, topic)
    print("END SCREEN / CTA SUGGESTION (mechanism-aligned; concrete action; no engagement bait)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    if topic:
        print(f"topic: {topic}")
    print()
    print("Suggested end-screen / final CTA (paste into publish.md ## End screen or ## CTA):")
    for i, t in enumerate(ctas, 1):
        wc = len(t.split())
        print(f"{i}. {t}  ({wc} words)")
    print()
    print("The CTA should be the concrete next action from the mechanism, not a subscribe or reply prompt.")
    print("Run tools/end_screen_scan.py after to confirm no weak/engagement-bait patterns.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
