#!/usr/bin/env python3
"""Report anti-slop phrases in script.md WORDS. Does not rewrite the script.

Patterns come from docs/content_quality.md. A hit is a revision signal, not
an authorship claim. This tool does not rewrite script.md. Default exit is 0
so a frozen Q1 script cannot fail the build. --strict exits 1 when any hit
remains. set_status.py refuses ready_for_vo while a hit remains.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Short, high-precision phrases. Do not add a broad "not X, but Y" regex.
PATTERNS = (
    "unlock your potential",
    "in today's fast-paced world",
    "in today’s fast-paced world",
    "we all struggle",
    "in this video",
    "you will learn",
    "the key is",
    "work smarter",
    "smash the like",
    "hit subscribe",
    "game changer",
    "at the end of the day",
    "in conclusion",
    "to summarize",
    "the bottom line is",
    "let's dive in",
    "let’s dive in",
    "without further ado",
    "it goes without saying",
    "as we all know",
    "it's no secret that",
    "it’s no secret that",
    "needless to say",
    "the fact of the matter is",
)

WORD_RE = re.compile(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n## |\Z)", re.S)


def spoken(text: str) -> str:
    parts = WORD_RE.findall(text.replace("\r\n", "\n"))
    return "\n".join(part.strip() for part in parts)


def hits(text: str) -> list[tuple[str, int]]:
    body = spoken(text).lower()
    found = []
    for phrase in PATTERNS:
        count = body.count(phrase)
        if count:
            found.append((phrase, count))
    return found


def scan_path(path: Path) -> list[tuple[str, int]]:
    script = path / "script.md"
    if not script.is_file():
        return []
    return hits(script.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Report anti-slop phrases in script WORDS.")
    parser.add_argument("packet", nargs="?", help="Packet folder. Default: every videos/* with script.md")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any hit remains.")
    args = parser.parse_args()
    if args.packet:
        folders = [Path(args.packet)]
    else:
        videos = ROOT / "videos"
        folders = sorted(p for p in videos.iterdir() if p.is_dir() and (p / "script.md").is_file())
    print("QUALITY SCAN")
    total = 0
    for folder in folders:
        found = scan_path(folder)
        total += sum(count for _, count in found)
        if not found:
            print(f"{folder.name}: clear")
            continue
        detail = ", ".join(f"{phrase} x{count}" for phrase, count in found)
        print(f"{folder.name}: hits {detail}")
    print(f"hits: {total}")
    print("rewrites: 0")
    if args.strict and total:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
