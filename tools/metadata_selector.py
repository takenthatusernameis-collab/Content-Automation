#!/usr/bin/env python3
"""Recommend highest-alignment metadata candidates for publish.md selection.

Reads the primary assignment via assignment_utils.read_primary.
Scores candidates in the local options files by key-term overlap (from the primary)
plus simple length fitness. Prints ranked recommendations per field so a human
or later step can copy the best ones into publish.md with less manual comparison.

Does not write publish.md or invent options. Pure ranking over existing candidates.
Compounds the assignment-source consistency and alignment scan.
Exit 0 always (informational).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from assignment_utils import read_primary  # noqa: E402
from phrase_utils import shorten  # noqa: E402


def extract_key_terms(primary: str) -> list[str]:
    stops = {"the", "a", "an", "so", "stops", "reopening", "the", "list", "install", "with", "for"}
    words = re.findall(r"\b[a-zA-Z']{4,}\b", primary.lower())
    terms = [w for w in words if w not in stops][:5]
    return terms or [shorten(primary, 24).lower()]


def score_candidate(cand: str, terms: list[str], ideal_len: tuple[int, int]) -> tuple[int, str]:
    """Return (score, reason). Higher is better."""
    lower = cand.lower()
    term_hits = sum(1 for t in terms if t in lower)
    # Length fitness: prefer within ideal range
    length = len(cand)
    lo, hi = ideal_len
    if lo <= length <= hi:
        len_bonus = 2
    elif length < lo:
        len_bonus = 0
    else:
        len_bonus = 1 if length < hi + 20 else 0
    score = term_hits * 3 + len_bonus
    reason = f"terms={term_hits}/{len(terms)} len={length}"
    return score, reason


def extract_candidates(path: Path) -> list[str]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    cands = []
    in_cands = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Candidates") or stripped.startswith("## Options") or (
            "candidates" in stripped.lower() and stripped.startswith("##")
        ):
            in_cands = True
            continue
        if in_cands and stripped.startswith("##"):
            break
        if in_cands and re.match(r"^\d+\.\s+", stripped):
            # strip the number
            body = re.sub(r"^\d+\.\s+", "", stripped)
            cands.append(body)
    if not cands:
        cands = [
            re.sub(r"^\d+\.\s+", "", line.strip())
            for line in text.splitlines()
            if re.match(r"^\d+\.\s+", line.strip())
        ]
    return cands


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rank metadata options candidates by alignment to assignment primary"
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"FAIL: not a directory: {packet}", file=sys.stderr)
        return 1

    primary = read_primary(packet)
    if not primary:
        print("INFO: no assignment_source.md primary. Run tools/assignment_source_writer.py first.")
        print("Selector skipped.")
        return 0

    terms = extract_key_terms(primary)
    print(f"Primary: {primary}")
    print(f"Key terms: {terms}")
    print()

    # (filename, ideal length range for that field)
    fields = [
        ("title_options.md", (40, 70)),
        ("description_options.md", (80, 200)),
        ("thumbnail_options.md", (8, 28)),
        ("first_comment_options.md", (40, 120)),
        ("end_screen_options.md", (20, 60)),
        ("tags_options.md", (5, 40)),
    ]

    any_recs = False
    for fname, ideal in fields:
        path = packet / fname
        cands = extract_candidates(path)
        if not cands:
            print(f"{fname}: no candidates")
            continue
        any_recs = True
        scored = []
        for c in cands:
            sc, reason = score_candidate(c, terms, ideal)
            scored.append((sc, c, reason))
        scored.sort(key=lambda x: -x[0])
        best = scored[0]
        print(f"{fname}:")
        print(f"  recommended: {best[1]}")
        print(f"  score={best[0]} ({best[2]})")
        if len(scored) > 1:
            print(f"  runner-up: {scored[1][1]} (score={scored[1][0]})")
        print()

    if any_recs:
        print("Recommendations complete. Copy preferred lines into publish.md. No files written.")
    else:
        print("No options files with candidates. Generate them first.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
