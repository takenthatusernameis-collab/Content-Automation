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

from phrase_utils import ANTI_SLOP_PATTERNS as PATTERNS

ROOT = Path(__file__).resolve().parents[1]

# Canonical list lives in phrase_utils.ANTI_SLOP_PATTERNS (single source of truth).
# Matching uses word boundaries for higher precision (avoids partial-word false positives).
# Text is normalized (curly apostrophes -> straight, etc.) so one pattern covers common variants.

WORD_RE = re.compile(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n## |\Z)", re.S)
# Precompile word-boundary patterns once (case-insensitive).
_PATTERN_RES = tuple(
    re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE) for phrase in PATTERNS
)


def normalize(text: str) -> str:
    """Normalize common variants so patterns match more reliably without duplicating entries."""
    text = text.replace("\u2019", "'").replace("\u2018", "'")  # curly single quotes
    text = text.replace("\u201c", '"').replace("\u201d", '"')  # curly double
    text = text.replace("\u2013", "-").replace("\u2014", "-")  # en/em dash
    return text


def spoken(text: str) -> str:
    parts = WORD_RE.findall(text.replace("\r\n", "\n"))
    body = "\n".join(part.strip() for part in parts)
    return normalize(body)


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
    print(f"patterns checked: {len(PATTERNS)}")
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
