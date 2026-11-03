#!/usr/bin/env python3
"""Chapters / description-embedded chapters consistency check.

Read-only. Extracts the YouTube chapter lines from chapters.md and the
timestamped lines from the Description section of publish.md.
Reports whether the two lists match (order and titles) so future packets
can surface chapter/metadata drift before upload.
Does not invent text, rewrite files, poll secrets, or extend production_readiness.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CHAPTER_LINE = re.compile(r"^(\d+:\d{2}(?::\d{2})?)\s+(.+)$")


def extract_chapters_from_file(text: str) -> list[tuple[str, str]]:
    """Pull lines under ## YouTube lines that look like timestamps."""
    m = re.search(r"^##[ \t]*YouTube lines[^\n]*\n(.*?)(?=^##|\Z)", text, re.M | re.S | re.I)
    if not m:
        return []
    body = m.group(1)
    out = []
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cm = CHAPTER_LINE.match(line)
        if cm:
            out.append((cm.group(1), cm.group(2).strip()))
    return out


def extract_chapters_from_description(text: str) -> list[tuple[str, str]]:
    """Pull timestamped lines from the Description section of publish.md."""
    m = re.search(r"^##[ \t]*Description[^\n]*\n(.*?)(?=^##|\Z)", text, re.M | re.S | re.I)
    if not m:
        return []
    body = m.group(1)
    out = []
    for line in body.splitlines():
        line = line.strip()
        cm = CHAPTER_LINE.match(line)
        if cm:
            out.append((cm.group(1), cm.group(2).strip()))
    return out


def inspect(packet: Path) -> dict:
    ch_path = packet / "chapters.md"
    pub_path = packet / "publish.md"
    if not ch_path.is_file() or not pub_path.is_file():
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "missing chapters.md or publish.md",
            "chapters": [],
            "description": [],
            "match": False,
        }
    ch_text = ch_path.read_text(encoding="utf-8")
    pub_text = pub_path.read_text(encoding="utf-8")
    from_ch = extract_chapters_from_file(ch_text)
    from_desc = extract_chapters_from_description(pub_text)
    if not from_ch and not from_desc:
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "no chapter lines found in either file",
            "chapters": from_ch,
            "description": from_desc,
            "match": False,
        }
    match = from_ch == from_desc
    issues = []
    if not match:
        if len(from_ch) != len(from_desc):
            issues.append(f"count differs: chapters.md={len(from_ch)} description={len(from_desc)}")
        else:
            issues.append("chapter lines differ in order or titles")
    # Extra soft check: first chapter should be 0:00
    if from_ch and from_ch[0][0] != "0:00":
        issues.append("first chapter in chapters.md is not 0:00")
    if from_desc and from_desc[0][0] != "0:00":
        issues.append("first chapter in description is not 0:00")
    warn = bool(issues) or not match
    return {
        "ok": match and not issues,
        "code": "OK" if match and not issues else "WARN",
        "detail": "; ".join(issues) if issues else "chapter lists match exactly",
        "chapters": from_ch,
        "description": from_desc,
        "match": match,
        "count_ch": len(from_ch),
        "count_desc": len(from_desc),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check chapters.md YouTube lines vs timestamped lines in publish.md Description. No writes."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    rep = inspect(path)
    print(f"packet: {path.name}")
    print(f"chapters_md: {rep.get('count_ch', 0)} lines")
    print(f"description: {rep.get('count_desc', 0)} lines")
    print(f"exact_match: {rep.get('match')}")
    if rep.get("chapters"):
        print("from_chapters:")
        for ts, title in rep["chapters"][:8]:
            print(f"  {ts} {title}")
        if len(rep["chapters"]) > 8:
            print("  ...")
    print(f"consistency: {rep['code']} ({rep['detail']})")
    print("Does not invent text, rewrite files, or poll OAuth.")
    return 0 if rep["code"] != "NO_DATA" else 2


if __name__ == "__main__":
    raise SystemExit(main())
