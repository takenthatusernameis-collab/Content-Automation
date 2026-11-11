#!/usr/bin/env python3
"""Soft metrics and suggestions for packet thumbnail text.

Read-only. Reports character/word counts against YouTube-friendly ranges
(ideally short for readability), and soft notes on numbers or questions
if absent. Does not rewrite files, invent media, call YouTube, or poll secrets.
Exit 0 always (informational). Reduces human labor on thumbnail text review
for future videos.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from thumbnail_scan import thumbnail_text  # noqa: E402

IDEAL_MAX_CHARS = 40
IDEAL_MAX_WORDS = 5

NUMBER_RE = re.compile(r"\b\d+\b")
QUESTION_RE = re.compile(r"\?")


def analyze(text: str) -> dict:
    text = text.strip()
    chars = len(text)
    words = text.split()
    word_count = len(words)
    has_number = bool(NUMBER_RE.search(text))
    has_question = bool(QUESTION_RE.search(text))
    return {
        "text": text,
        "chars": chars,
        "words": word_count,
        "has_number": has_number,
        "has_question": has_question,
    }


def suggestions(m: dict) -> list[str]:
    sug = []
    if m["chars"] > IDEAL_MAX_CHARS:
        sug.append(f"long ({m['chars']} chars; ideal <= {IDEAL_MAX_CHARS} for readability)")
    if m["words"] > IDEAL_MAX_WORDS:
        sug.append(f"many words ({m['words']}; ideal <= {IDEAL_MAX_WORDS})")
    if not m["has_number"] and not m["has_question"]:
        sug.append("consider a number or question if natural for curiosity")
    return sug


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Soft thumbnail text length/metrics suggestions (read-only)."
    )
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    packet = args.packet.resolve()
    # Prefer publish.md
    pub = packet / "publish.md"
    assets = packet / "assets.md"
    source = None
    text = ""
    if pub.is_file():
        source = "publish.md"
        text = pub.read_text(encoding="utf-8")
    elif assets.is_file():
        source = "assets.md"
        text = assets.read_text(encoding="utf-8")
    else:
        print(f"THUMBNAIL_METRICS_SUGGEST: no publish.md or assets.md in {packet}")
        return 2

    body = thumbnail_text(text)
    print("THUMBNAIL METRICS SUGGEST (soft; for human editor; does not rewrite)")
    print(f"Packet: {packet.name}")
    print(f"Source: {source}")
    print(f"Ideal: <= {IDEAL_MAX_CHARS} chars, <= {IDEAL_MAX_WORDS} words")
    print()
    if not body:
        print("No thumbnail section found.")
        return 0

    m = analyze(body)
    sug = suggestions(m)
    print(f"Thumbnail text: {m['chars']} chars, {m['words']} words")
    print(f"  {m['text'][:100]}")
    if m["has_number"]:
        print("  has number")
    if m["has_question"]:
        print("  has question")
    if sug:
        print(f"  notes: {'; '.join(sug)}")
    else:
        print("  looks readable")
    print()
    print("Human: use as signals only; preserve channel voice and anti-slop rules.")
    print("Does not rewrite files, does not upload, does not invent media.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
