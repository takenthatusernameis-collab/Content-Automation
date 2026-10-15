#!/usr/bin/env python3
"""Report anti-slop phrases in script.md WORDS. Does not rewrite the script.

Patterns come from docs/content_quality.md. A hit is a revision signal, not
an authorship claim. This tool does not rewrite script.md. Default exit is 0
so a frozen Q1 script cannot fail the build. --strict exits 1 when any hit
remains. set_status.py refuses ready_for_vo while a hit remains.

Output includes a short context snippet around the first match of each phrase
so the revision signal is immediately actionable.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Short, high-precision phrases. Do not add a broad "not X, but Y" regex.
# Matching uses word boundaries for higher precision (avoids partial-word false positives).
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
    "to put it simply",
    "in other words",
    "the reality is",
    "here's the thing",
    "here’s the thing",
    "the truth is",
    "make no mistake",
    "in a nutshell",
    "long story short",
    "when all is said and done",
    "the point is",
    "let me be clear",
    "as it turns out",
    "believe it or not",
    "to be honest",
    "the thing is",
    "all in all",
    "moving forward",
    "going forward",
    "first and foremost",
    "it is important to note",
    "it should be noted",
    "as a matter of fact",
    "for what it's worth",
    "for what it’s worth",
    "that being said",
    "having said that",
    "in fact",
    "of course",
    "obviously",
    "clearly",
    "simply put",
    "in short",
    "to be clear",
    "all things considered",
    "it's worth noting",
    "it’s worth noting",
    "at its core",
    "when it comes to",
    "keep in mind",
    "in essence",
    "the fact remains",
    "let's be honest",
    "let’s be honest",
    "here's the kicker",
    "here’s the kicker",
    "bear in mind",
    "take note that",
    "as you can see",
    "as we can see",
    "the takeaway is",
    "to put it in perspective",
    "it's important to remember",
    "it’s important to remember",
    "in the modern world",
    "in today's society",
    "in today’s society",
    "it's safe to say",
    "it’s safe to say",
    "suffice it to say",
    "one thing is clear",
    "in a perfect world",
    "when push comes to shove",
    "to be fair",
    "last but not least",
    "with that said",
    "to that end",
    "as previously mentioned",
    "it is worth mentioning",
    "in reality",
    "as a result",
    "for instance",
    "in particular",
    "on the other hand",
    "that said",
    "the bottom line",
    "it is important",
)

WORD_RE = re.compile(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n## |\Z)", re.S)
# Precompile word-boundary patterns once (case-insensitive).
_PATTERN_RES = tuple(
    re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE) for phrase in PATTERNS
)


def spoken(text: str) -> str:
    parts = WORD_RE.findall(text.replace("\r\n", "\n"))
    return "\n".join(part.strip() for part in parts)


def hits(text: str) -> list[tuple[str, int, str]]:
    body = spoken(text)
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
