#!/usr/bin/env python3
"""Print a structured research gap brief from script spoken WORDS.

Extracts digit and hedge claim signals (via shared helpers) and prints a
Markdown brief listing each gap with suggested source category, priority,
and blank notes for the researcher. Reduces recurring labor of manually
listing what needs sourcing before filling sources.md or research.md on
every future packet. Does not invent sources, URLs, numbers, or content.
Does not write files, poll secrets, or call external services.
Exit 0 always (informational).
Useful early in the research path so claim hygiene starts from concrete gaps.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import (
    HEDGE_PATTERNS,
    compile_word_boundary_patterns,
    context_snippet,
    spoken_words,
)
from research_brief import numbers_in_spoken_words  # type: ignore


def unique_preserve(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for it in items:
        key = it.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append(it.strip())
    return out


def hedges_with_context(script_text: str) -> list[tuple[str, str]]:
    body = spoken_words(script_text)
    found = []
    _HEDGE_RES = compile_word_boundary_patterns(HEDGE_PATTERNS)
    for phrase, cre in zip(HEDGE_PATTERNS, _HEDGE_RES):
        matches = list(cre.finditer(body))
        if matches:
            m = matches[0]
            ctx = context_snippet(body, m)
            found.append((phrase, ctx))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print script research gap brief from claim signals. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("SCRIPT RESEARCH GAP BRIEF (informational only; no writes)")
    print(f"Packet: {path.name}")
    print("Lists claim signals that need real sources before claim_scan can pass cleanly.")
    print("Suggested categories are starting points only. Do not invent citations.")
    print()

    script_path = path / "script.md"
    draft_path = path / "draft.md"
    chosen = script_path if script_path.is_file() else draft_path
    if not chosen.is_file():
        print("No script.md or draft.md found.")
        print("This tool writes nothing.")
        return 0

    text = chosen.read_text(encoding="utf-8")
    numbers = unique_preserve(numbers_in_spoken_words(text))
    hedges = hedges_with_context(text)

    if not numbers and not hedges:
        print("No digit or hedge claim signals detected in spoken WORDS.")
        print("claim_scan should already pass for these (or packet is still a skeleton).")
        print("This tool writes nothing.")
        return 0

    print(f"Source: {chosen.name}")
    print(f"Digit claims: {len(numbers)} | Hedge claims: {len(hedges)}")
    print()

    print("### Research gaps (fill notes / sources.md after verification)")
    idx = 1
    for num in numbers:
        body = spoken_words(text)
        m = re.search(re.escape(num), body)
        ctx = context_snippet(body, m) if m else "(no context)"
        print(f"{idx}. Digit claim: {num}")
        print(f"   Context: {ctx}")
        print(f"   Suggested category: study / measurement / primary source")
        print(f"   Priority: high if central to the mechanism")
        print(f"   notes: ")
        print()
        idx += 1

    for phrase, ctx in hedges:
        print(f"{idx}. Hedge claim: {phrase}")
        print(f"   Context: {ctx}")
        print(f"   Suggested category: review / survey / expert source")
        print(f"   Priority: medium (rewrite qualitatively if no good source)")
        print(f"   notes: ")
        print()
        idx += 1

    print("### Reminder")
    print("- Prefer real, verifiable sources. Do not invent numbers or studies.")
    print("- After filling, run: python3 tools/claim_scan.py PATH")
    print("- Or generate the full table with: python3 tools/claim_source_table.py PATH")
    print("- This brief does not invent content or write files.")
    print()
    print("Useful before research.md or sources.md drafting on every packet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
