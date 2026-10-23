#!/usr/bin/env python3
"""Report anti-slop phrases in script.md WORDS. Does not rewrite the script.

Patterns come from tools/phrase_utils.ANTI_SLOP_PATTERNS (single source of truth).
A hit is a revision signal, not an authorship claim. This tool does not rewrite script.md.
Default exit is 0 so a frozen Q1 script cannot fail the build. --strict exits 1 when any hit remains.
set_status.py refuses ready_for_vo while a hit remains.

Output includes a short context snippet around the first match of each phrase so the revision signal is immediately actionable.
Text is normalized (curly apostrophes/quotes/dashes -> straight) so one pattern covers common variants.
Spoken WORDS extraction uses shared phrase_utils.spoken_words.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from phrase_utils import ANTI_SLOP_PATTERNS as PATTERNS, context_snippet, spoken_words, compile_word_boundary_patterns

ROOT = Path(__file__).resolve().parents[1]

# Canonical list lives in phrase_utils.ANTI_SLOP_PATTERNS (single source of truth).
# Matching uses word boundaries for higher precision (avoids partial-word false positives).
# Text is normalized (curly apostrophes -> straight, etc.) so one pattern covers common variants.
# Spoken extraction is shared via phrase_utils.spoken_words.
# Human overview: docs/content_quality.md.

# Precompile word-boundary patterns once (case-insensitive) via shared helper.
_PATTERN_RES = compile_word_boundary_patterns(PATTERNS)


def hits(text: str) -> list[tuple[str, int, str]]:
    body = spoken_words(text)
    found = []
    for phrase, cre in zip(PATTERNS, _PATTERN_RES):
        matches = list(cre.finditer(body))
        count = len(matches)
        if count:
            m = matches[0]
            context = context_snippet(body, m)
            found.append((phrase, count, context))
    return found


def scan_path(path: Path) -> list[tuple[str, int, str]]:
    script = path / "script.md"
    if not script.is_file():
        return []
    return hits(script.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Report anti-slop phrases in script WORDS.")
    parser.add_argument("packet", nargs="?", help="Packet folder. Default: every videos/* with script.md")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any hit remains.")
    args = parser.parse_args()
    if args.packet:
        folders = [Path(args.packet)]
    else:
        videos = ROOT / "videos"
        folders = sorted(p for p in videos.iterdir() if p.is_dir() and (p / "script.md").is_file())
    print("QUALITY SCAN")
    print(f"patterns checked: {len(PATTERNS)}")
    total = 0
    for folder in folders:
        found = scan_path(folder)
        total += sum(count for _, count, _ in found)
        if not found:
            print(f"{folder.name}: clear")
            continue
        details = []
        for phrase, count, ctx in found:
            details.append(f"{phrase} x{count} [{ctx}]")
        detail = "; ".join(details)
        print(f"{folder.name}: hits {detail}")
    print(f"hits: {total}")
    print("rewrites: 0")
    if args.strict and total:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
