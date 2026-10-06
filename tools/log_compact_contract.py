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
    stacked = (
        "# FAILURES\n\n"
        "Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.\n\n"
        "## Run 3 — a\nnote\n\n"
        "# FAILURES\n\n"
        "Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.\n\n"
        "## Run 2 — b\nnote\n"
    )
    collapsed, _, moved_headers = log_compact.compact_text(stacked, "# ARCHIVE\n")
    if moved_headers != 0:
        return fail("header collapse must not archive")
    if collapsed.count("# FAILURES") != 1:
        return fail(f"stacked header survived: {collapsed.count('# FAILURES')}")
    if collapsed.count("Older failure notes live") != 1:
        return fail("stacked pointer survived")
    if "## Run 3 —" not in collapsed or "## Run 2 —" not in collapsed:
        return fail("collapse dropped a section")
    again_h, _, _ = log_compact.compact_text(collapsed, "# ARCHIVE\n")
    if again_h != collapsed:
        return fail("header collapse is not stable")
    bare = (
        "# PROGRESS\n\n"
        "Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.\n\n"
        "## Run 361 — 2026-10-06T10:12:00Z\nnote\n\n"
        "360 — 2026-10-06T09:11:00Z\nnote\n\n"
        "## Run 359 — 2026-10-06T08:11:00Z\nnote\n"
    )
    promoted, _, moved_bare = log_compact.compact_text(bare, "# ARCHIVE\n")
    if moved_bare != 0:
        return fail("bare header promotion must not archive")
    if "## Run 360 — 2026-10-06T09:11:00Z" not in promoted:
        return fail("bare run header was not promoted")
    if promoted.count("## Run ") != 3:
        return fail(f"bare promotion section count {promoted.count('## Run ')}")
    again_b, _, moved_b = log_compact.compact_text(promoted, "# ARCHIVE\n")
    if moved_b != 0 or again_b != promoted:
        return fail("bare promotion is not stable")
    print("LOG COMPACT CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
