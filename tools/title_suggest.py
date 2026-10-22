#!/usr/bin/env python3
"""Suggest mechanism-aligned title options that avoid clickbait and shouted words.

Reads idea.md for mechanism, problem, and topic. Proposes 5+ title candidates
that name the concrete default or stall, stay calm/operational, include at least
one under 50 characters, and avoid the high-precision weak patterns tracked by
title_scan.py. Does not write any files. A suggestion is a starting point for
titles.md, not a final Primary.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from idea_utils import extract
from phrase_utils import shorten as _shorten

ROOT = Path(__file__).resolve().parents[1]

WEAK = (
    "secret hack",
    "you won't believe",
    "must see",
    "this changes everything",
    "one weird trick",
    "will shock you",
    "the secret to",
)

def suggest(mech: str, problem: str, topic: str) -> list[str]:
    """Return 5+ title candidates grounded in the packet."""
    if not mech:
        mech = "the written next-action default"
    # Prefer topic when it is already a usable title-length phrase
    core = topic.strip() if topic and len(topic) <= 60 else _shorten(mech, 45)
    base = core.lower()
    candidates = [
        topic if topic else f"Write the {base}",
        f"Install one default: {_shorten(mech, 35)}",
        f"The stall is naming what to work on. The default is {_shorten(mech, 28)}",
        f"Stop deciding. Write the {_shorten(mech, 30)}",
        f"{_shorten(mech, 40)} on a sticky note",
        f"One note that installs the {_shorten(mech, 32)}",
    ]
    # Ensure at least one short title under 50
    short = topic if topic and len(topic) < 50 else f"Write the {_shorten(mech, 35)}"
    if len(short) >= 50:
        short = _shorten(short, 48)
    candidates.insert(0, short)
    # Filter weak patterns and ALL CAPS words (except short acronyms)
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK):
            continue
        words = re.findall(r"[A-Za-z]+", c)
        if any(w.isupper() and len(w) >= 5 for w in words):
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:6]

def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest mechanism-aligned titles.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    titles = suggest(mech, problem, topic)
    print("TITLE SUGGESTION (mechanism-aligned; calm/operational; no clickbait or shouted words)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    if topic:
        print(f"topic: {topic}")
    print()
    print("Suggested titles (at least one under 50 chars; pick or adapt Primary):")
    for i, t in enumerate(titles, 1):
        length = len(t)
        print(f"{i}. {t}  ({length} chars)")
    print()
    print("Paste a chosen Primary and alts into titles.md.")
    print("Run tools/title_scan.py after to confirm no shout or weak patterns.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
