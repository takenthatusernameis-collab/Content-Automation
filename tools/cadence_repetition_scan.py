#!/usr/bin/env python3
"""Report cadence (sentence length variation) and repetition signals in spoken WORDS.

Supports the read-aloud pass for cadence and repetition from docs/content_quality.md.
Parses draft.md (preferred) or script.md, extracts WORDS blocks via shared phrase_utils.spoken_words,
computes length statistics (mean, stdev, short/long ratios), and detects repeated
n-grams or near-duplicate phrases that may indicate padding or monotonous delivery.
Does not invent content, rewrite files, or claim authorship. Hits are revision signals.
Complements quality_scan, claim_scan, and the draft coaches by making the final
editorial gate mechanically assisted for every future packet.
"""

from __future__ import annotations

import argparse
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

from phrase_utils import spoken_words

SENTENCE_RE = re.compile(r"[^.!?]+[.!?]+" , re.S)
WORD_TOKEN_RE = re.compile(r"\b[\w'-]+\b")

def sentences(body: str) -> list[str]:
    return [s.strip() for s in SENTENCE_RE.findall(body) if s.strip()]

def sentence_lengths(sents: list[str]) -> list[int]:
    return [len(WORD_TOKEN_RE.findall(s)) for s in sents]

def ngrams(tokens: list[str], n: int) -> list[tuple[str, ...]]:
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cadence and repetition signals on spoken WORDS. No invented content."
    )
    parser.add_argument("packet", help="Packet folder containing draft.md or script.md")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if strong signals remain.")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    source = path / "draft.md"
    if not source.is_file():
        source = path / "script.md"
    if not source.is_file():
        print(f"No draft.md or script.md in {args.packet}", file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8")
    body = spoken_words(text)
    if not body.strip():
        print("No WORDS blocks found.")
        return 0

    sents = sentences(body)
    if len(sents) < 3:
        print("Too few sentences for cadence analysis.")
        return 0

    lengths = sentence_lengths(sents)
    mean_len = statistics.mean(lengths)
    try:
        stdev = statistics.stdev(lengths)
    except statistics.StatisticsError:
        stdev = 0.0
    short = sum(1 for L in lengths if L < 8)
    long_ = sum(1 for L in lengths if L > 25)
    short_pct = 100.0 * short / len(lengths)
    long_pct = 100.0 * long_ / len(lengths)

    tokens = WORD_TOKEN_RE.findall(body.lower())
    bigrams = ngrams(tokens, 2)
    trigrams = ngrams(tokens, 3)
    bi_counts = Counter(bigrams)
    tri_counts = Counter(trigrams)
    repeated_bi = [(k, v) for k, v in bi_counts.items() if v >= 3 and len(k[0]) > 2]
    repeated_tri = [(k, v) for k, v in tri_counts.items() if v >= 2]

    print("CADENCE & REPETITION SCAN (read-aloud assist; revision signals only)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Sentences: {len(sents)}")
    print(f"Mean sentence length: {mean_len:.1f} words")
    print(f"Stdev: {stdev:.1f}")
    print(f"Short (<8 words): {short_pct:.0f}%   Long (>25 words): {long_pct:.0f}%")
    print()
    signals = []
    if stdev < 4.0 and len(sents) > 8:
        signals.append("LOW_VARIATION: sentence lengths are tightly clustered (possible monotonous cadence)")
    if short_pct > 40:
        signals.append("MANY_SHORT: high fraction of very short sentences (possible choppy or list-like delivery)")
    if long_pct > 30:
        signals.append("MANY_LONG: high fraction of long sentences (possible dense or hard-to-follow delivery)")
    if repeated_bi:
        top = sorted(repeated_bi, key=lambda x: -x[1])[:5]
        signals.append(f"REPEATED_BIGRAMS: {len(repeated_bi)} bigrams appear 3+ times (e.g. {' '.join(top[0][0])} x{top[0][1]})")
    if repeated_tri:
        top = sorted(repeated_tri, key=lambda x: -x[1])[:3]
        signals.append(f"REPEATED_TRIGRAMS: {len(repeated_tri)} trigrams appear 2+ times (possible padding)")

    if not signals:
        print("No strong cadence or repetition signals. Cadence looks varied.")
    else:
        print("Signals (revision candidates for the read-aloud pass):")
        for s in signals:
            print(f"  - {s}")
    print()
    print("Next: read the spoken WORDS aloud or scan for the flagged patterns.")
    print("Cut repeated phrases, vary sentence length, or tighten dense sections.")
    print("This tool writes nothing and invents nothing. Prefer human OAuth for publish.")
    if args.strict and signals:
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
