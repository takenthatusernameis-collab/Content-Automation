#!/usr/bin/env python3
"""Check generated install notes for channel voice compliance.

Scans install_package.md (or other install notes) for engagement-bait phrases
and confirms presence of operational language grounded in the packet.
No writes by default. No invented content. Stdlib only.
Reduces recurring human review labor on every future packet.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BANNED_PHRASES = [
    "like and subscribe",
    "smash that like",
    "comment below",
    "what do you think",
    "let me know in the comments",
    "hit the bell",
    "don't forget to",
    "make sure to like",
]

OPERATIONAL_MARKERS = [
    "install this default",
    "the stall is",
    "it lives",
    "write the default",
    "do the first",
    "leave the default visible",
    "point at the default",
]


def check_text(text: str) -> tuple[bool, list[str]]:
    lower = text.lower()
    issues: list[str] = []
    for phrase in BANNED_PHRASES:
        if phrase in lower:
            issues.append(f"banned phrase: {phrase}")
    has_operational = any(m in lower for m in OPERATIONAL_MARKERS)
    if not has_operational:
        issues.append("missing operational markers (install/stall/lives/write/do/leave/point)")
    return len(issues) == 0, issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Check install note voice compliance")
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--file", default="install_package.md", help="Note file to check")
    args = parser.parse_args()

    packet = args.packet.resolve()
    note = packet / args.file
    if not note.is_file():
        print(f"FAIL: {note} missing (run the generator first)", file=sys.stderr)
        return 2

    text = note.read_text(encoding="utf-8")
    ok, issues = check_text(text)
    if ok:
        print(f"PASS: {note} voice-compliant (no banned phrases, operational markers present)")
        return 0
    print(f"FAIL: {note} voice issues:", file=sys.stderr)
    for issue in issues:
        print(f"  - {issue}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
