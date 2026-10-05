#!/usr/bin/env python3
"""Lock the PROGRESS.md and FAILURES.md size caps."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import log_compact  # noqa: E402


def fail(msg: str) -> int:
    print(f"FAIL: {msg}", file=sys.stderr)
    return 1


def check_live(name: str, archive_name: str, needle: str) -> str | None:
    text = (ROOT / name).read_text()
    _pre, sections = log_compact.split_sections(text)
    if len(sections) > log_compact.MAX_SECTIONS:
        return f"{name} has {len(sections)} sections"
    if len(text.encode()) > 20000:
        return f"{name} is {len(text.encode())} bytes"
    if archive_name not in text:
        return f"{name} archive pointer missing"
    archive = ROOT / "docs" / archive_name
    if not archive.is_file():
        return f"docs/{archive_name} missing"
    if needle not in archive.read_text():
        return f"{needle} missing from docs/{archive_name}"
    return None


def main() -> int:
    for name, archive, needle in (
        ("PROGRESS.md", "progress_archive.md", "Run 2"),
        ("FAILURES.md", "failures_archive.md", "Run 2"),
    ):
        err = check_live(name, archive, needle)
        if err:
            return fail(err)
    filler = "".join(f"## Run {i} — filler\nnote {i}\n\n" for i in range(20, 0, -1))
    new_text, new_archive, moved = log_compact.compact_text(filler, "# ARCHIVE\n\n")
    if moved != 8:
        return fail(f"expected to move 8, moved {moved}")
    if len(log_compact.split_sections(new_text)[1]) != 12:
        return fail("compact did not keep 12")
    if "## Run 8 —" not in new_archive:
        return fail("older section not archived")
    again, _, moved_again = log_compact.compact_text(new_text, new_archive)
    if moved_again != 0 or again != new_text:
        return fail("second compact must be a no-op")
    print("LOG COMPACT CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
