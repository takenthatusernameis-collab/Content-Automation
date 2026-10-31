#!/usr/bin/env python3
"""Check YouTube title lengths against recommended best practices.

Reads titles.md, extracts title candidates, and reports character counts.
Flags titles outside the 40-70 character ideal band (YouTube search truncates ~60).
Provides context for revision. Does not rewrite files. Reduces recurring
manual length checks before publish on every future packet.
Uses shared phrase_utils.normalize and titles_from where possible.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from validate_packet import titles_from  # noqa: E402
from phrase_utils import normalize  # noqa: E402

IDEAL_MIN = 40
IDEAL_MAX = 70
HARD_MAX = 100


def check_title(title: str) -> tuple[str, str]:
    title = normalize(title.strip())
    n = len(title)
    if n == 0:
        return "empty", "empty title"
    if n < IDEAL_MIN:
        return "short", f"{n} chars (ideal {IDEAL_MIN}-{IDEAL_MAX})"
    if n > HARD_MAX:
        return "too_long", f"{n} chars (hard max {HARD_MAX})"
    if n > IDEAL_MAX:
        return "long", f"{n} chars (ideal <= {IDEAL_MAX}, truncates ~60)"
    return "ok", f"{n} chars"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report YouTube title length vs recommended band. No file writes."
    )
    parser.add_argument("packet", type=Path)
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any non-ok")
    args = parser.parse_args()

    path = args.packet.resolve()
    titles_path = path / "titles.md"
    if not titles_path.is_file():
        print("no titles.md")
        return 0

    text = titles_path.read_text(encoding="utf-8")
    titles = titles_from(text)
    if not titles:
        print("no titles extracted")
        return 0

    print("TITLE LENGTH CHECK (YouTube recommended ~50-60 chars, ideal 40-70)")
    print(f"Packet: {path.name}")
    print()
    issues = 0
    for i, raw in enumerate(titles, 1):
        status, detail = check_title(raw)
        mark = "OK" if status == "ok" else status.upper()
        print(f"{i}. [{mark}] {detail}")
        print(f"   {normalize(raw.strip())[:80]}")
        if status != "ok":
            issues += 1
        print()

    if issues == 0:
        print("All titles in recommended length band.")
        return 0
    print(f"{issues} title(s) outside ideal band. Prefer 40-70 characters for better CTR/search display.")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
