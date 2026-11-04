#!/usr/bin/env python3
"""Soft title length match for a packet.

Extracts the first line under '## Title to upload' from publish.md and reports
character count against YouTube's hard 100-character limit and the practical
~60-character guideline for full mobile visibility without truncation.
When over the soft guideline, notes the overflow. Does not change hard gates,
invent text, rewrite titles, poll secrets, or write files.
Reusable across packets. Complements thumbnail soft reports.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
HARD_LIMIT = 100
SOFT_VISIBLE = 60


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
    print("TITLE LENGTH MATCH (soft only; gates unchanged)")
    print(f"Packet: {packet.name}")
    print()

    if not publish.is_file():
        print("publish.md: not present")
        print("TITLE LENGTH MATCH PASS (soft)")
        return 0

    text = publish.read_text(encoding="utf-8")
    title_block = extract_section(text, "## Title to upload")
    title_lines = title_block.splitlines()
    title = title_lines[0].strip() if title_lines else ""

    if not title:
        print("Title: missing or empty under ## Title to upload")
        print("TITLE LENGTH MATCH PASS (soft)")
        return 0

    n = len(title)
    print(f"Title: {title}")
    print(f"Characters: {n}")
    print(f"Hard limit (YouTube): {HARD_LIMIT}")
    print(f"Soft visibility guideline (mobile full display): {SOFT_VISIBLE}")

    if n > HARD_LIMIT:
        print(f"HARD LIMIT: exceeded by {n - HARD_LIMIT} characters (will be truncated by YouTube)")
    else:
        print("HARD LIMIT: ok")

    if n > SOFT_VISIBLE:
        print(f"SOFT VISIBILITY: exceeds by {n - SOFT_VISIBLE} characters (may truncate on mobile)")
        print("NOTE: shorter titles often improve click-through on mobile; soft only, review intent.")
    else:
        print("SOFT VISIBILITY: within guideline")

    print()
    print("Human next: docs/human_oauth_checklist.md or python3 tools/human_one_pager.py")
    print("TITLE LENGTH MATCH PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
