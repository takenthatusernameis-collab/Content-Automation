#!/usr/bin/env python3
"""Print structured description candidates from script spoken WORDS.

Extracts key sentences from spoken content and maps each to a suggested short
description body segment (via shared shorten) that names the concrete stall,
default, or mechanism. Flags any that hit weak/filler/bait patterns so humans
start from script-derived options instead of a blank page or generic copy.
Does not invent content, write files, poll secrets, or call external services.
Exit 0 always (informational).
Complements description_suggest.py (from idea.md) and description_scan.py.
Useful before publish.md drafting for early description planning.
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
    ANTI_SLOP_PATTERNS,
    DESCRIPTION_EXTRA_PATTERNS,
    compile_word_boundary_patterns,
)


def sentences(text: str) -> list[str]:
    text = normalize(text)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 20]


def hits_weak(text: str, patterns, compiled) -> list[str]:
    found = []
    for phrase, cre in zip(patterns, compiled):
        if cre.search(text):
            found.append(phrase)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print script-derived description candidates. No file writes."
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

    print("SCRIPT-TO-DESCRIPTION CANDIDATES (informational only; no writes)")
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
    sents = sentences(spoken)[:8]  # limit for usability

    weak_patterns = ANTI_SLOP_PATTERNS + DESCRIPTION_EXTRA_PATTERNS
    weak_compiled = compile_word_boundary_patterns(weak_patterns)

    print("Suggested description candidates section (copy into publish.md ## Description; fill only with deliberate choices):")
    print("---")
    print("## Script-derived description candidates (baseline only; human decides final description)")
    print()
    print("Description should name the concrete stall, default, and under-two-minute install. Prefer specific operational language over filler.")
    print()
    if sents:
        for i, sent in enumerate(sents, 1):
            preview = sent[:90].replace("\n", " ")
            if len(sent) > 90:
                preview += "..."
            desc_cand = shorten(sent, max_len=140)
            weak_hits = hits_weak(desc_cand, weak_patterns, weak_compiled)
            print(f"{i}. Spoken signal: {preview}")
            print(f"   Suggested description segment: {desc_cand}")
            if weak_hits:
                print(f"   - weak_description_patterns: {', '.join(weak_hits)} (rewrite to name the concrete mechanism or stall)")
            else:
                print("   - weak_description_patterns: none")
            print("   - final_choice: (select or rewrite; leave blank until decided)")
            print()
    else:
        print("(none extracted; review spoken content manually for description phrases)")
        print()
    print("### Reminder")
    print("- Prefer calm, specific, operational language matching docs/channel.md voice.")
    print("- Avoid filler and engagement bait (see description_scan.py).")
    print("- These are starters only; confirm they match the mechanism after review.")
    print("- Run tools/description_suggest.py (from idea) and tools/description_scan.py after description exists in publish.md.")
    print("- Do not invent claims or commit secrets.")
    print("---")
    print()
    print("This skeleton does not invent content or write files.")
    print("Useful before publish metadata drafting to reduce blank-page description work on every packet.")
    print("Complements tools/description_suggest.py and tools/description_scan.py.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
