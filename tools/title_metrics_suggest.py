#!/usr/bin/env python3
"""Soft metrics and suggestions for packet titles.

Read-only. Reports character/word counts, ideal length range signals,
and soft notes on common high-engagement elements (numbers, questions,
power words) if absent. Does not rewrite titles.md, invent media,
call YouTube, or poll secrets. Exit 0 always (informational).
Reduces human labor on title review for future videos.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from validate_packet import titles_from  # noqa: E402

IDEAL_MIN_CHARS = 40
IDEAL_MAX_CHARS = 70
IDEAL_MIN_WORDS = 5
IDEAL_MAX_WORDS = 12

NUMBER_RE = re.compile(r"\b\d+\b")
QUESTION_RE = re.compile(r"\?")
POWER_WORDS = {
    "secret", "proven", "ultimate", "essential", "simple", "fast",
    "easy", "powerful", "best", "top", "how", "why", "what",
}


def analyze(title: str) -> dict:
    title = title.strip()
    chars = len(title)
    words = title.split()
    word_count = len(words)
    has_number = bool(NUMBER_RE.search(title))
    has_question = bool(QUESTION_RE.search(title))
    lower = title.lower()
    power_hits = [w for w in POWER_WORDS if w in lower]
    return {
        "title": title,
        "chars": chars,
        "words": word_count,
        "has_number": has_number,
        "has_question": has_question,
        "power_hits": power_hits,
    }


def suggestions(m: dict) -> list[str]:
    sug = []
    if m["chars"] < IDEAL_MIN_CHARS:
        sug.append(f"short ({m['chars']} chars; ideal ~{IDEAL_MIN_CHARS}-{IDEAL_MAX_CHARS})")
    elif m["chars"] > IDEAL_MAX_CHARS:
        sug.append(f"long ({m['chars']} chars; may truncate in search)")
    if m["words"] < IDEAL_MIN_WORDS:
        sug.append(f"few words ({m['words']}; ideal ~{IDEAL_MIN_WORDS}-{IDEAL_MAX_WORDS})")
    elif m["words"] > IDEAL_MAX_WORDS:
        sug.append(f"many words ({m['words']})")
    if not m["has_number"] and not m["has_question"]:
        sug.append("consider adding a number or question for curiosity if natural")
    if not m["power_hits"]:
        sug.append("no common power/how/why words; optional if fits voice")
    return sug


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Soft title length/metrics suggestions (read-only)."
    )
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    packet = args.packet.resolve()
    titles_path = packet / "titles.md"
    if not titles_path.is_file():
        print(f"TITLE_METRICS_SUGGEST: titles.md absent at {titles_path}")
        return 2

    text = titles_path.read_text(encoding="utf-8")
    titles = titles_from(text)
    print("TITLE METRICS SUGGEST (soft; for human editor; does not rewrite)")
    print(f"Packet: {packet.name}")
    print(f"Ideal: {IDEAL_MIN_CHARS}-{IDEAL_MAX_CHARS} chars, ~{IDEAL_MIN_WORDS}-{IDEAL_MAX_WORDS} words")
    print()
    if not titles:
        print("No titles found.")
        return 0

    for i, title in enumerate(titles, 1):
        m = analyze(title)
        sug = suggestions(m)
        print(f"Title {i}: {m['chars']} chars, {m['words']} words")
        print(f"  {m['title'][:80]}")
        if m["has_number"]:
            print("  has number")
        if m["has_question"]:
            print("  has question")
        if m["power_hits"]:
            print(f"  power/how words: {', '.join(m['power_hits'][:3])}")
        if sug:
            print(f"  notes: {'; '.join(sug)}")
        else:
            print("  looks balanced")
        print()
    print("Human: use as signals only; preserve channel voice and anti-slop rules.")
    print("Does not rewrite titles.md, does not upload, does not invent media.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
