#!/usr/bin/env python3
"""Soft metrics and suggestions for packet tags.

Read-only. Reports tag count, individual lengths, total character length
(YouTube tags total ~500 chars including separators), and soft notes on
count range, overly long tags, or missing mechanism alignment signals.
Does not rewrite publish.md, invent media, call YouTube, or poll secrets.
Exit 0 always (informational). Reduces human labor on tags review for
future videos.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from tags_scan import extract_tags, tags_text  # noqa: E402

IDEAL_MIN_COUNT = 5
IDEAL_MAX_COUNT = 12
IDEAL_MAX_INDIVIDUAL = 40
HARD_TOTAL_CHARS = 500  # YouTube total tags limit (approx, including commas/spaces)


def analyze(tags: list[str]) -> dict:
    count = len(tags)
    lengths = [len(t) for t in tags]
    total_chars = sum(lengths) + max(0, count - 1) * 2  # rough separator estimate
    long_ones = [t for t in tags if len(t) > IDEAL_MAX_INDIVIDUAL]
    short_ones = [t for t in tags if len(t) < 3]
    return {
        "count": count,
        "lengths": lengths,
        "total_chars": total_chars,
        "long_ones": long_ones,
        "short_ones": short_ones,
        "tags": tags,
    }


def suggestions(m: dict) -> list[str]:
    sug = []
    if m["count"] < IDEAL_MIN_COUNT:
        sug.append(f"few tags ({m['count']}; ideal ~{IDEAL_MIN_COUNT}-{IDEAL_MAX_COUNT})")
    elif m["count"] > IDEAL_MAX_COUNT:
        sug.append(f"many tags ({m['count']}; may dilute relevance)")
    if m["total_chars"] > HARD_TOTAL_CHARS:
        sug.append(f"total chars high ({m['total_chars']} approx > {HARD_TOTAL_CHARS} limit)")
    if m["long_ones"]:
        sug.append(f"{len(m['long_ones'])} tag(s) over {IDEAL_MAX_INDIVIDUAL} chars")
    if m["short_ones"]:
        sug.append(f"{len(m['short_ones'])} very short tag(s)")
    if m["count"] == 0:
        sug.append("no tags present; add mechanism-aligned ones")
    return sug


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Soft tags length/count/metrics suggestions (read-only)."
    )
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    packet = args.packet.resolve()
    pub = packet / "publish.md"
    if not pub.is_file():
        print(f"TAGS_METRICS_SUGGEST: publish.md absent at {pub}")
        return 2

    text = pub.read_text(encoding="utf-8")
    body = tags_text(text)
    print("TAGS METRICS SUGGEST (soft; for human editor; does not rewrite)")
    print(f"Packet: {packet.name}")
    print(f"Ideal: {IDEAL_MIN_COUNT}-{IDEAL_MAX_COUNT} tags, each <= {IDEAL_MAX_INDIVIDUAL} chars, total ~under {HARD_TOTAL_CHARS}")
    print()
    if not body:
        print("No Tags section found.")
        return 0

    tags = extract_tags(body)
    m = analyze(tags)
    sug = suggestions(m)
    print(f"Tags: {m['count']} count, ~{m['total_chars']} total chars")
    if tags:
        print("  Sample: " + "; ".join(tags[:5]))
    if m["long_ones"]:
        print(f"  long: {', '.join(m['long_ones'][:3])}")
    if sug:
        print(f"  notes: {'; '.join(sug)}")
    else:
        print("  looks balanced")
    print()
    print("Human: use as signals only; prefer mechanism-aligned specific tags; run tags_scan.py after changes.")
    print("Does not rewrite publish.md, does not upload, does not invent media.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
