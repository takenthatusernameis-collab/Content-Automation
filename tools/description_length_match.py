#!/usr/bin/env python3
"""Soft description length match for a packet.

Extracts the text under '## Description' from publish.md and reports character
count against YouTube's hard 5000-character description limit. Notes overflow
or very short descriptions. Does not change hard gates, invent text, rewrite
publish.md, poll secrets, or write files. Reusable across packets.
Complements title length, tags length, and thumbnail soft reports.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
HARD_LIMIT = 5000
SOFT_MIN = 100  # practical minimum for a useful description; soft only


def extract_section(text: str, header: str) -> str:
    lines = text.splitlines()
    capture = False
    collected = []
    for line in lines:
        if line.strip() == header:
            capture = True
            continue
        if capture and line.startswith("## ") and line.strip() != header:
            break
        if capture:
            collected.append(line)
    return "\n".join(collected).strip()


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"not a directory: {packet}", file=sys.stderr)
        return 1

    publish = packet / "publish.md"
    print("DESCRIPTION LENGTH MATCH (soft only; gates unchanged)")
    print(f"Packet: {packet.name}")
    print()

    if not publish.is_file():
        print("publish.md: not present")
        print("DESCRIPTION LENGTH MATCH PASS (soft)")
        return 0

    text = publish.read_text(encoding="utf-8")
    desc = extract_section(text, "## Description")

    if not desc:
        print("Description: missing or empty under ## Description")
        print("DESCRIPTION LENGTH MATCH PASS (soft)")
        return 0

    n = len(desc)
    print(f"Description characters: {n}")
    print(f"Hard limit (YouTube): {HARD_LIMIT}")

    if n > HARD_LIMIT:
        print(f"HARD LIMIT: exceeded by {n - HARD_LIMIT} characters (YouTube will reject or truncate)")
        print("NOTE: shorten the description; soft only, review intent.")
    else:
        print("HARD LIMIT: ok")
        remaining = HARD_LIMIT - n
        print(f"Remaining headroom: {remaining} characters")

    if n < SOFT_MIN:
        print(f"SOFT MINIMUM: under {SOFT_MIN} characters (may be too brief for search/context; soft only)")
    else:
        print(f"SOFT MINIMUM ({SOFT_MIN}): ok")

    print()
    print("Human next: docs/human_oauth_checklist.md or python3 tools/human_one_pager.py")
    print("DESCRIPTION LENGTH MATCH PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
