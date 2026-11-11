#!/usr/bin/env python3
"""Soft metrics and suggestions for packet descriptions.

Read-only. Reports character/word counts against YouTube-friendly ranges
(first ~125 chars matter for search snippets; total under 5000), and soft
notes on structure elements (timestamps, links, CTAs, questions) if absent.
Does not rewrite publish.md, invent media, call YouTube, or poll secrets.
Exit 0 always (informational). Reduces human labor on description review
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

from description_scan import description_text  # noqa: E402

IDEAL_FIRST_CHARS = 125  # search snippet priority
IDEAL_MIN_CHARS = 200
IDEAL_MAX_CHARS = 2500
HARD_MAX_CHARS = 5000

TIMESTAMP_RE = re.compile(r"\b\d{1,2}:\d{2}\b")
LINK_RE = re.compile(r"https?://\S+")
CTA_WORDS = {"subscribe", "comment", "like", "share", "watch", "check"}
QUESTION_RE = re.compile(r"\?")


def analyze(text: str) -> dict:
    text = text.strip()
    chars = len(text)
    words = text.split()
    word_count = len(words)
    first_125 = text[:IDEAL_FIRST_CHARS]
    has_timestamp = bool(TIMESTAMP_RE.search(text))
    has_link = bool(LINK_RE.search(text))
    lower = text.lower()
    cta_hits = [w for w in CTA_WORDS if w in lower]
    has_question = bool(QUESTION_RE.search(text))
    return {
        "text": text,
        "chars": chars,
        "words": word_count,
        "first_125": first_125,
        "has_timestamp": has_timestamp,
        "has_link": has_link,
        "cta_hits": cta_hits,
        "has_question": has_question,
    }


def suggestions(m: dict) -> list[str]:
    sug = []
    if m["chars"] < IDEAL_MIN_CHARS:
        sug.append(f"short ({m['chars']} chars; ideal ~{IDEAL_MIN_CHARS}-{IDEAL_MAX_CHARS})")
    elif m["chars"] > IDEAL_MAX_CHARS:
        sug.append(f"long ({m['chars']} chars; consider trimming)")
    if m["chars"] > HARD_MAX_CHARS:
        sug.append(f"exceeds YouTube limit ({m['chars']} > {HARD_MAX_CHARS})")
    if not m["has_timestamp"]:
        sug.append("consider timestamps (e.g. 0:00) for chapters/navigation if natural")
    if not m["has_link"]:
        sug.append("consider a relevant link (channel, related, source) if available")
    if not m["cta_hits"]:
        sug.append("optional soft CTA (subscribe/comment) if fits voice; avoid engagement bait")
    if not m["has_question"]:
        sug.append("consider a question for engagement if natural")
    return sug


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Soft description length/structure metrics suggestions (read-only)."
    )
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    packet = args.packet.resolve()
    pub = packet / "publish.md"
    if not pub.is_file():
        print(f"DESCRIPTION_METRICS_SUGGEST: publish.md absent at {pub}")
        return 2

    text = pub.read_text(encoding="utf-8")
    body = description_text(text)
    print("DESCRIPTION METRICS SUGGEST (soft; for human editor; does not rewrite)")
    print(f"Packet: {packet.name}")
    print(f"Ideal: first ~{IDEAL_FIRST_CHARS} chars for search; total ~{IDEAL_MIN_CHARS}-{IDEAL_MAX_CHARS} chars")
    print()
    if not body:
        print("No Description section found.")
        return 0

    m = analyze(body)
    sug = suggestions(m)
    print(f"Description: {m['chars']} chars, {m['words']} words")
    print(f"  First 125: {m['first_125'][:80]}...")
    if m["has_timestamp"]:
        print("  has timestamp(s)")
    if m["has_link"]:
        print("  has link(s)")
    if m["cta_hits"]:
        print(f"  CTA words: {', '.join(m['cta_hits'][:3])}")
    if m["has_question"]:
        print("  has question")
    if sug:
        print(f"  notes: {'; '.join(sug)}")
    else:
        print("  looks balanced")
    print()
    print("Human: use as signals only; preserve channel voice, honesty, and anti-slop rules.")
    print("Does not rewrite publish.md, does not upload, does not invent media.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
