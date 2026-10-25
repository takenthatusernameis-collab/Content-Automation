#!/usr/bin/env python3
"""Suggest short, high-contrast thumbnail text grounded in the packet mechanism.

Reads idea.md for mechanism, problem, and topic. Proposes 4-6 candidates
under 6 words that name the stall or the default, stay operational, and
avoid high-precision thumbnail weak/clickbait patterns.
Does not write any files. A suggestion is a starting point for the
## Thumbnail section of publish.md or assets.md, not a final asset.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from idea_utils import extract
from phrase_utils import shorten as _shorten, THUMBNAIL_WEAK_PATTERNS as WEAK

ROOT = Path(__file__).resolve().parents[1]


def suggest(mech: str, problem: str, topic: str) -> list[str]:
    """Return short thumbnail candidates grounded in the packet."""
    if not mech:
        mech = "next-action default"
    base = _shorten(mech, 22)
    stall = _shorten(problem, 18) if problem else "the stall"
    # High-contrast, operational phrases that name mechanism or stall
    candidates = [
        f"Write the {base}",
        f"{base} first",
        f"Stop the {stall}",
        f"Cue on the work",
        f"{base} on disk",
        f"No more reopen",
        f"Install the {base}",
        f"Start cue ready",
    ]
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK):
            continue
        words = c.split()
        if not (2 <= len(words) <= 6):
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:6]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest short mechanism-aligned thumbnail text. No file writes."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}", file=sys.stderr)
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    thumbs = suggest(mech, problem, topic)
    print("THUMBNAIL TEXT SUGGESTIONS (short; operational; no weak patterns)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    print()
    for i, t in enumerate(thumbs, 1):
        print(f"{i}. {t}")
    print()
    print("Paste preferred line into ## Thumbnail of publish.md or assets.md.")
    print("Then run thumbnail_scan.py to confirm. This tool writes nothing.")
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
