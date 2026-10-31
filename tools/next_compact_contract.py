#!/usr/bin/env python3
"""Lock the NEXT.md size cap. A truncated fetch must still show the newest notes."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import next_compact  # noqa: E402


def fail(msg: str) -> int:
    print(f"FAIL: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    text = (ROOT / "NEXT.md").read_text()
    _pre, items = next_compact.split_items(text)
    if len(items) > next_compact.MAX_ITEMS:
        return fail(f"NEXT.md has {len(items)} notes, max {next_compact.MAX_ITEMS}")
    if len(text.encode()) > 12000:
        return fail(f"NEXT.md is {len(text.encode())} bytes")
    if "docs/next_archive.md" not in text:
        return fail("archive pointer missing")
    if "STALL_OAUTH_IDLE" not in text or "scaffold Q2" not in text:
        return fail("active lock missing")
    archive = ROOT / "docs" / "next_archive.md"
    if not archive.is_file():
        return fail("docs/next_archive.md missing")
    archived = archive.read_text()
    if "Do not rediscover the materialize abort" not in archived:
        return fail("materialize note missing from archive")
    if "Do not restore multipart" not in archived:
        return fail("multipart note missing from archive")
    bloated = "\n\n".join(f"{i}. **Do not rediscover filler {i}.** note\n" for i in range(20, 0, -1))
    new_next, new_archive, moved = next_compact.compact_text(bloated, "# NEXT ARCHIVE\n\n")
    if moved != 14:
        return fail(f"expected to move 8, moved {moved}")
    if len(next_compact.split_items(new_next)[1]) != 6:
        return fail("compact did not keep 12")
    if not new_next.startswith("20. "):
        return fail("kept the wrong end")
    if "8. **Do not rediscover filler 8.**" not in new_archive:
        return fail("older note not archived")
    again, _, moved_again = next_compact.compact_text(new_next, new_archive)
    if moved_again != 0 or again != new_next:
        return fail("second compact must be a no-op")
    dup = "# NEXT\n\nActive locks: one.\n\nActive locks: two longer.\n\n.\n\n1. note\n"
    collapsed, _, moved_dup = next_compact.compact_text(dup, "# NEXT ARCHIVE\n\n")
    if moved_dup != 0:
        return fail("duplicate locks must not archive the note")
    if collapsed.count("Active locks:") != 1 or "Active locks: two" in collapsed:
        return fail("duplicate active locks not collapsed")
    if "\n.\n" in collapsed or collapsed.strip().splitlines()[-1] == ".":
        return fail("dot paragraph kept")
    again_dup, _, moved_dup2 = next_compact.compact_text(collapsed, "# NEXT ARCHIVE\n\n")
    if moved_dup2 != 0 or again_dup != collapsed:
        return fail("collapsed preamble must be stable")
    print("NEXT COMPACT CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
