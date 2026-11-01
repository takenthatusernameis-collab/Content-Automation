#!/usr/bin/env python3
"""Shared helpers for the local canonical assignment source.

Provides a reliable reader for the primary assignment statement so option writers
and scanners can prefer it without duplicated parsing logic or drift.
Does not invent content. Returns None when the file or a clear primary is absent.
"""

from __future__ import annotations

from pathlib import Path


def read_primary(packet: Path) -> str | None:
    """Return the primary assignment statement from assignment_source.md if present.

    Looks for the first substantial non-header line after the
    '## Primary assignment statement' heading. Returns None if the file
    is missing or no clear primary line is found.
    """
    src = packet / "assignment_source.md"
    if not src.is_file():
        return None
    text = src.read_text(encoding="utf-8")
    in_section = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Primary assignment statement"):
            in_section = True
            continue
        if in_section and stripped.startswith("##"):
            break
        if in_section and stripped and not stripped.startswith("#") and not stripped.startswith("-"):
            return stripped
    return None
