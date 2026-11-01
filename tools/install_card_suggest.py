#!/usr/bin/env python3
"""Suggest concise on-card text for the same-day install default.

Extracts mechanism and problem from idea.md, shortens them with the shared
phrase_utils.shorten helper, and prints 2-3 candidate phrases suitable for
a text-card or end-card that names the default and where it lives.
Does not invent claims, write files, or call external services.

Reduces recurring labor of crafting readable on-screen install language
for every future packet while staying aligned with the channel promise.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from idea_utils import extract as idea_extract  # type: ignore
from phrase_utils import shorten  # type: ignore


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest short on-card install-default text from idea.md. No file writes."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    parser.add_argument("--max-len", type=int, default=40, help="Max characters per suggestion (default 40)")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    idea_path = path / "idea.md"
    if not idea_path.is_file():
        print("No idea.md found. Run idea_brief.py first.")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    print("INSTALL CARD TEXT SUGGESTIONS (short; no invented claims)")
    print(f"Topic: {topic or '(none)'}")
    print("Use these as starting points for a text-card or end-card that names the default.")
    print("Prefer the shortest readable version. Human decides final wording.")
    print("=" * 72)
    print()

    candidates = []
    if mech:
        short_mech = shorten(mech, max_len=args.max_len)
        candidates.append(f"Install: {short_mech}")
        candidates.append(short_mech)
    if problem:
        short_prob = shorten(problem, max_len=args.max_len)
        candidates.append(f"Stall: {short_prob}")
    if mech and problem:
        combined = shorten(f"{mech} for {problem}", max_len=args.max_len)
        candidates.append(combined)

    # Deduplicate
    seen = set()
    unique = []
    for c in candidates:
        low = c.lower().strip()
        if low and low not in seen:
            seen.add(low)
            unique.append(c.strip())

    if not unique:
        print("No mechanism or problem found in idea.md.")
        return 0

    for i, c in enumerate(unique[:3], 1):
        print(f"{i}. {c}  ({len(c)} chars)")

    print()
    print("=" * 72)
    print("Next: use one phrase on a card, then python3 tools/card_generator.py PATH")
    return 0


if __name__ == "__main__":
    sys.exit(main())
