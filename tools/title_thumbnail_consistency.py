#!/usr/bin/env python3
"""Title / thumbnail text consistency check.

Read-only. Parses titles.md Primary and thumbnail.md "On-image text".
Reports whether the thumbnail text is a short, non-empty phrase that shares
at least one significant word with the primary title or packet promise.
Surfaces visual/metadata drift before upload without credentials.
Does not invent text, rewrite files, poll secrets, or extend production_readiness.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

STOP = {
    "a", "an", "the", "to", "of", "and", "or", "for", "on", "in", "with",
    "what", "every", "stop", "deciding", "work", "morning", "your", "you",
}

def extract_primary(titles_text: str) -> str:
    m = re.search(r"^Primary:\s*(.+)$", titles_text, re.M)
    return m.group(1).strip() if m else ""

def extract_on_image(thumb_text: str) -> str:
    m = re.search(r"On-image text[^:]*:\s*(.+)$", thumb_text, re.M | re.I)
    return m.group(1).strip() if m else ""

def significant_words(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z']+", text.lower())
    return {w for w in words if len(w) > 2 and w not in STOP}

def inspect(packet: Path) -> dict:
    titles_path = packet / "titles.md"
    thumb_path = packet / "thumbnail.md"
    if not titles_path.is_file() or not thumb_path.is_file():
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "missing titles.md or thumbnail.md",
            "primary": "",
            "on_image": "",
            "shared": [],
        }
    primary = extract_primary(titles_path.read_text(encoding="utf-8"))
    on_image = extract_on_image(thumb_path.read_text(encoding="utf-8"))
    if not primary or not on_image:
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "could not parse Primary or On-image text",
            "primary": primary,
            "on_image": on_image,
            "shared": [],
        }
    p_words = significant_words(primary)
    t_words = significant_words(on_image)
    shared = sorted(p_words & t_words)
    short_ok = 1 <= len(on_image.split()) <= 6
    overlap_ok = bool(shared) or len(t_words) == 0
    issues = []
    if not short_ok:
        issues.append(f"on-image word count {len(on_image.split())} outside 1-6")
    if not overlap_ok:
        issues.append("no significant word overlap with primary")
    warn = bool(issues)
    return {
        "ok": not warn,
        "code": "WARN" if warn else "OK",
        "detail": "; ".join(issues) if issues else "short on-image text overlaps primary",
        "primary": primary,
        "on_image": on_image,
        "shared": shared,
        "short_ok": short_ok,
        "overlap_ok": overlap_ok,
    }

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check thumbnail on-image text vs primary title. No writes."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    rep = inspect(path)
    print(f"packet: {path.name}")
    print(f"primary: {rep.get('primary')}")
    print(f"on_image: {rep.get('on_image')}")
    print(f"shared_words: {', '.join(rep.get('shared') or []) or 'none'}")
    print(f"consistency: {rep['code']} ({rep['detail']})")
    print("Does not invent text, rewrite files, or poll OAuth.")
    return 0 if rep["code"] != "NO_DATA" else 2

if __name__ == "__main__":
    raise SystemExit(main())
