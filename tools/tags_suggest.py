#!/usr/bin/env python3
"""Suggest mechanism-aligned tags that avoid weak, generic, or spammy patterns.

Reads idea.md for mechanism, problem, and topic. Proposes 5-10 concrete,
specific tags that name the stall, the default, or the under-two-minute
install action. Avoids the high-precision weak patterns tracked by
tags_scan.py (video, youtube, tutorial, how to, subscribe, free, best,
amazing, viral, secret, hack, etc.). No duplicates, no placeholders,
lengths between 3 and 40 characters. Does not write any files. A
suggestion is a starting point for the ## Tags section of publish.md,
not a final list.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from idea_utils import extract

ROOT = Path(__file__).resolve().parents[1]



def suggest(mech: str, problem: str, topic: str) -> list[str]:
    """Return 5-10 tag candidates grounded in the packet."""
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    candidates = [
        base[:40],
        f"install {base[:30]}",
        "sticky note default",
        "before next tab",
        "under two minutes",
        "written next action",
        "name the stall",
        "one concrete default",
    ]
    if problem:
        short_prob = problem.lower()[:35]
        candidates.append(f"stall: {short_prob}")
    if topic:
        candidates.append(topic.lower()[:40])
    # Filter weak patterns, short, long, duplicates
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower().strip()
        if not low or len(low) < 3 or len(low) > 40:
            continue
        if any(w in low for w in WEAK):
            continue
        if low not in seen:
            seen.add(low)
            cleaned.append(c.strip())
    # Ensure at least 5
    extras = ["operational default", "mechanism install", "no decision stall"]
    for e in extras:
        if len(cleaned) >= 8:
            break
        if e not in seen and len(e) <= 40:
            cleaned.append(e)
            seen.add(e)
    return cleaned[:8]


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest mechanism-aligned tags.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    tags = suggest(mech, problem, topic)
    print("TAGS SUGGESTION (mechanism-aligned; specific; no weak/generic/spam patterns)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    if topic:
        print(f"topic: {topic}")
    print()
    print("Suggested ## Tags (bullet list; pick or adapt; avoid duplicates):")
    for t in tags:
        print(f"- {t}")
    print()
    print("Paste into the ## Tags section of publish.md.")
    print("Run tools/tags_scan.py after to confirm no weak patterns, duplicates, or length issues.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
