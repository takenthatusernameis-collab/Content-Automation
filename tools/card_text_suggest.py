#!/usr/bin/env python3
"""Suggest short on-screen text phrases for planned text-cards.

Reads assets.md (or falls back to script VISUAL needs) and emits 2-3
candidate phrases (<=5 words) per card. Candidates are derived from the
card need by shortening and focusing on the core action or object.
Does not invent facts, write files, or call external services.

Reduces the recurring labor of inventing readable card text while building
local cards in the editor for every future video.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import shorten  # type: ignore


def parse_assets_cards(text: str) -> list[dict[str, str]]:
    """Extract planned card rows from assets.md table."""
    cards = []
    in_table = False
    for line in text.splitlines():
        if "| Beat |" in line and "Need" in line:
            in_table = True
            continue
        if in_table and line.startswith("|") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 4 and cells[0] and cells[1]:
                cards.append({
                    "beat": cells[0],
                    "need": cells[1],
                    "type": cells[2] if len(cells) > 2 else "text-card",
                    "file": cells[3] if len(cells) > 3 else "",
                })
        elif in_table and not line.startswith("|"):
            break
    return cards


def suggest_phrases(need: str, max_words: int = 5) -> list[str]:
    """Derive 2-3 short phrases from the need using shorten and simple focus."""
    if not need or len(need.split()) < 2:
        return []
    base = shorten(need, max_len=40).strip(" .")
    words = base.split()
    phrases = []

    # Full shortened if short enough
    if len(words) <= max_words:
        phrases.append(base)

    # First N words
    if len(words) > 2:
        phrases.append(" ".join(words[:max_words]))

    # Key action + object heuristic: last significant words
    if len(words) > 3:
        phrases.append(" ".join(words[-max_words:]))

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for p in phrases:
        low = p.lower().strip()
        if low and low not in seen and len(low.split()) <= max_words:
            seen.add(low)
            unique.append(p.strip())
    return unique[:3]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest short (<=5 word) on-screen phrases for planned text-cards. No file writes."
    )
    parser.add_argument("packet", help="Packet folder containing assets.md (preferred) or script.md")
    parser.add_argument("--max-words", type=int, default=5, help="Maximum words per suggestion (default 5)")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    assets_path = path / "assets.md"
    cards = []
    source = "assets.md"
    if assets_path.is_file():
        text = assets_path.read_text(encoding="utf-8")
        cards = parse_assets_cards(text)
    if not cards:
        # Fallback: could parse script, but keep simple for now
        print("No planned cards found in assets.md.")
        print("Run: python3 tools/asset_brief.py PATH first.")
        return 0

    print("CARD TEXT SUGGESTIONS (short on-screen phrases; no invented content)")
    print(f"Source: {source}")
    print("Use these as starting points for on-card text. Prefer the shortest readable version.")
    print("Keep <=5 words. Human decides the final wording.")
    print("=" * 72)
    print()

    for card in cards:
        if card.get("type", "").lower() != "text-card":
            continue
        phrases = suggest_phrases(card["need"], args.max_words)
        print(f"Beat: {card['beat']}")
        print(f"Need: {card['need']}")
        if phrases:
            for i, p in enumerate(phrases, 1):
                print(f"  {i}. {p}  ({len(p.split())} words)")
        else:
            print("  (need too short for suggestion)")
        print()

    print("=" * 72)
    print("Next: build the cards locally, then python3 tools/card_generator.py PATH --inspect-only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
