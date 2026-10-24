#!/usr/bin/env python3
"""Report anti-slop phrases in publish.md Description section.

Does not rewrite publish.md. A hit is a revision signal, not an authorship claim.
This tool does not rewrite. Default exit is 0 so a clear packet cannot fail the build.
--strict exits 1 when any hit remains. Patterns are high-precision word-boundary matches.

Output includes a short context snippet around the first match of each phrase
so the revision signal is immediately actionable. Uses shared phrase_utils.ANTI_SLOP_PATTERNS
plus DESCRIPTION_EXTRA_PATTERNS, normalize, context_snippet, and compile_word_boundary_patterns.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import (
    ANTI_SLOP_PATTERNS,
    DESCRIPTION_EXTRA_PATTERNS,
    context_snippet,
    normalize,
    compile_word_boundary_patterns,
)  # noqa: E402

# Combined high-precision patterns for descriptions. Shared lists avoid local duplication.
PATTERNS = ANTI_SLOP_PATTERNS + DESCRIPTION_EXTRA_PATTERNS
DESC_RE = re.compile(r"## Description\s*\n(.*?)(?=\n## |\Z)", re.S)
_PATTERN_RES = compile_word_boundary_patterns(PATTERNS)


def description_text(text: str) -> str:
    m = DESC_RE.search(text.replace("\r\n", "\n"))
    return m.group(1).strip() if m else ""


def hits(text: str) -> list[tuple[str, int, str]]:
    body = normalize(description_text(text))
    if not body:
        return []
    found = []
    for phrase, cre in zip(PATTERNS, _PATTERN_RES):
        matches = list(cre.finditer(body))
        count = len(matches)
        if count:
            m = matches[0]
            ctx = context_snippet(body, m)
            found.append((phrase, count, ctx))
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
