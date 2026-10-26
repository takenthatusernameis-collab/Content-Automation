#!/usr/bin/env python3
"""Print structured first-comment candidates from script spoken WORDS.

Extracts key sentences that name the mechanism or assignment action from spoken
content and maps each to a suggested pinned first-comment text (via shared
shorten) that states the concrete viewer assignment. Flags any that hit
FIRST_COMMENT_BAIT_PATTERNS so humans start from script-derived pin options
instead of a blank page or a reply prompt. Does not invent content, write
files, poll secrets, or call external services. Exit 0 always (informational).
Complements first_comment_scan.py and body_suggest.py.
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
    FIRST_COMMENT_BAIT_PATTERNS,
    compile_word_boundary_patterns,
)


def sentences(text: str) -> list[str]:
    text = normalize(text)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 25]


def hits_bait(text: str, patterns, compiled) -> list[str]:
    found = []
    for phrase, cre in zip(patterns, compiled):
        if cre.search(text):
            found.append(phrase)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print script-derived first-comment candidates. No file writes."
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

    print("SCRIPT-TO-FIRST-COMMENT CANDIDATES (informational only; no writes)")
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
    sents = sentences(spoken)[:5]  # limit for usability; prefer assignment-like

    bait_compiled = compile_word_boundary_patterns(FIRST_COMMENT_BAIT_PATTERNS)

    print("Suggested first-comment candidates section (copy into publish.md First comment; fill only with deliberate choices):")
    print("---")
    print("## Script-derived first-comment candidates (baseline only; human decides final pin)")
    print()
    print("The pin should be the assignment from the mechanism, not a reply prompt.")
    print()
    if sents:
        for i, sent in enumerate(sents, 1):
            preview = sent[:90].replace("\n", " ")
            if len(sent) > 90:
                preview += "..."
            comment_cand = shorten(sent, max_len=140)
            bait_hits = hits_bait(comment_cand, FIRST_COMMENT_BAIT_PATTERNS, bait_compiled)
            print(f"{i}. Spoken signal: {preview}")
            print(f"   Suggested first comment (assignment): {comment_cand}")
            if bait_hits:
                print(f"   - bait_patterns: {', '.join(bait_hits)} (rewrite to avoid; pin the action, not a prompt)")
            else:
                print("   - bait_patterns: none")
            print("   - final_choice: (select or rewrite as the concrete viewer assignment; leave blank until decided)")
            print()
    else:
        print("(none extracted; review spoken content manually for the mechanism assignment)")
        print()
    print("### Reminder")
    print("- Prefer the concrete next action the viewer should do today (the mechanism).")
    print("- Avoid engagement-bait and reply prompts (see first_comment_scan.py and FIRST_COMMENT_BAIT_PATTERNS).")
    print("- These are starters only; confirm they name the stall and the default.")
    print("- Run tools/first_comment_scan.py after publish.md exists.")
    print("- Do not invent claims or commit secrets.")
    print("---")
    print()
    print("This skeleton does not invent content or write files.")
    print("Useful before publish drafting to reduce blank-page first-comment (pin) work on every packet.")
    print("Complements tools/first_comment_scan.py and tools/body_suggest.py.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
