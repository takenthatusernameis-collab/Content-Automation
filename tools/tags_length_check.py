#!/usr/bin/env python3
"""Check YouTube tags total character budget against the 500-char hard limit.

Reads publish.md ## Tags section, extracts bullet tags, and reports:
- number of tags
- per-tag character lengths
- estimated total characters as YouTube counts them (tags joined by commas;
  multi-word tags wrapped in quotes that also count)
Flags total over 500. Provides context for revision. Does not rewrite files.
Reduces recurring manual counting of the combined tag string before publish
on every future packet.

Uses shared phrase_utils.normalize. Complements tags_scan (quality) with length.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import normalize  # noqa: E402

TAGS_RE = re.compile(r"## Tags\s*\n(.*?)(?=\n## |\Z)", re.S)
BULLET_RE = re.compile(r"^-\s+(.+)$", re.M)
HARD_TOTAL_MAX = 500
IDEAL_TAG_COUNT_MIN = 5
IDEAL_TAG_COUNT_MAX = 15


def tags_body(text: str) -> str:
    m = TAGS_RE.search(text.replace("\r\n", "\n"))
    return m.group(1).strip() if m else ""


def extract_tags(body: str) -> list[str]:
    return [normalize(m.group(1).strip()) for m in BULLET_RE.finditer(body) if m.group(1).strip()]


def youtube_counted_length(tags: list[str]) -> int:
    """Estimate characters YouTube counts: join with commas, +2 quotes per multi-word tag."""
    if not tags:
        return 0
    # Join with commas (comma counts)
    joined = ",".join(tags)
    # Add 2 for each tag that contains a space (implied quotes)
    extra = sum(2 for t in tags if " " in t)
    return len(joined) + extra


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report YouTube tags length vs 500-char total budget. No file writes."
    )
    parser.add_argument("packet", type=Path)
    parser.add_argument("--strict", action="store_true", help="Exit 1 on total over hard max")
    args = parser.parse_args()

    path = args.packet.resolve()
    pub_path = path / "publish.md"
    if not pub_path.is_file():
        print("no publish.md")
        return 0

    text = pub_path.read_text(encoding="utf-8")
    body = tags_body(text)
    if not body:
        print("no Tags section extracted")
        return 0

    tags = extract_tags(body)
    if not tags:
        print("no tags extracted")
        return 0

    counted = youtube_counted_length(tags)
    print("TAGS LENGTH CHECK (YouTube: 500 characters total including commas and quotes for spaces)")
    print(f"Packet: {path.name}")
    print(f"Tag count: {len(tags)}")
    print()
    for i, tag in enumerate(tags, 1):
        n = len(tag)
        print(f"{i}. {n:3d} chars  {tag}")
    print()
    print(f"Estimated YouTube-counted total: {counted} / {HARD_TOTAL_MAX}")
    issues = 0
    if counted > HARD_TOTAL_MAX:
        print(f"[TOO_LONG] exceeds hard max by {counted - HARD_TOTAL_MAX} characters")
        issues += 1
    else:
        print("[OK] under hard limit")
    if not (IDEAL_TAG_COUNT_MIN <= len(tags) <= IDEAL_TAG_COUNT_MAX):
        print(f"[COUNT] {len(tags)} tags (prefer {IDEAL_TAG_COUNT_MIN}-{IDEAL_TAG_COUNT_MAX} focused tags)")
        # count is advisory, not a hard issue for exit
    print()
    if issues == 0:
        print("Tags length within recommended budget.")
        return 0
    print("Prefer fewer, more specific tags so the combined string stays under 500.")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
