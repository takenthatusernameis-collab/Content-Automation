#!/usr/bin/env python3
"""Suggest mechanism-aligned payoff promise starters.

Reads idea.md for mechanism, problem, and topic. Proposes 2-3 short
payoff promise candidates (target 40-70 spoken words) that name the
concrete doable outcome, the mechanism, and the under-two-minute install,
and avoid high-precision anti-slop patterns. Does not write any files.
A suggestion is a starting point for the ## Payoff promise WORDS of
draft.md, not a final script.
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

def _shorten(text: str, max_len: int = 40) -> str:
    """Return a natural short phrase, preferring whole words or first clause."""
    text = text.strip()
    if len(text) <= max_len:
        return text
    for sep in (". ", ", ", " so ", " that ", " and ", " — ", " - "):
        if sep in text:
            cand = text.split(sep)[0].strip()
            if 10 <= len(cand) <= max_len:
                return cand
    words = text.split()
    out = []
    for w in words:
        trial = " ".join(out + [w])
        if len(trial) > max_len:
            break
        out.append(w)
    return " ".join(out) if out else text[:max_len].rstrip()

def suggest(mech: str, problem: str, topic: str) -> list[str]:
    """Return 2-3 payoff promise candidates grounded in the packet."""
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    stall = problem.lower() if problem else "the list reopens"
    candidates = [
        f"After this video you can write the {_shorten(base, 40)} once and put it where the stall starts. The morning no longer reopens the whole list because the next action is already visible. The install takes under two minutes.",
        f"You leave with one concrete default: the {_shorten(base, 35)} written on the object or file that already sits at the start of the work. Opening the list is no longer the first action. The change is finishable today.",
        f"The outcome is a single next-action line from the {_shorten(base, 40)} that stays open. Competing lists collapse. The stall that used to reopen the decision now hits the written cue instead.",
    ]
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK):
            continue
        words = c.split()
        if len(words) > 90 or len(words) < 30:
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:3]

def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest mechanism-aligned payoff promise starters.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    promises = suggest(mech, problem, topic)
    print("PAYOFF SUGGESTION (mechanism-aligned; concrete doable outcome; under-two-minute install)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    if topic:
        print(f"topic: {topic}")
    print()
    print("Suggested Payoff promise WORDS (40-70 words; name the mechanism and the outcome):")
    for i, t in enumerate(promises, 1):
        wc = len(t.split())
        print(f"{i}. {t}  ({wc} words)")
    print()
    print("The payoff must name what the viewer can do after watching and how the mechanism delivers it.")
    print("Prefer a concrete install over abstract encouragement.")
    print("Run tools/quality_scan.py after drafting to confirm no anti-slop patterns.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
