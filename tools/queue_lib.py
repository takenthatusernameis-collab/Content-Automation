#!/usr/bin/env python3
"""Shared topic-queue helpers. No writes. Used by next_topic, mark_topic, new_packet."""

from __future__ import annotations

import re
from pathlib import Path


def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:60] or "untitled"


def next_id(videos_dir: Path) -> str:
    highest = 0
    if videos_dir.is_dir():
        for p in videos_dir.iterdir():
            if not p.is_dir() or p.name.startswith("_"):
                continue
            m = re.match(r"^(?:sample-)?(\d+)", p.name)
            if m:
                highest = max(highest, int(m.group(1)))
    return f"{highest + 1:03d}"


def existing_dirs(videos_dir: Path) -> list[str]:
    if not videos_dir.is_dir():
        return []
    names: list[str] = []
    for p in videos_dir.iterdir():
        if p.is_dir() and not p.name.startswith("_"):
            names.append(p.name)
    return sorted(names)


def existing_slugs(videos_dir: Path) -> set[str]:
    found: set[str] = set()
    for name in existing_dirs(videos_dir):
        found.add(name.lower())
        m = re.match(r"^(?:sample-)?\d+-(.+)$", name)
        if m:
            found.add(m.group(1).lower())
    return found


def parse_queue(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.startswith("| Q"):
            continue
        parts = [c.strip() for c in line.strip("|").split("|")]
        if len(parts) < 4:
            continue
        rows.append(
            {
                "id": parts[0],
                "status": parts[1].lower(),
                "working_title": parts[2],
                "one_line": parts[3],
                "raw": line,
            }
        )
    return rows


def match_folder(title: str, folders: list[str]) -> str | None:
    slug = slugify(title)
    for name in folders:
        lower = name.lower()
        if lower == slug or lower.endswith("-" + slug):
            return name
        m = re.match(r"^(?:sample-)?\d+-(.+)$", lower)
        if m and (m.group(1) == slug or slug in m.group(1)):
            return name
    return None


def already_used(title: str, slugs: set[str]) -> bool:
    slug = slugify(title)
    if slug in slugs:
        return True
    for existing in slugs:
        if slug and slug in existing:
            return True
    return False


def matching_queue_row(title: str, rows: list[dict[str, str]]) -> dict[str, str] | None:
    slug = slugify(title)
    for row in rows:
        if slugify(row["working_title"]) == slug:
            return row
    return None
