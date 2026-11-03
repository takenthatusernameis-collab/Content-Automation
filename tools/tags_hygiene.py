#!/usr/bin/env python3
"""Tags hygiene check for publish.md.

Read-only. Parses the Tags list and the "Removed as stopwords" note.
Reports duplicates, any leakage of removed stopwords into the live tags,
and unusually long tags so future packets can surface tag metadata issues
before upload.
Does not invent text, rewrite files, poll secrets, or extend production_readiness.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def extract_tags_and_removed(publish_text: str) -> tuple[list[str], set[str]]:
    """Return (live tags, removed stopwords set)."""
    tags: list[str] = []
    removed: set[str] = set()
    in_tags = False
    for line in publish_text.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("## tags"):
            in_tags = True
            continue
        if in_tags and stripped.startswith("##"):
            break
        if in_tags and stripped.startswith("- "):
            tag = stripped[2:].strip()
            if tag:
                tags.append(tag)
        if "Removed as stopwords" in line or "Removed as stopwords" in stripped:
            # Capture the colon list
            m = re.search(r"Removed as stopwords[^:]*:\s*(.+)", line, re.I)
            if m:
                for part in m.group(1).split(","):
                    w = part.strip().lower()
                    if w:
                        removed.add(w)
    return tags, removed


def inspect(packet: Path) -> dict:
    pub_path = packet / "publish.md"
    if not pub_path.is_file():
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "missing publish.md",
            "tags": [],
            "removed": [],
            "issues": [],
        }
    text = pub_path.read_text(encoding="utf-8")
    tags, removed = extract_tags_and_removed(text)
    if not tags:
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "no tags list found",
            "tags": [],
            "removed": sorted(removed),
            "issues": ["empty tags"],
        }
    issues = []
    lower_tags = [t.lower() for t in tags]
    if len(tags) != len(set(lower_tags)):
        issues.append("duplicate tags present")
    leaked = [t for t in tags if t.lower() in removed]
    if leaked:
        issues.append(f"removed-stopword leakage: {', '.join(leaked)}")
    long_tags = [t for t in tags if len(t) > 40]
    if long_tags:
        issues.append(f"unusually long tags (>40 chars): {', '.join(long_tags)}")
    emptyish = [t for t in tags if len(t.strip()) < 2]
    if emptyish:
        issues.append("near-empty tags")
    warn = bool(issues)
    return {
        "ok": not warn,
        "code": "WARN" if warn else "OK",
        "detail": "; ".join(issues) if issues else "tags unique, no removed-stopword leakage, reasonable lengths",
        "tags": tags,
        "removed": sorted(removed),
        "issues": issues,
        "count": len(tags),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check publish.md Tags hygiene (duplicates, removed-stopword leakage). No writes."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    rep = inspect(path)
    print(f"packet: {path.name}")
    print(f"tags_count: {rep.get('count', 0)}")
    print(f"tags: {', '.join(rep.get('tags') or [])}")
    print(f"removed_stopwords_noted: {', '.join(rep.get('removed') or []) or 'none'}")
    print(f"hygiene: {rep['code']} ({rep['detail']})")
    print("Does not invent text, rewrite files, or poll OAuth.")
    return 0 if rep["code"] != "NO_DATA" else 2


if __name__ == "__main__":
    raise SystemExit(main())
