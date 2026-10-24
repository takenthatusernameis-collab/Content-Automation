#!/usr/bin/env python3
"""Report weak, malformed, or gap-violating YouTube chapter lines.

Scans chapters.md ## YouTube lines or timestamp lines inside publish.md Description.
Does not rewrite files. A hit is a revision signal.
Default exit is 0 so a clear packet cannot fail the build.
--strict exits 1 when any hit remains.

Checks: first line 0:00, minimum 10s gaps (YouTube rule), reasonable count (3-12),
weak/engagement-bait titles, placeholders.
Output includes short context so the revision signal is immediately actionable.
Uses shared phrase_utils.CHAPTER_WEAK_PATTERNS, normalize, and compile_word_boundary_patterns.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import normalize, CHAPTER_WEAK_PATTERNS, compile_word_boundary_patterns  # noqa: E402

# High-precision weak patterns live in phrase_utils.CHAPTER_WEAK_PATTERNS.
# Matching uses shared compile_word_boundary_patterns. Titles are normalized so one straight entry covers variants.
_WEAK_RES = compile_word_boundary_patterns(CHAPTER_WEAK_PATTERNS)

CHAPTER_LINE_RE = re.compile(r"^\s*(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)$", re.M)
YOUTUBE_SECTION_RE = re.compile(r"## YouTube lines\s*\n(.*?)(?=\n## |\Z)", re.S)
DESC_RE = re.compile(r"## Description\s*\n(.*?)(?=\n## |\Z)", re.S)


def _to_seconds(stamp: str) -> float:
    parts = stamp.split(":")
    if len(parts) == 2:
        m, s = parts
        return int(m) * 60 + int(s)
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + int(s)
    return 0.0


def extract_lines(text: str) -> list[tuple[str, str]]:
    """Return list of (stamp, title) from chapters.md or description."""
    # Prefer explicit YouTube lines section
    m = YOUTUBE_SECTION_RE.search(text.replace("\r\n", "\n"))
    body = m.group(1) if m else ""
    if not body:
        # Fallback to description
        dm = DESC_RE.search(text.replace("\r\n", "\n"))
        body = dm.group(1) if dm else text
    lines = []
    for match in CHAPTER_LINE_RE.finditer(body):
        stamp, title = match.group(1), match.group(2).strip()
        if title:
            lines.append((stamp, title))
    return lines


def hits_from_lines(lines: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    found: list[tuple[str, str, str]] = []
    if not lines:
        found.append(("missing", "no chapter lines", ""))
        return found
    if lines[0][0] not in ("0:00", "00:00", "0:00:00"):
        found.append(("first", lines[0][0], lines[0][1]))
    if len(lines) < 3:
        found.append(("count", str(len(lines)), "fewer than 3"))
    if len(lines) > 12:
        found.append(("count", str(len(lines)), "more than 12"))
    prev = 0.0
    for stamp, title in lines:
        secs = _to_seconds(stamp)
        if secs - prev < 10.0 and prev > 0:
            found.append(("gap", stamp, title))
        prev = secs
        norm_title = normalize(title)
        for phrase, cre in zip(CHAPTER_WEAK_PATTERNS, _WEAK_RES):
            if cre.search(norm_title):
                found.append(("weak", phrase, title))
        if "(add" in title.lower() or title.lower() in ("chapter", "untitled"):
            found.append(("placeholder", title, title))
    return found


def scan_path(path: Path) -> list[tuple[str, str, str]]:
    # Prefer chapters.md
    ch = path / "chapters.md"
    if ch.is_file():
        lines = extract_lines(ch.read_text(encoding="utf-8"))
        return hits_from_lines(lines)
    # Fallback to publish.md
    pub = path / "publish.md"
    if pub.is_file():
        lines = extract_lines(pub.read_text(encoding="utf-8"))
        return hits_from_lines(lines)
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Report chapter quality issues.")
    parser.add_argument("packet", nargs="?", help="Packet folder. Default: every videos/* with publish or chapters")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any hit remains.")
    args = parser.parse_args()
    if args.packet:
        folders = [Path(args.packet)]
    else:
        videos = ROOT / "videos"
        folders = sorted(
            p for p in videos.iterdir()
            if p.is_dir() and ((p / "publish.md").is_file() or (p / "chapters.md").is_file())
        )
    print("CHAPTERS SCAN")
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
