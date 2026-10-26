#!/usr/bin/env python3
"""Print a structured visual plan from script spoken WORDS and any VISUAL cues.

Extracts key sentences or beats from spoken content and maps each to a suggested
short on-screen text-card phrase (using shared shorten) plus a blank slot for
b-roll or additional visual note. Prepares asset and editor planning so humans
or agents start from concrete script-derived visual options instead of a blank
page. Does not invent content, write files, poll secrets, or call external
services. Exit 0 always (informational).
Complements visual_cues_brief.py, card_text_suggest.py, and asset_brief.py.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import spoken_words, normalize, shorten  # type: ignore


def sentences(text: str) -> list[str]:
    text = normalize(text)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 20]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print script-derived visual plan skeleton. No file writes."
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

    print("SCRIPT-TO-VISUAL PLAN (informational only; no writes)")
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

    print("Suggested visual plan section (copy into assets.md or editor notes; fill only with deliberate choices):")
    print("---")
    print("## Script-derived visual plan (baseline only; human decides final cards and b-roll)")
    print()
    if sents:
        for i, sent in enumerate(sents, 1):
            preview = sent[:100].replace("\n", " ")
            if len(sent) > 100:
                preview += "..."
            card_text = shorten(sent, max_len=35)
            print(f"{i}. Spoken signal: {preview}")
            print(f"   Suggested card text: {card_text}")
            print("   - broll_or_visual_note: (describe public-domain or original visual that supports the point; leave blank until decided)")
            print("   - card_file: (e.g. cards/NNN-beat.png after generation)")
            print()
    else:
        print("(none extracted; add VISUAL lines or review spoken content manually)")
        print()
    print("### Reminder")
    print("- Prefer text-cards + public-domain b-roll notes per docs/assets.md.")
    print("- These are starters only; confirm readability (<=5 words preferred for cards).")
    print("- Run tools/card_text_suggest.py or tools/visual_cues_brief.py after assets.md exists.")
    print("- Do not invent visuals or commit pngs.")
    print("---")
    print()
    print("This skeleton does not invent content or write files.")
    print("Useful before asset generation or editor session to reduce blank-page visual planning on every packet.")
    print("Complements tools/visual_cues_brief.py, tools/card_text_suggest.py, and tools/asset_brief.py.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
