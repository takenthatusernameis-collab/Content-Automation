#!/usr/bin/env python3
"""Report weak, generic, or spammy tags in publish.md Tags section.

Does not rewrite publish.md. A hit is a revision signal, not an authorship claim.
This tool does not rewrite. Default exit is 0 so a clear packet cannot fail the build.
--strict exits 1 when any hit remains. Patterns are high-precision.

Output includes a short context snippet so the revision signal is immediately actionable.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

# High-precision weak / generic / spam tags common in low-quality metadata.
# Matching uses word boundaries or exact for short terms.
WEAK_PATTERNS = (
    "video",
    "youtube",
    "tutorial",
    "how to",
    "subscribe",
    "like and subscribe",
    "free",
    "best",
    "amazing",
    "incredible",
    "must watch",
    "viral",
    "trending",
    "clickbait",
    "secret",
    "hack",
    "tips and tricks",
)
_WEAK_RES = tuple(
    re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE) for phrase in WEAK_PATTERNS
)

TAGS_RE = re.compile(r"## Tags\s*\n(.*?)(?=\n## |\Z)", re.S)
BULLET_RE = re.compile(r"^-\s+(.+)$", re.M)


def tags_text(text: str) -> str:
    m = TAGS_RE.search(text.replace("\r\n", "\n"))
    return m.group(1).strip() if m else ""


def extract_tags(body: str) -> list[str]:
    return [m.group(1).strip() for m in BULLET_RE.finditer(body) if m.group(1).strip()]


def hits(text: str) -> list[tuple[str, str, str]]:
    body = tags_text(text)
    if not body:
        return []
    tags = extract_tags(body)
    found = []
    # Duplicates (case-insensitive)
    lower_tags = [t.lower() for t in tags]
    counts = Counter(lower_tags)
    for tag, count in counts.items():
        if count > 1:
            ctx = f"duplicate: {tag} x{count}"
            found.append(("duplicate", tag, ctx))
    # Weak patterns
    for tag in tags:
        for phrase, cre in zip(WEAK_PATTERNS, _WEAK_RES):
            if cre.search(tag):
                ctx = tag[:80]
                found.append(("weak", phrase, ctx))
    # Too short or placeholder
    for tag in tags:
        if len(tag) < 3 or tag.lower() in ("(add tags)", "add tags", "tags"):
            found.append(("short", tag, tag))
        if len(tag) > 40:
            found.append(("long", tag, tag[:50] + "..."))
    return found


def scan_path(path: Path) -> list[tuple[str, str, str]]:
    pub = path / "publish.md"
    if not pub.is_file():
        return []
    return hits(pub.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Report weak/generic tags in publish.md Tags.")
    parser.add_argument("packet", nargs="?", help="Packet folder. Default: every videos/* with publish.md")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any hit remains.")
    args = parser.parse_args()
    if args.packet:
        folders = [Path(args.packet)]
    else:
        videos = ROOT / "videos"
        folders = sorted(p for p in videos.iterdir() if p.is_dir() and (p / "publish.md").is_file())
    print("TAGS SCAN")
    total = 0
    for folder in folders:
        found = scan_path(folder)
        total += len(found)
        if not found:
            print(f"{folder.name}: clear")
            continue
        details = []
        for kind, token, ctx in found:
            details.append(f"{kind}:{token} [{ctx}]")
        detail = "; ".join(details)
        print(f"{folder.name}: hits {detail}")
    print(f"hits: {total}")
    print("rewrites: 0")
    if args.strict and total:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
