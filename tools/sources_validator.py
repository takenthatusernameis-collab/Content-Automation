#!/usr/bin/env python3
"""Validate that packet sources cover detected claims without inventing sources.

Extracts quantitative digits and hedge phrases from script.md (or draft.md).
Scans sources.md and research.md for non-placeholder Source cells or bullets.
Reports coverage: claims with at least one plausible source mention vs uncovered.
Does not invent citations, URLs, or numbers. Does not write files or call APIs.
Soft signal only; does not gate status. Reduces manual cross-check labor before claim_scan.
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
    """Pull non-placeholder Source column values and non-placeholder bullets."""
    sources = []
    # Simple table row parser for | Claim | Source | ...
    for line in md_text.splitlines():
        if line.strip().startswith("|") and "|" in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2 and not is_placeholder(cells[1]):
                sources.append(cells[1])
        elif line.strip().startswith(("-", "*", "1.", "2.")) and not is_placeholder(line.strip(" -*0123456789.")):
            sources.append(line.strip())
    return unique_preserve(sources)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report claim-to-source coverage from script vs sources.md/research.md. No invented sources."
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
        print("No script.md or draft.md found. Nothing to validate.")
        return 0

    text = chosen.read_text(encoding="utf-8")
    numbers, hedges = extract_claims(text)
    all_claims = numbers + hedges

    sources_files = [path / "sources.md", path / "research.md"]
    all_sources: list[str] = []
    for sf in sources_files:
        if sf.is_file():
            all_sources.extend(extract_sources_from_md(sf.read_text(encoding="utf-8")))
    all_sources = unique_preserve(all_sources)

    print("SOURCES VALIDATOR (coverage report; no invent, no writes)")
    print(f"Script source: {chosen.name}")
    print(f"Claims detected: {len(all_claims)} ({len(numbers)} digits, {len(hedges)} hedges)")
    print(f"Non-placeholder sources found: {len(all_sources)}")
    print()

    if not all_claims:
        print("No claims requiring sources detected. claim_scan should pass these signals.")
        return 0

    if not all_sources:
        print("NO SOURCES FILE CONTENT. Fill sources.md or research.md with real citations before claim_scan.")
        print("Uncovered claims:")
        for c in all_claims:
            print(f"  - {c}")
        return 0

    # Simple coverage: claim text appears in any source string or vice-versa (case-insensitive)
    covered = []
    uncovered = []
    for claim in all_claims:
        cl = claim.lower()
        hit = any(cl in s.lower() or any(word in s.lower() for word in cl.split() if len(word) > 3) for s in all_sources)
        (covered if hit else uncovered).append(claim)

    print(f"Covered: {len(covered)} / {len(all_claims)}")
    if covered:
        print("Likely covered (claim text or key words appear in a source):")
        for c in covered:
            print(f"  + {c}")
    if uncovered:
        print()
        print("Uncovered (no matching source text found; fill Source column or bullets):")
        for c in uncovered:
            print(f"  - {c}")
    print()
    print("Next: python3 tools/claim_scan.py", path)
    print("Do not invent sources. Human OAuth remains the publish blocker.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
