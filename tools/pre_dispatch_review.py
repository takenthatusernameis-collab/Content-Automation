#!/usr/bin/env python3
"""Print a concise, fail-closed human review of the packet that will be uploaded.

One command so the human can glance at title, description excerpt, tags, and
expected master fingerprint before completing the OAuth checklist and dispatch.
Does not poll secrets, invent values, dispatch, or write files.
Reusable for future packets once they exist.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
EXPECTED_MASTER_SHA = "4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546"
DISPATCH = (
    "gh workflow dispatch youtube-production.yml "
    "--repo takenthatusernameis-collab/Content-Automation "
    "-f execute=true -f collect_feedback=false"
)


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
    publish = packet / "publish.md"
    if not publish.is_file():
        print(f"PRE_DISPATCH_REVIEW FAIL: publish.md missing in {packet}")
        return 1

    text = publish.read_text(encoding="utf-8")
    title = extract_section(text, "## Title to upload").splitlines()
    title = title[0].strip() if title else ""
    desc = extract_section(text, "## Description")
    tags = extract_section(text, "## Tags")

    if not title:
        print("PRE_DISPATCH_REVIEW FAIL: title missing")
        return 1
    if not desc:
        print("PRE_DISPATCH_REVIEW FAIL: description missing")
        return 1

    desc_lines = [ln.strip() for ln in desc.splitlines() if ln.strip()][:4]
    tag_lines = [ln.strip().lstrip("- ").strip() for ln in tags.splitlines() if ln.strip().startswith("-")]

    print("PRE-DISPATCH REVIEW (fail-closed; no secret poll, no invent)")
    print(f"packet: {packet.name}")
    print()
    print(f"TITLE: {title}")
    print()
    print("DESCRIPTION EXCERPT:")
    for ln in desc_lines:
        print(f"  {ln}")
    print()
    print(f"TAGS ({len(tag_lines)}): {', '.join(tag_lines[:8])}")
    print()
    print(f"EXPECTED MASTER SHA256 (q1-media-r253):")
    print(f"  {EXPECTED_MASTER_SHA}")
    print("  Do not use the truncated r249 master.")
    print()
    print("DISPATCH (once, after secrets exist):")
    print(f"  {DISPATCH}")
    print()
    print("Next human step: docs/human_oauth_checklist.md (estimated 10-20 min).")
    print("Then confirm private provider_video_id before any further dispatch.")
    print("PRE_DISPATCH_REVIEW PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
