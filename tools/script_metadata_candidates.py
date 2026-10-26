#!/usr/bin/env python3
"""Print structured metadata candidates from script spoken WORDS.

Extracts key sentences from spoken content and maps each to suggested title options,
thumbnail text, and a description hook using shared shorten. Flags any that hit
weak/clickbait patterns so humans start from concrete script-derived publish options
instead of a blank page. Does not invent content, write files, poll secrets, or call
external services. Exit 0 always (informational).
Complements title_scan.py, thumbnail_scan.py, and body_suggest.py.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import spoken_words, normalize, shorten, TITLE_WEAK_PATTERNS, THUMBNAIL_WEAK_PATTERNS, compile_word_boundary_patterns  # type: ignore


def sentences(text: str) -> list[str]:
    text = normalize(text)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 25]


def hits_weak(text: str, patterns, compiled) -> list[str]:
    found = []
    for phrase, cre in zip(patterns, compiled):
        if cre.search(text):
            found.append(phrase)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print script-derived metadata candidates. No file writes."
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

    print("SCRIPT-TO-METADATA CANDIDATES (informational only; no writes)")
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
    sents = sentences(spoken)[:6]  # limit for usability

    title_weak = compile_word_boundary_patterns(TITLE_WEAK_PATTERNS)
    thumb_weak = compile_word_boundary_patterns(THUMBNAIL_WEAK_PATTERNS)

    print("Suggested metadata candidates section (copy into titles.md / thumbnail.md / publish.md; fill only with deliberate choices):")
    print("---")
    print("## Script-derived metadata candidates (baseline only; human decides final titles and text)")
    print()
    if sents:
        for i, sent in enumerate(sents, 1):
            preview = sent[:90].replace("\n", " ")
            if len(sent) > 90:
                preview += "..."
            title_cand = shorten(sent, max_len=60)
            thumb_cand = shorten(sent, max_len=30)
            desc_hook = shorten(sent, max_len=120)
            title_hits = hits_weak(title_cand, TITLE_WEAK_PATTERNS, title_weak)
            thumb_hits = hits_weak(thumb_cand, THUMBNAIL_WEAK_PATTERNS, thumb_weak)
            print(f"{i}. Spoken signal: {preview}")
            print(f"   Suggested title: {title_cand}")
            if title_hits:
                print(f"   - weak_title_patterns: {', '.join(title_hits)} (rewrite to avoid)")
            else:
                print("   - weak_title_patterns: none")
            print(f"   Suggested thumbnail text: {thumb_cand}")
            if thumb_hits:
                print(f"   - weak_thumbnail_patterns: {', '.join(thumb_hits)} (rewrite to avoid)")
            else:
                print("   - weak_thumbnail_patterns: none")
            print(f"   Suggested description hook: {desc_hook}")
            print("   - final_choice: (select or rewrite; leave blank until decided)")
            print()
    else:
        print("(none extracted; review spoken content manually)")
        print()
    print("### Reminder")
    print("- Prefer calm, specific, operational titles matching docs/channel.md voice.")
    print("- Avoid shouted words and weak/clickbait patterns (see title_scan.py / thumbnail_scan.py).")
    print("- These are starters only; confirm they name the stall and the default.")
    print("- Run tools/title_scan.py and tools/body_suggest.py after titles.md / publish.md exist.")
    print("- Do not invent claims or commit secrets.")
    print("---")
    print()
    print("This skeleton does not invent content or write files.")
    print("Useful before publish metadata drafting to reduce blank-page title/thumbnail/description work on every packet.")
    print("Complements tools/title_scan.py, tools/thumbnail_scan.py, and tools/body_suggest.py.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
