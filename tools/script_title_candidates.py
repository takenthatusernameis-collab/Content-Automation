#!/usr/bin/env python3
"""Print structured title candidates from script spoken WORDS.

Extracts key sentences from spoken content (preferring early ones for hooks)
and maps each to a suggested short title phrase (via shared shorten) that
names the concrete stall, default, or mechanism. Flags any that hit weak/
clickbait patterns so humans start from script-derived title options instead
of a blank page or generic bait.
Does not invent content, write files, poll secrets, or call external services.
Exit 0 always (informational).
Complements title_suggest.py (from idea.md) and title_scan.py.
Useful before titles.md drafting for early title planning.
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
    TITLE_WEAK_PATTERNS,
    compile_word_boundary_patterns,
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
        description="Print script-derived title candidates. No file writes."
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

    print("SCRIPT-TO-TITLE CANDIDATES (informational only; no writes)")
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
    sents = sentences(spoken)[:8]  # prefer early for titles; limit for usability

    weak_compiled = compile_word_boundary_patterns(TITLE_WEAK_PATTERNS)

    print("Suggested title candidates section (copy into titles.md; fill only with deliberate choices):")
    print("---")
    print("## Script-derived title candidates (baseline only; human decides final titles)")
    print()
    print("Titles should name the concrete stall or the default the viewer can install. Prefer specific operational language. Keep under ~60 characters. Avoid weak clickbait.")
    print()
    if sents:
        for i, sent in enumerate(sents, 1):
            preview = sent[:80].replace("\n", " ")
            if len(sent) > 80:
                preview += "..."
            title_cand = shorten(sent, max_len=55)
            weak_hits = hits_weak(title_cand, TITLE_WEAK_PATTERNS, weak_compiled)
            print(f"{i}. Spoken signal: {preview}")
            print(f"   Suggested title: {title_cand}")
            if weak_hits:
                print(f"   - weak_title_patterns: {', '.join(weak_hits)} (rewrite to name the concrete mechanism or stall)")
            else:
                print("   - weak_title_patterns: none")
            print("   - final_choice: (select or rewrite; leave blank until decided)")
            print()
    else:
        print("(none extracted; review spoken content manually for title phrases)")
        print()
    print("### Reminder")
    print("- Prefer calm, specific titles matching docs/channel.md voice (name the stall, name the default).")
    print("- Avoid shouted words and weak clickbait patterns (see title_scan.py).")
    print("- These are starters only; confirm they match the mechanism after review.")
    print("- Run tools/title_suggest.py (from idea) and tools/title_scan.py after titles exist in titles.md.")
    print("- Do not invent claims or commit secrets.")
    print("---")
    print()
    print("This skeleton does not invent content or write files.")
    print("Useful before titles.md drafting to reduce blank-page title work on every packet.")
    print("Complements tools/title_suggest.py and tools/title_scan.py.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
