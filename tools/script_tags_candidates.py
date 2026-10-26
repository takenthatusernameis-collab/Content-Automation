#!/usr/bin/env python3
"""Print structured tag candidates from script spoken WORDS.

Extracts key sentences from spoken content and maps each to a suggested short
tag phrase (via shared shorten) that names the concrete stall, default, or
mechanism. Flags any that hit weak/generic/spam patterns so humans start from
script-derived tag options instead of a blank page or generic labels.
Does not invent content, write files, poll secrets, or call external services.
Exit 0 always (informational).
Complements tags_suggest.py (from idea.md) and tags_scan.py.
Useful before publish.md drafting for early metadata planning.
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
    compile_word_boundary_patterns,
)

# Match tags_scan.py high-precision weak / generic / spam patterns.
TAG_WEAK_PATTERNS = (
    "video",
    "youtube",
    "tutorial",
    "how to",
    "subscribe",
    "like and subscribe",
    "free",
    "best",
    "amazing",
    "incredible",
    "must watch",
    "viral",
    "trending",
    "clickbait",
    "secret",
    "hack",
    "tips and tricks",
)


def sentences(text: str) -> list[str]:
    text = normalize(text)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 15]


def hits_weak(text: str, patterns, compiled) -> list[str]:
    found = []
    for phrase, cre in zip(patterns, compiled):
        if cre.search(text):
            found.append(phrase)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print script-derived tag candidates. No file writes."
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

    print("SCRIPT-TO-TAGS CANDIDATES (informational only; no writes)")
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
    sents = sentences(spoken)[:10]  # limit for usability; aim for 5-8 tags

    weak_compiled = compile_word_boundary_patterns(TAG_WEAK_PATTERNS)

    print("Suggested tag candidates section (copy into publish.md ## Tags; fill only with deliberate choices):")
    print("---")
    print("## Script-derived tag candidates (baseline only; human decides final tags)")
    print()
    print("Tags should name the concrete stall, default, or mechanism. Prefer 3-40 characters, specific, no weak generics.")
    print()
    if sents:
        for i, sent in enumerate(sents, 1):
            preview = sent[:80].replace("\n", " ")
            if len(sent) > 80:
                preview += "..."
            tag_cand = shorten(sent, max_len=35)
            weak_hits = hits_weak(tag_cand, TAG_WEAK_PATTERNS, weak_compiled)
            print(f"{i}. Spoken signal: {preview}")
            print(f"   Suggested tag: {tag_cand}")
            if weak_hits:
                print(f"   - weak_tag_patterns: {', '.join(weak_hits)} (rewrite to name the concrete mechanism or stall)")
            else:
                print("   - weak_tag_patterns: none")
            print("   - final_choice: (select or rewrite; leave blank until decided)")
            print()
    else:
        print("(none extracted; review spoken content manually for tag phrases)")
        print()
    print("### Reminder")
    print("- Prefer operational tags that name the stall or the default (see docs/channel.md).")
    print("- Avoid generic weak tags (see tags_scan.py).")
    print("- YouTube tag budget is ~500 characters including commas and quotes for spaces.")
    print("- These are starters only; confirm they match the mechanism after review.")
    print("- Run tools/tags_suggest.py (from idea) and tools/tags_scan.py after tags exist in publish.md.")
    print("- Do not invent claims or commit secrets.")
    print("---")
    print()
    print("This skeleton does not invent content or write files.")
    print("Useful before publish metadata drafting to reduce blank-page tag work on every packet.")
    print("Complements tools/tags_suggest.py and tools/tags_scan.py.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
