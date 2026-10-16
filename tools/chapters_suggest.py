#!/usr/bin/env python3
"""Suggest mechanism-aligned YouTube chapter lines that avoid weak titles and rule violations.

Reads idea.md for mechanism, problem, and topic. Proposes 4-8 chapter lines
starting at 0:00, with minimum 10s gaps (YouTube rule), reasonable count,
and titles that name the concrete default or stall. Avoids the high-precision
weak patterns tracked by chapters_scan.py. Does not write any files. A
suggestion is a starting point for chapters.md, not a final set.
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
    "intro",
    "outro",
    "hook",
    "cta",
    "subscribe",
    "what you will learn",
    "in this video",
    "let's dive in",
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
    """Return 4-8 chapter lines grounded in the packet."""
    if not mech:
        mech = "the written next-action default"
    base = mech.lower()
    # Assume ~8 min target; place beats at operational points
    lines = [
        "0:00 Name the stall",
        "0:45 The concrete default",
        f"1:30 Write the {base[:40]}",
        "2:45 Where it lives on disk",
        "4:00 One under-two-minute install",
        "5:30 Common failure: deciding instead of writing",
        "6:45 The same-day test",
        "7:30 Close with the default still installed",
    ]
    # Filter weak patterns
    cleaned = []
    for line in lines:
        title = line.split(None, 1)[1] if " " in line else line
        low = title.lower()
        if any(w in low for w in WEAK):
            continue
        cleaned.append(line)
    # Ensure first is 0:00 and count is reasonable
    if not cleaned or not cleaned[0].startswith("0:00"):
        cleaned.insert(0, "0:00 Name the stall")
    return cleaned[:8]

def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest mechanism-aligned chapters.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    chapters = suggest(mech, problem, topic)
    print("CHAPTERS SUGGESTION (mechanism-aligned; starts 0:00; >=10s gaps; no weak titles)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    if topic:
        print(f"topic: {topic}")
    print()
    print("Suggested YouTube lines (paste into chapters.md ## YouTube lines):")
    for line in chapters:
        print(line)
    print()
    print("Adjust timestamps to match actual script length after VO.")
    print("Run tools/chapters_scan.py after to confirm no weak titles, gaps, or count issues.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
