#!/usr/bin/env python3
"""Print a structured human-friendly metadata spot-check list.

Parses existing title/description/tags candidates in a packet (does not rewrite or invent content).
Prints primary title length, description length, tag count, and soft flags
(title too long/short, desc too short, missing tags, keyword density soft hints)
so a human can scan faster than opening multiple files. Hard gates remain elsewhere
(metadata_alignment_scan, publish_brief locks, youtube_upload dry-run).
Reduces recurring metadata review minutes across future videos.
Does not call YouTube, does not encode, does not write files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _extract_section(md: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)"
    m = re.search(pattern, md, re.M | re.S)
    if not m:
        return ""
    body = m.group(1).strip()
    lines = [ln for ln in body.splitlines() if ln.strip() and not ln.strip().startswith("##")]
    return "\n".join(lines).strip()


def _first_line(text: str) -> str:
    for ln in text.splitlines():
        s = ln.strip()
        if s and not s.startswith("#") and not s.startswith("-"):
            return s
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print structured metadata spot-check list (no invent, no write)."
    )
    parser.add_argument("packet", type=Path, help="Packet folder")
    args = parser.parse_args()
    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}")
        return 1

    # Prefer metadata_bundle.md, fall back to individual files
    bundle_path = packet / "metadata_bundle.md"
    titles_path = packet / "titles.md"
    desc_path = packet / "description.md"
    tags_path = packet / "tags.md"
    publish_path = packet / "publish.md"

    title = ""
    desc = ""
    tags = ""
    source = "none"

    if bundle_path.is_file():
        text = bundle_path.read_text(encoding="utf-8", errors="replace")
        title = _extract_section(text, "Title (Primary)") or _first_line(_extract_section(text, "Title"))
        desc = _extract_section(text, "Description")
        tags = _extract_section(text, "Tags")
        source = "metadata_bundle.md"
    else:
        if titles_path.is_file():
            text = titles_path.read_text(encoding="utf-8", errors="replace")
            title = _extract_section(text, "Primary") or _first_line(text)
            source = "titles.md"
        if desc_path.is_file():
            text = desc_path.read_text(encoding="utf-8", errors="replace")
            desc = _extract_section(text, "Suggested text") or text.strip()
            if source == "none":
                source = "description.md"
        if tags_path.is_file():
            text = tags_path.read_text(encoding="utf-8", errors="replace")
            tags = _extract_section(text, "Suggested tags") or text.strip()
            if source == "none":
                source = "tags.md"

    if not title and not desc and not tags:
        print(f"No metadata candidates found in {packet}")
        print("Look for metadata_bundle.md, titles.md, description.md, or tags.md.")
        print("Hard gates remain: metadata_alignment_scan.py, publish_brief locks.")
        return 1

    print("METADATA SPOTCHECK ASSISTANT (structured review list; no invent, no write)")
    print(f"Packet: {packet}")
    print(f"Source: {source}")
    print("Hard gates remain: metadata_alignment_scan.py (if present), youtube_upload dry-run, publish.md locks.")
    print("=" * 70)
    print()

    flags = []
    # Title checks (YouTube title max 100; soft prefer <=60 for readability)
    if title:
        tlen = len(title)
        print(f"Title ({tlen} chars): {title}")
        if tlen > 100:
            flags.append("title_over_100")
        elif tlen > 70:
            flags.append("title_long")
        elif tlen < 20:
            flags.append("title_short")
    else:
        print("Title: (missing)")
        flags.append("missing_title")

    # Description
    if desc:
        dlen = len(desc)
        print(f"Description ({dlen} chars):")
        print(f"  {desc[:200]}{'...' if len(desc) > 200 else ''}")
        if dlen < 50:
            flags.append("desc_short")
        elif dlen > 5000:
            flags.append("desc_over_limit")
    else:
        print("Description: (missing)")
        flags.append("missing_desc")

    # Tags
    if tags:
        tag_list = [t.strip() for t in re.split(r"[,\n]", tags) if t.strip()]
        print(f"Tags ({len(tag_list)}): {', '.join(tag_list[:15])}{'...' if len(tag_list) > 15 else ''}")
        if len(tag_list) < 3:
            flags.append("few_tags")
        if len(tag_list) > 30:
            flags.append("many_tags")
    else:
        print("Tags: (missing)")
        flags.append("missing_tags")

    print()
    if flags:
        print("Soft flags (human still verifies):")
        for f in flags:
            print(f"  - {f}")
    else:
        print("No soft flags raised.")
    print()
    print("These flags are soft hints only. Review against channel voice in docs/channel.md.")
    print("Spot-check time is reduced by scanning this list instead of opening multiple metadata files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
