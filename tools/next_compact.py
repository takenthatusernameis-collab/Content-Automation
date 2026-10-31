#!/usr/bin/env python3
"""Keep NEXT.md short enough that a truncated fetch still shows the newest locks.

Older do-not-rediscover notes move to docs/next_archive.md. This tool does not
delete them, does not poll OAuth, and does not write packets.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEXT = ROOT / "NEXT.md"
ARCHIVE = ROOT / "docs" / "next_archive.md"
MAX_ITEMS = 6
ITEM_RE = re.compile(r"^([0-9]|Run )")


def split_items(text: str) -> tuple[str, list[str]]:
    blocks = text.split("\n\n")
    preamble: list[str] = []
    items: list[str] = []
    seen_item = False
    for block in blocks:
        if not block.strip():
            continue
        first = block.lstrip().splitlines()[0]
        if ITEM_RE.match(first):
            seen_item = True
            items.append(block.strip() + "\n")
        elif not seen_item:
            preamble.append(block.strip())
        else:
            # A non-item after notes stays with the preamble so it is not archived.
            preamble.append(block.strip())
    pre = "\n\n".join(preamble).strip()
    if pre:
        pre += "\n\n"
    return pre, items


def collapse_preamble(pre: str) -> str:
    """Keep one Active locks block. A second copy hides the human step in a truncated fetch.

    A lone '.' paragraph is leftover separator noise, not a lock.
    """
    blocks = [block.strip() for block in pre.split("\n\n") if block.strip()]
    kept: list[str] = []
    seen_locks = False
    for block in blocks:
        if block == ".":
            continue
        if block.startswith("Active locks:"):
            if seen_locks:
                continue
            seen_locks = True
        kept.append(block)
    text = "\n\n".join(kept)
    if text:
        text += "\n\n"
    return text


def compact_text(text: str, archive_text: str, max_items: int = MAX_ITEMS) -> tuple[str, str, int]:
    """Return new NEXT, new archive, and how many notes were moved."""
    preamble, items = split_items(text)
    preamble = collapse_preamble(preamble)
    if len(items) <= max_items:
        new_next = preamble + "\n".join(items)
        if new_next and not new_next.endswith("\n"):
            new_next += "\n"
        return new_next, archive_text, 0
    kept = items[:max_items]
    older = items[max_items:]
    moved = []
    for part in older:
        marker = part[:48]
        if marker in archive_text:
            continue
        moved.append(part.strip() + "\n")
    addition = "\n".join(moved)
    if addition and archive_text and not archive_text.endswith("\n"):
        archive_text += "\n"
    if addition:
        archive_text = archive_text + ("\n" if archive_text.endswith("\n") else "") + addition
        if not archive_text.endswith("\n"):
            archive_text += "\n"
    new_next = preamble + "\n".join(kept)
    if not new_next.endswith("\n"):
        new_next += "\n"
    return new_next, archive_text, len(older)


def main() -> int:
    if not NEXT.is_file():
        print("REFUSE: NEXT.md missing", file=sys.stderr)
        return 2
    archive_text = ARCHIVE.read_text() if ARCHIVE.is_file() else (
        "# NEXT ARCHIVE\n\n"
        "Older do-not-rediscover notes. Do not paste these back into NEXT.md. "
        "Do not restore a behavior named here.\n\n"
    )
    new_next, new_archive, moved = compact_text(NEXT.read_text(), archive_text)
    if moved == 0:
        if new_next != NEXT.read_text():
            NEXT.write_text(new_next)
            print(f"NEXT COMPACT OK items={len(split_items(new_next)[1])} moved=0 collapsed=1")
            return 0
        print(f"NEXT COMPACT OK items={len(split_items(new_next)[1])} moved=0")
        return 0
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE.write_text(new_archive)
    NEXT.write_text(new_next)
    print(f"NEXT COMPACT OK items={len(split_items(new_next)[1])} moved={moved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
