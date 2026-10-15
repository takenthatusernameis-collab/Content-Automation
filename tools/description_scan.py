#!/usr/bin/env python3
"""Report anti-slop phrases in publish.md Description section.

Does not rewrite publish.md. A hit is a revision signal, not an authorship claim.
This tool does not rewrite. Default exit is 0 so a clear packet cannot fail the build.
--strict exits 1 when any hit remains. Patterns are high-precision word-boundary matches.

Output includes a short context snippet around the first match of each phrase
so the revision signal is immediately actionable.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# High-precision anti-slop / filler phrases common in video descriptions.
# Matching uses word boundaries for higher precision.
PATTERNS = (
    "in this video",
    "you will learn",
    "the key is",
    "unlock your potential",
    "in today's fast-paced world",
    "in today’s fast-paced world",
    "we all struggle",
    "work smarter",
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
    "to put it simply",
    "in other words",
    "the reality is",
    "here's the thing",
    "here’s the thing",
    "the truth is",
    "make no mistake",
    "in a nutshell",
    "long story short",
    "the point is",
    "to sum up",
    "in summary",
    "put simply",
    "what this means is",
    "the implication is",
    "case in point",
    "in the final analysis",
    "when you think about it",
    "smash the like",
    "hit subscribe",
    "don't forget to",
    "don’t forget to",
    "leave a comment",
    "let me know",
)

DESC_RE = re.compile(r"## Description\s*\n(.*?)(?=\n## |\Z)", re.S)
_PATTERN_RES = tuple(
    re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE) for phrase in PATTERNS
)


def description_text(text: str) -> str:
    m = DESC_RE.search(text.replace("\r\n", "\n"))
    return m.group(1).strip() if m else ""


def hits(text: str) -> list[tuple[str, int, str]]:
    body = description_text(text)
    if not body:
        return []
    found = []
    for phrase, cre in zip(PATTERNS, _PATTERN_RES):
        matches = list(cre.finditer(body))
        count = len(matches)
        if count:
            m = matches[0]
            start = max(0, m.start() - 40)
            end = min(len(body), m.end() + 40)
            context = body[start:end].replace("\n", " ").strip()
            if len(context) > 90:
                context = context[:87] + "..."
            found.append((phrase, count, context))
    return found


def scan_path(path: Path) -> list[tuple[str, int, str]]:
    pub = path / "publish.md"
    if not pub.is_file():
        return []
    return hits(pub.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Report anti-slop phrases in publish.md Description.")
    parser.add_argument("packet", nargs="?", help="Packet folder. Default: every videos/* with publish.md")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any hit remains.")
    args = parser.parse_args()
    if args.packet:
        folders = [Path(args.packet)]
    else:
        videos = ROOT / "videos"
        folders = sorted(p for p in videos.iterdir() if p.is_dir() and (p / "publish.md").is_file())
    print("DESCRIPTION SCAN")
    total = 0
    for folder in folders:
        found = scan_path(folder)
        total += sum(count for _, count, _ in found)
        if not found:
            print(f"{folder.name}: clear")
            continue
        details = []
        for phrase, count, ctx in found:
            details.append(f"{phrase} x{count} [{ctx}]")
        detail = "; ".join(details)
        print(f"{folder.name}: hits {detail}")
    print(f"hits: {total}")
    print("rewrites: 0")
    if args.strict and total:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
