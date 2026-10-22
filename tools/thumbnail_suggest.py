#!/usr/bin/env python3
"""Suggest mechanism-aligned thumbnail text ideas that avoid clickbait and long text.

Reads idea.md for mechanism, problem, and topic. Proposes 3-5 short thumbnail
text candidates (prefer <=6 words, always <=8) that name the concrete default
or stall, stay calm/operational, and avoid the high-precision weak/clickbait
patterns tracked by thumbnail_scan.py. Does not write any files. A suggestion
is a starting point for the ## Thumbnail section, not a final design.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from idea_utils import extract

ROOT = Path(__file__).resolve().parents[1]


def suggest(mech: str, problem: str, topic: str) -> list[str]:
    """Return 3-5 short thumbnail text candidates grounded in the packet."""
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    # Prefer very short, high-contrast operational phrases
    candidates = [
        f"Write the {base[:25]}",
        "Name the stall",
        f"Install: {base[:20]}",
        "One default on disk",
        f"Stop deciding. {base[:15]}",
        "Same-day install",
    ]
    # Filter weak patterns, enforce length, dedupe
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK):
            continue
        words = c.split()
        if len(words) > 8:
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:5]

def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest mechanism-aligned thumbnail text.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    thumbs = suggest(mech, problem, topic)
    print("THUMBNAIL SUGGESTION (mechanism-aligned; short/readable; no clickbait)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    if topic:
        print(f"topic: {topic}")
    print()
    print("Suggested thumbnail text (prefer <=6 words; paste into publish.md ## Thumbnail or assets.md):")
    for i, t in enumerate(thumbs, 1):
        wc = len(t.split())
        print(f"{i}. {t}  ({wc} words)")
    print()
    print("Keep text large and high-contrast. Pair with a simple visual of the default or stall.")
    print("Run tools/thumbnail_scan.py after to confirm no long text or weak/clickbait patterns.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
