#!/usr/bin/env python3
"""Suggest mechanism-aligned visual stage directions.

Reads idea.md for mechanism, problem, and topic. Proposes 3-4 short
italic stage-direction candidates (target 12-35 words) that show the
stall or the installed default in the physical workspace, stay operational,
and avoid generic stock-footage language. Does not write any files.
A suggestion is a starting point for a VISUAL: line in draft.md, not a final script.
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
    "stock footage",
    "person thinking",
    "laptop closeup",
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
    """Return 3-4 short visual direction candidates grounded in the packet."""
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    stall = problem.lower() if problem else "the list reopens"
    candidates = [
        f"Close on the open list. Cursor hovers. No note visible. Then a sticky note with the {base[:40]} appears at the top of the page.",
        f"Desk edge. Monitor shows the stalled task. Hand places a small card with the exact {base[:35]} next to the keyboard. List stays closed.",
        f"Tab is open. Nothing is written. Camera stays on the empty first line while the viewer writes the {base[:30]} and leaves it open.",
        f"Multiple windows. One note remains. The note contains only the {base[:40]}. Other lists are minimized. Cursor moves to the note.",
    ]
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK):
            continue
        words = c.split()
        if len(words) > 45 or len(words) < 8:
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:4]


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest mechanism-aligned visual stage directions.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    visuals = suggest(mech, problem, topic)
    print("VISUAL SUGGESTION (mechanism-aligned; short stage direction; operational)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    if topic:
        print(f"topic: {topic}")
    print()
    print("Suggested VISUAL: lines (italic stage directions; 12-35 words; place under matching WORDS):")
    for i, t in enumerate(visuals, 1):
        wc = len(t.split())
        print(f"{i}. *{t}*  ({wc} words)")
    print()
    print("Each direction must show the stall or the installed default in the workspace the viewer already has.")
    print("Prefer a concrete object or note placement over generic stock language.")
    print("Keep VISUAL shorter than the WORDS it accompanies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
