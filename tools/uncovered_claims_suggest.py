#!/usr/bin/env python3
"""Suggest research directions for uncovered claims without inventing sources.

Reuses claim extraction and coverage logic from sources_validator patterns.
For each uncovered digit or hedge, prints a soft category suggestion and
example search query style (no actual search, no invented URLs or numbers).
Reduces recurring labor of manually deciding where to look for sources
before filling sources.md / research.md. Soft only; does not gate or write.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import (
    HEDGE_PATTERNS,
    compile_word_boundary_patterns,
    spoken_words,
)
from research_brief import numbers_in_spoken_words  # type: ignore

PLACEHOLDERS = {"", " ", "placeholder", "tbd", "todo", "fill", "n/a", "none", "-", "—"}


def unique_preserve(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for it in items:
        key = it.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append(it.strip())
    return out


def extract_claims(text: str) -> tuple[list[str], list[str]]:
    numbers = unique_preserve(numbers_in_spoken_words(text))
    body = spoken_words(text)
    _HEDGE_RES = compile_word_boundary_patterns(HEDGE_PATTERNS)
    hedges = []
    for phrase, cre in zip(HEDGE_PATTERNS, _HEDGE_RES):
        if cre.search(body):
            hedges.append(phrase)
    return numbers, hedges


def is_placeholder(val: str) -> bool:
    return val.strip().lower() in PLACEHOLDERS


def extract_sources_from_md(md_text: str) -> list[str]:
    sources = []
    for line in md_text.splitlines():
        if line.strip().startswith("|") and "|" in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2 and not is_placeholder(cells[1]):
                sources.append(cells[1])
        elif line.strip().startswith(("-", "*", "1.", "2.")) and not is_placeholder(line.strip(" -*0123456789.")):
            sources.append(line.strip())
    return unique_preserve(sources)


def suggest_for_claim(claim: str, is_digit: bool) -> str:
    if is_digit:
        return "Look for primary studies, official statistics, or measurement papers that report this exact figure or range. Prefer sources with methodology."
    return "Look for systematic reviews, survey summaries, or expert consensus documents that discuss this hedge. Prefer recent, citable overviews."


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest research directions for uncovered claims. No invented sources or searches."
    )
    parser.add_argument("packet", help="Packet folder")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    script_path = path / "script.md"
    draft_path = path / "draft.md"
    chosen = script_path if script_path.is_file() else (draft_path if draft_path.is_file() else None)
    if chosen is None:
        print("No script.md or draft.md found.")
        return 0

    text = chosen.read_text(encoding="utf-8")
    numbers, hedges = extract_claims(text)
    all_claims = [(c, True) for c in numbers] + [(c, False) for c in hedges]

    sources_files = [path / "sources.md", path / "research.md"]
    all_sources: list[str] = []
    for sf in sources_files:
        if sf.is_file():
            all_sources.extend(extract_sources_from_md(sf.read_text(encoding="utf-8")))
    all_sources = unique_preserve(all_sources)

    print("UNCOVERED CLAIMS RESEARCH SUGGEST (soft directions only; no invent, no search)")
    print(f"Script source: {chosen.name}")
    print()

    if not all_claims:
        print("No claims detected. Nothing to suggest.")
        return 0

    uncovered = []
    for claim, is_digit in all_claims:
        cl = claim.lower()
        hit = any(cl in s.lower() or any(word in s.lower() for word in cl.split() if len(word) > 3) for s in all_sources)
        if not hit:
            uncovered.append((claim, is_digit))

    if not uncovered:
        print("All detected claims appear covered by existing non-placeholder sources.")
        print("Next: python3 tools/claim_scan.py", path)
        return 0

    print(f"Uncovered claims: {len(uncovered)}")
    print("Suggested research directions (fill real sources yourself; do not invent):")
    print()
    for claim, is_digit in uncovered:
        cat = "digit/quantitative" if is_digit else "hedge/qualitative"
        sugg = suggest_for_claim(claim, is_digit)
        print(f"- Claim: {claim} ({cat})")
        print(f"  Direction: {sugg}")
        print(f"  Example query style: \"{claim} study\" or \"{claim} review\" (run manually)")
        print()

    print("After filling sources.md or research.md with real citations:")
    print("  python3 tools/sources_validator.py", path)
    print("  python3 tools/claim_scan.py", path)
    print("Do not invent sources. Human OAuth remains the publish blocker.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
