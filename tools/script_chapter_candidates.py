#!/usr/bin/env python3
"""Print structured chapter title candidates from script spoken WORDS.

Extracts key sentences from spoken content and maps each to a suggested short
chapter title (via shared shorten) that names the concrete beat. Flags any that
hit CHAPTER_WEAK_PATTERNS so humans start from script-derived chapter options
instead of a blank page or generic labels. Does not invent content, write files,
poll secrets, or call external services. Exit 0 always (informational).
Complements chapters_suggest.py, chapter_draft.py, and chapters_scan.py.
Useful before captions.srt exists for early planning.
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
    CHAPTER_WEAK_PATTERNS,
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
        description="Print script-derived chapter title candidates. No file writes."
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

    print("SCRIPT-TO-CHAPTER CANDIDATES (informational only; no writes)")
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
    sents = sentences(spoken)[:7]  # limit for usability; aim for 4-8 chapters

    weak_compiled = compile_word_boundary_patterns(CHAPTER_WEAK_PATTERNS)

    print("Suggested chapter title candidates section (copy into chapters.md; fill only with deliberate choices and real timestamps after VO):")
    print("---")
    print("## Script-derived chapter candidates (baseline only; human decides final titles and times)")
    print()
    print("Titles should name the concrete stall, default, or mechanism. First chapter starts at 0:00.")
    print()
    if sents:
        for i, sent in enumerate(sents, 1):
            preview = sent[:90].replace("\n", " ")
            if len(sent) > 90:
                preview += "..."
            title_cand = shorten(sent, max_len=42)
            weak_hits = hits_weak(title_cand, CHAPTER_WEAK_PATTERNS, weak_compiled)
            print(f"{i}. Spoken signal: {preview}")
            print(f"   Suggested chapter title: {title_cand}")
            if weak_hits:
                print(f"   - weak_chapter_patterns: {', '.join(weak_hits)} (rewrite to name the concrete beat)")
            else:
                print("   - weak_chapter_patterns: none")
            print("   - final_choice: (select or rewrite; leave blank until decided; add timestamp later)")
            print()
    else:
        print("(none extracted; review spoken content manually for beat titles)")
        print()
    print("### Reminder")
    print("- Prefer operational titles that name the stall or the default (see docs/channel.md).")
    print("- Avoid generic weak titles (see chapters_scan.py and CHAPTER_WEAK_PATTERNS).")
    print("- YouTube requires first at 0:00, min 10s gaps, reasonable count.")
    print("- These are starters only; confirm they match actual beats after VO.")
    print("- Run tools/chapters_suggest.py or tools/chapter_draft.py (needs srt) and tools/chapters_scan.py after chapters.md exists.")
    print("- Do not invent claims or commit secrets.")
    print("---")
    print()
    print("This skeleton does not invent content or write files.")
    print("Useful before chapter drafting to reduce blank-page title work on every packet (especially pre-captions).")
    print("Complements tools/chapters_suggest.py, tools/chapter_draft.py, and tools/chapters_scan.py.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
