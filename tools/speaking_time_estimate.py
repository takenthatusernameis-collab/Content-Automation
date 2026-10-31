#!/usr/bin/env python3
"""Estimate narration duration from spoken word count.

Extracts spoken WORDS from draft.md or script.md using shared helpers,
counts words with the canonical counter, and estimates speaking time at a
typical clear-narration rate (140 wpm).
Prints minutes:seconds and a short note for timeline/planning use.
Reduces recurring manual calculation of expected VO length before recording or assembly
for every future packet. Does not invent content, rewrite files, or call external services.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import spoken_words, count_spoken_words

WPM = 140  # typical clear explanatory narration rate


def estimate_seconds(word_count: int) -> int:
    if word_count <= 0:
        return 0
    return int(round(word_count / WPM * 60))


def format_duration(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    return f"{m}:{s:02d}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Estimate speaking time from packet spoken words. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    draft = path / "draft.md"
    script = path / "script.md"
    source = draft if draft.is_file() else script
    if not source.is_file():
        print(f"No draft.md or script.md in {path}", file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8")
    words_text = spoken_words(text)
    count = count_spoken_words(words_text)

    seconds = estimate_seconds(count)
    duration = format_duration(seconds)

    print("SPEAKING TIME ESTIMATE (approximate; verify with real take)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Spoken words: {count}")
    print(f"Estimated rate: {WPM} wpm (clear narration)")
    print(f"Estimated duration: {duration} ({seconds} seconds)")
    print()
    print("Use for timeline planning and end-screen reservation (last 20s).")
    print("Actual take length may differ; run media_qa after a selected VO exists.")
    print("Word count uses shared phrase_utils.count_spoken_words.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
