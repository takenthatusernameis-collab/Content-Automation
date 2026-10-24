#!/usr/bin/env python3
"""Report weak, clickbait, or overly long thumbnail text ideas.

Scans ## Thumbnail section in publish.md or assets.md.
Does not rewrite files. A hit is a revision signal.
Default exit is 0 so a clear packet cannot fail the build.
--strict exits 1 when any hit remains.

Checks: presence, placeholder, high-precision clickbait/weak patterns,
word count over 6 (YouTube readability guideline).
Output includes short context so the revision signal is immediately actionable.
Uses shared phrase_utils.context_snippet, THUMBNAIL_WEAK_PATTERNS, normalize, and compile_word_boundary_patterns.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import context_snippet, normalize, THUMBNAIL_WEAK_PATTERNS, compile_word_boundary_patterns  # noqa: E402

# High-precision weak / clickbait patterns live in phrase_utils.THUMBNAIL_WEAK_PATTERNS.
# Matching uses shared compile_word_boundary_patterns. Text is normalized so one straight entry covers variants.
_WEAK_RES = compile_word_boundary_patterns(THUMBNAIL_WEAK_PATTERNS)

THUMB_RE = re.compile(r"## Thumbnail(?: text| idea| brief)?\s*\n(.*?)(?=\n## |\Z)", re.S)


def thumbnail_text(text: str) -> str:
    m = THUMB_RE.search(text.replace("\r\n", "\n"))
    return m.group(1).strip() if m else ""


def hits(text: str) -> list[tuple[str, str, str]]:
    body = thumbnail_text(text)
    if not body:
        return [("missing", "no thumbnail section", "")]
    body = normalize(body)
    found = []
    if len(body) < 10 or "(add" in body.lower() or body.lower() in ("thumbnail", "tbd"):
        found.append(("placeholder", body[:60], body[:60]))
    words = body.split()
    if len(words) > 6:
        found.append(("long", str(len(words)), body[:60]))
    for phrase, cre in zip(THUMBNAIL_WEAK_PATTERNS, _WEAK_RES):
        m = cre.search(body)
        if m:
            ctx = context_snippet(body, m, before=20, after=20, max_len=80)
            found.append(("weak", phrase, ctx))
    return found


def scan_path(path: Path) -> list[tuple[str, str, str]]:
    # Prefer publish.md
    pub = path / "publish.md"
    if pub.is_file():
        return hits(pub.read_text(encoding="utf-8"))
    # Fallback to assets.md
    assets = path / "assets.md"
    if assets.is_file():
        return hits(assets.read_text(encoding="utf-8"))
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Report thumbnail text quality issues.")
    parser.add_argument("packet", nargs="?", help="Packet folder. Default: every videos/* with publish or assets")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any hit remains.")
    args = parser.parse_args()
    if args.packet:
        folders = [Path(args.packet)]
    else:
        videos = ROOT / "videos"
        folders = sorted(
            p for p in videos.iterdir()
            if p.is_dir() and ((p / "publish.md").is_file() or (p / "assets.md").is_file())
        )
    print("THUMBNAIL SCAN")
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
