#!/usr/bin/env python3
"""Soft tags length match for a packet.

Extracts the Tags section from publish.md, sums character counts of individual
tags (bullet items), and reports against YouTube's hard 500-character combined
tags limit. Notes overflow. Does not change hard gates, invent tags, rewrite
publish.md, poll secrets, or write files. Reusable across packets.
Complements title length and thumbnail soft reports.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
HARD_LIMIT = 500

TAGS_RE = re.compile(r"## Tags\s*\n(.*?)(?=\n## |\Z)", re.S)
BULLET_RE = re.compile(r"^-\s+(.+)$", re.M)


def extract_tags(text: str) -> list[str]:
    m = TAGS_RE.search(text.replace("\r\n", "\n"))
    if not m:
        return []
    body = m.group(1).strip()
    return [m.group(1).strip() for m in BULLET_RE.finditer(body) if m.group(1).strip()]


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"not a directory: {packet}", file=sys.stderr)
        return 1

    publish = packet / "publish.md"
    print("TAGS LENGTH MATCH (soft only; gates unchanged)")
    print(f"Packet: {packet.name}")
    print()

    if not publish.is_file():
        print("publish.md: not present")
        print("TAGS LENGTH MATCH PASS (soft)")
        return 0

    text = publish.read_text(encoding="utf-8")
    tags = extract_tags(text)

    if not tags:
        print("Tags: missing or empty under ## Tags")
        print("TAGS LENGTH MATCH PASS (soft)")
        return 0

    lengths = [len(t) for t in tags]
    total = sum(lengths)
    print(f"Tag count: {len(tags)}")
    print(f"Individual lengths: {lengths}")
    print(f"Combined character count (sum of tag texts): {total}")
    print(f"Hard limit (YouTube combined tags): {HARD_LIMIT}")

    if total > HARD_LIMIT:
        print(f"HARD LIMIT: exceeded by {total - HARD_LIMIT} characters (YouTube will reject or truncate)")
        print("NOTE: shorten or remove tags; soft only, review intent.")
    else:
        print("HARD LIMIT: ok")
        remaining = HARD_LIMIT - total
        print(f"Remaining headroom: {remaining} characters")

    print()
    print("Human next: docs/human_oauth_checklist.md or python3 tools/human_one_pager.py")
    print("TAGS LENGTH MATCH PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
