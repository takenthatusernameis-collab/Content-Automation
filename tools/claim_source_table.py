#!/usr/bin/env python3
"""Generate a fillable claim-to-source Markdown table from a packet script or draft.

Extracts quantitative (digit) and hedge claims from spoken WORDS using the shared
helpers. Emits a structured table that maps each unique claim to a placeholder
source row. Does not invent URLs, numbers, citations, or results. Does not write
files. Does not call APIs.

Useful early in the research path (or after a draft exists) so the human or
agent can paste the table into sources.md / research.md and fill only the
Source column. Reduces the recurring labor of manually listing every claim
that claim_scan will later require.
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
        description="Print a fillable claim-to-source Markdown table from script.md or draft.md. No invented sources."
    )
    parser.add_argument("packet", help="Packet folder containing script.md and/or draft.md")
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

    script_path = path / "script.md"
    draft_path = path / "draft.md"
    chosen = None
    if args.prefer == "script" and script_path.is_file():
        chosen = script_path
    elif args.prefer == "draft" and draft_path.is_file():
        chosen = draft_path
    else:  # auto
        if script_path.is_file():
            chosen = script_path
        elif draft_path.is_file():
            chosen = draft_path

    if chosen is None:
        print("No script.md or draft.md found.")
        print("Generate a draft first with: python3 tools/draft_starter.py PATH")
        return 0

    text = chosen.read_text(encoding="utf-8")
    numbers = unique_preserve(numbers_in_spoken_words(text))
    hedges = hedges_with_context(text)

    print("CLAIM-TO-SOURCE TABLE (fillable; no invented sources)")
    print(f"Source file: {chosen.name}")
    print("Paste the table below into sources.md or research.md, then fill only the Source column with real, verifiable citations.")
    print("claim_scan will extract non-placeholder Source cells / bullets automatically.")
    print("=" * 72)
    print()

    if not numbers and not hedges:
        print("No quantitative digits or hedge phrases detected in spoken WORDS.")
        print("claim_scan should already pass for these signals (or the packet is still a skeleton).")
        return 0

    print("| Claim | Type | Context | Suggested category | Source (fill) | Notes |")
    print("|-------|------|---------|--------------------|---------------|-------|")

    for num in numbers:
        # Simple context: first occurrence window
        body = spoken_words(text)
        m = re.search(re.escape(num), body)
        ctx = context_snippet(body, m) if m else "(no context)"
        print(f"| {num} | digit | {ctx} | study / measurement / primary source |  |  |")

    for phrase, ctx in hedges:
        print(f"| {phrase} | hedge | {ctx} | review / survey / expert source |  |  |")

    print()
    print("=" * 72)
    print(f"Rows: {len(numbers)} digit(s) + {len(hedges)} hedge(s)")
    print("Next: fill Source column, then python3 tools/claim_scan.py PATH")
    print("Or: python3 tools/research_package_starter.py PATH for the full skeleton first.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
