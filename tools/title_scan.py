#!/usr/bin/env python3
"""Report shouted title words and an explicit thumbnail mismatch.

Does not rewrite titles.md or thumbnail.md. A word of two or more letters
that is all capitals is a hit, except one acronym of two to four letters in
that title. "Matches title: No" is a hit. A missing titles.md is not a hit.
Default exit is 0 so a clear packet cannot fail the build. --strict exits 1
when any hit remains. set_status.py refuses ready_for_vo while a hit remains.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from validate_packet import titles_from  # noqa: E402

WORD_RE = re.compile(r"[A-Za-z][A-Za-z']*")
MATCH_RE = re.compile(r"^Matches title:[ \t]*([^\n]*)$", re.M)


def shouted(title: str) -> list[str]:
    words = WORD_RE.findall(title)
    caps = [word for word in words if len(word) >= 2 and word.isupper()]
    long = [word for word in caps if len(word) >= 5]
    short = [word for word in caps if len(word) <= 4]
    # One 2-4 letter token can be an acronym (API, ADHD). Two of them, or any
    # 5+ letter shout (GRIND), is the production-rule miss.
    if long or len(short) > 1:
        return caps
    return []


def hits(titles_text: str, thumb_text: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for title in titles_from(titles_text):
        for word in shouted(title):
            found.append(("shout", f"{word} in {title}"))
    match = MATCH_RE.search(thumb_text or "")
    if match and match.group(1).strip().lower().startswith("no"):
        found.append(("thumb", match.group(1).strip()))
    return found


def scan_path(path: Path) -> list[tuple[str, str]]:
    titles = path / "titles.md"
    if not titles.is_file():
        return []
    thumb_path = path / "thumbnail.md"
    thumb = thumb_path.read_text(encoding="utf-8") if thumb_path.is_file() else ""
    return hits(titles.read_text(encoding="utf-8"), thumb)


def main() -> int:
    parser = argparse.ArgumentParser(description="Report shouted titles and an explicit thumbnail mismatch.")
    parser.add_argument("packet", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    found = scan_path(args.packet)
    if not found:
        print("clear")
        return 0
    for kind, detail in found:
        print(f"{kind}: {detail}")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
