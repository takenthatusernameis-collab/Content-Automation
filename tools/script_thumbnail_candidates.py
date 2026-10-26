#!/usr/bin/env python3
"""Print structured thumbnail text candidates from script spoken WORDS.

Extracts key sentences from spoken content (preferring early ones for high-contrast hooks)
and maps each to a suggested short thumbnail phrase (via shared shorten, capped for readability)
that names the concrete stall, default, or mechanism. Flags any that hit THUMBNAIL_WEAK_PATTERNS
so humans start from script-derived thumbnail options instead of a blank page or generic bait.
Does not invent content, write files, poll secrets, or call external services.
Exit 0 always (informational).
Complements thumbnail_text_suggest.py (from idea.md) and thumbnail_scan.py.
Useful before thumbnail.md or publish.md Thumbnail section drafting for early visual-text planning.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import (  # type: ignore
    spoken_words,
    normalize,
    shorten,
    THUMBNAIL_WEAK_PATTERNS,
    compile_word_boundary_patterns,
)


def sentences(text: str) -> list[str]:
    text = normalize(text)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 12]


def hits_weak(text: str, patterns, compiled) -> list[str]:
    found = []
    for phrase, cre in zip(patterns, compiled):
        if cre.search(text):
            found.append(phrase)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print script-derived thumbnail text candidates. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    parser.add_argument(
        "--prefer",
        choices=("script", "draft", "auto"),
        default="auto",
        help="Which file to prefer for spoken WORDS (default: auto)",
    )
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("SCRIPT-TO-THUMBNAIL CANDIDATES (informational only; no writes)")
    print(f"Packet: {path.name}")
    print()

    script_path = path / "script.md"
    draft_path = path / "draft.md"
    chosen = None
    if args.prefer == "script" and script_path.is_file():
        chosen = script_path
    elif args.prefer == "draft" and draft_path.is_file():
        chosen = draft_path
    else:
        if script_path.is_file():
            chosen = script_path
        elif draft_path.is_file():
            chosen = draft_path

    if not chosen:
        print("No script.md or draft.md found.")
        print("This tool writes nothing.")
        return 0

    text = chosen.read_text(encoding="utf-8")
    spoken = spoken_words(text)
    sents = sentences(spoken)[:6]  # prefer early for thumbnail hooks; limit for usability

    weak_compiled = compile_word_boundary_patterns(THUMBNAIL_WEAK_PATTERNS)

    print("Suggested thumbnail text candidates section (copy into thumbnail.md or publish.md; fill only with deliberate choices):")
    print("---")
    print("## Script-derived thumbnail text candidates (baseline only; human decides final text)")
    print()
    print("Thumbnail text should be short (ideally under 6-8 words / ~40 chars), high-contrast, and name the concrete stall or the default the viewer can install. Prefer operational language. Avoid weak clickbait.")
    print()
    if sents:
        for i, sent in enumerate(sents, 1):
            preview = sent[:70].replace("\n", " ")
            if len(sent) > 70:
                preview += "..."
            # Cap shorter for thumbnail readability
            thumb_cand = shorten(sent, max_len=40)
            weak_hits = hits_weak(thumb_cand, THUMBNAIL_WEAK_PATTERNS, weak_compiled)
            print(f"{i}. Spoken signal: {preview}")
            print(f"   Suggested thumbnail text: {thumb_cand}")
            if weak_hits:
                print(f"   - weak_thumbnail_patterns: {', '.join(weak_hits)} (rewrite to name the concrete mechanism or stall; keep high-contrast)")
            else:
                print("   - weak_thumbnail_patterns: none")
            print("   - final_choice: (select or rewrite; leave blank until decided)")
            print()
    else:
        print("(none extracted; review spoken content manually for short high-contrast phrases)")
        print()
    print("### Reminder")
    print("- Prefer calm, specific thumbnail text matching docs/channel.md voice (name the stall, name the default).")
    print("- Keep text large and readable; avoid long sentences or weak clickbait patterns (see thumbnail_scan.py).")
    print("- These are starters only; confirm they match the mechanism after review.")
    print("- Run tools/thumbnail_text_suggest.py (from idea) and tools/thumbnail_scan.py after text exists.")
    print("- Do not invent claims or commit secrets.")
    print("---")
    print()
    print("This skeleton does not invent content or write files.")
    print("Useful before thumbnail text drafting to reduce blank-page visual-text work on every packet.")
    print("Complements tools/thumbnail_text_suggest.py and tools/thumbnail_scan.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
