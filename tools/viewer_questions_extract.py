#!/usr/bin/env python3
"""Extract potential viewer questions and objections from a packet script or draft.

Pulls spoken WORDS, identifies sentences containing question marks, "why", "how",
"what if", "but", or common objection starters, and lists them as a baseline of
expected viewer language. Useful before the observation window so later comment
analysis has a concrete starting set of anticipated questions. Does not invent
questions, rewrite files, poll secrets, or call external services. Exit 0 always;
informational only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import spoken_words, normalize  # type: ignore


def sentences(text: str) -> list[str]:
    """Split normalized spoken text into rough sentences."""
    text = normalize(text)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 15]


def is_potential_question(sent: str) -> bool:
    low = sent.lower()
    if "?" in sent:
        return True
    starters = (
        "why ",
        "how ",
        "what if",
        "what about",
        "but ",
        "however ",
        "the problem is",
        "the issue is",
        "people might",
        "viewers might",
        "you might think",
        "common objection",
        "some will say",
    )
    return any(low.startswith(s) or f" {s}" in low for s in starters)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract potential viewer questions/objections from script or draft. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    parser.add_argument(
        "--prefer",
        choices=("script", "draft", "auto"),
        default="auto",
        help="Which file to prefer (default: auto = script if present else draft)",
    )
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("VIEWER QUESTIONS EXTRACT (informational only; no writes)")
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

    if chosen is None:
        print("No script.md or draft.md found.")
        print("This tool writes nothing.")
        return 0

    text = chosen.read_text(encoding="utf-8")
    spoken = spoken_words(text)
    if not spoken.strip():
        print(f"No spoken WORDS found in {chosen.name}.")
        print("This tool writes nothing.")
        return 0

    sents = sentences(spoken)
    questions = [s for s in sents if is_potential_question(s)]

    print(f"Source: {chosen.name}")
    print(f"Spoken sentences scanned: {len(sents)}")
    print(f"Potential questions / objections: {len(questions)}")
    print()

    if not questions:
        print("No question-like or objection-like sentences detected.")
        print("This is a starting point only. Later comment analysis can still surface new ones.")
    else:
        print("Extracted (for later comparison with real comments; not invented):")
        for i, q in enumerate(questions[:12], 1):
            preview = q[:140].replace("\n", " ")
            if len(q) > 140:
                preview += "..."
            print(f"  {i}. {preview}")
        if len(questions) > 12:
            print(f"  ... and {len(questions) - 12} more")

    print()
    print("Use this list as a baseline when reviewing comments after the observation window.")
    print("Do not treat these as actual viewer questions until real comments arrive.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
