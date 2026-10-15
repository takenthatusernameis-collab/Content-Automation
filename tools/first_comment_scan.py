#!/usr/bin/env python3
"""Report engagement-bait or reply-prompt patterns in publish.md First comment section.

Does not rewrite publish.md. A hit is a revision signal, not an authorship claim.
This tool does not rewrite. Default exit is 0 so a clear packet cannot fail the build.
--strict exits 1 when any hit remains. Patterns are high-precision.

Output includes a short context snippet so the revision signal is immediately actionable.
The pin should be the assignment from the mechanism, not a reply prompt (see docs/content_quality.md).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# High-precision engagement-bait / reply-prompt patterns for pinned comments.
# Matching uses word boundaries.
BAIT_PATTERNS = (
    "reply with",
    "let me know",
    "comment below",
    "what do you think",
    "smash the like",
    "don't forget to",
    "leave a comment",
    "tell me in the comments",
    "drop a comment",
    "your thoughts",
    "let\u2019s discuss",
    "let's discuss",
)
_BAIT_RES = tuple(
    re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE) for phrase in BAIT_PATTERNS
)

FIRST_RE = re.compile(r"## First comment(?: \(pin candidate\))?\s*\n(.*?)(?=\n## |\Z)", re.S)


def first_comment_text(text: str) -> str:
    m = FIRST_RE.search(text.replace("\r\n", "\n"))
    return m.group(1).strip() if m else ""


def _context(body: str, start: int, end: int) -> str:
    s = max(0, start - 40)
    e = min(len(body), end + 40)
    context = body[s:e].replace("\n", " ").strip()
    if len(context) > 100:
        context = context[:97] + "..."
    return context


def hits(text: str) -> list[tuple[str, str, str]]:
    body = first_comment_text(text)
    if not body:
        return []
    found = []
    for phrase, cre in zip(BAIT_PATTERNS, _BAIT_RES):
        m = cre.search(body)
        if m:
            ctx = _context(body, m.start(), m.end())
            found.append(("bait", phrase, ctx))
    # Placeholder or too short
    if len(body) < 20 or "(add" in body.lower() or body.lower().startswith("assignment:"):
        # Note: assignment: is expected; flag only pure placeholders
        if "(add" in body.lower() or len(body) < 10:
            found.append(("placeholder", body[:60], body[:60]))
    return found


def scan_path(path: Path) -> list[tuple[str, str, str]]:
    pub = path / "publish.md"
    if not pub.is_file():
        return []
    return hits(pub.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Report engagement bait in publish.md First comment.")
    parser.add_argument("packet", nargs="?", help="Packet folder. Default: every videos/* with publish.md")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any hit remains.")
    args = parser.parse_args()
    if args.packet:
        folders = [Path(args.packet)]
    else:
        videos = ROOT / "videos"
        folders = sorted(p for p in videos.iterdir() if p.is_dir() and (p / "publish.md").is_file())
    print("FIRST COMMENT SCAN")
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
