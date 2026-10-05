#!/usr/bin/env python3
"""Keep PROGRESS.md and FAILURES.md short enough for a truncated fetch.

Older sections move to docs/progress_archive.md and docs/failures_archive.md.
This tool does not delete them, does not poll OAuth, and does not write packets.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_SECTIONS = 12
SPLIT = "## Run "


def split_sections(text: str) -> tuple[str, list[str]]:
    parts = text.split(SPLIT)
    return parts[0], parts[1:]


def compact_text(text: str, archive_text: str, max_sections: int = MAX_SECTIONS) -> tuple[str, str, int]:
    preamble, sections = split_sections(text)
    if len(sections) <= max_sections:
        if text and not text.endswith("\n"):
            text += "\n"
        return text, archive_text, 0
    kept = sections[:max_sections]
    older = sections[max_sections:]
    moved = []
    for part in older:
        marker = (SPLIT + part).splitlines()[0][:48]
        if marker and marker in archive_text:
            continue
        moved.append(SPLIT + part)
    addition = "".join(moved)
    if addition and archive_text and not archive_text.endswith("\n"):
        archive_text += "\n"
    new_archive = archive_text + addition
    if preamble.strip():
        pre = preamble if preamble.endswith("\n") else preamble + "\n"
    else:
        pre = "# LOG\n\n"
    new_text = pre + "".join(SPLIT + part for part in kept)
    if not new_text.endswith("\n"):
        new_text += "\n"
    return new_text, new_archive, len(older)


def compact_file(live: Path, archive: Path, pointer: str) -> tuple[int, int]:
    if not live.is_file():
        print(f"REFUSE: {live.name} missing", file=sys.stderr)
        return 2, 0
    archive_text = archive.read_text() if archive.is_file() else (
        f"# {live.stem.upper()} ARCHIVE\n\nOlder sections. Do not delete. Do not paste back into {live.name}.\n\n"
    )
    new_text, new_archive, moved = compact_text(live.read_text(), archive_text)
    if pointer not in new_text.split(SPLIT, 1)[0]:
        pre, sections = split_sections(new_text)
        if not pre.endswith("\n"):
            pre += "\n"
        pre = pre.rstrip() + f"\n\n{pointer}\n\n"
        new_text = pre + "".join(SPLIT + part for part in sections)
    if moved == 0 and new_text == live.read_text():
        print(f"LOG COMPACT OK file={live.name} sections={len(split_sections(new_text)[1])} moved=0")
        return 0, 0
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_text(new_archive)
    live.write_text(new_text)
    print(f"LOG COMPACT OK file={live.name} sections={len(split_sections(new_text)[1])} moved={moved}")
    return 0, moved


def main() -> int:
    jobs = [
        (
            ROOT / "PROGRESS.md",
            ROOT / "docs" / "progress_archive.md",
            "Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.",
        ),
        (
            ROOT / "FAILURES.md",
            ROOT / "docs" / "failures_archive.md",
            "Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.",
        ),
    ]
    status = 0
    for live, archive, pointer in jobs:
        code, _moved = compact_file(live, archive, pointer)
        status = status or code
    return status


if __name__ == "__main__":
    raise SystemExit(main())
