#!/usr/bin/env python3
"""Soft check that key sections exist in publish.md.

Reports presence of required metadata sections (title, description, tags, etc.)
so a human does not rediscover missing parts before the OAuth step.
Does not invent text, rewrite files, change hard gates, or require credentials.
Advisory only. Reusable across packets.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"

REQUIRED_SECTIONS = [
    "## Title to upload",
    "## Description",
    "## Tags",
    "## First comment",
]

OPTIONAL_SECTIONS = [
    "## End screen",
    "## Human before upload",
]


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    publish = packet / "publish.md"
    if not publish.is_file():
        print(f"PUBLISH SECTIONS PRESENT: FAIL (publish.md missing in {packet})")
        return 1

    text = publish.read_text(encoding="utf-8")
    missing_req = [s for s in REQUIRED_SECTIONS if s not in text]
    missing_opt = [s for s in OPTIONAL_SECTIONS if s not in text]

    print("PUBLISH SECTIONS PRESENT (soft only; gates unchanged)")
    print(f"Packet: {packet.name}")
    print()
    if missing_req:
        print(f"MISSING REQUIRED: {', '.join(missing_req)}")
        print("ADVISORY: add the missing sections before dispatch review.")
    else:
        print("REQUIRED SECTIONS: all present")
    if missing_opt:
        print(f"MISSING OPTIONAL: {', '.join(missing_opt)} (not blocking)")
    else:
        print("OPTIONAL SECTIONS: all present")
    print()
    print("Human next: docs/human_oauth_checklist.md or python3 tools/human_one_pager.py")
    print("PUBLISH SECTIONS PRESENT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
