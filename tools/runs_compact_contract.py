#!/usr/bin/env python3
"""Lock the RUNS.md size cap. A truncated fetch must still show the newest runs."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import runs_compact  # noqa: E402


def fail(msg: str) -> int:
    print(f"FAIL: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    text = (ROOT / "RUNS.md").read_text()
    _pre, items, footer = runs_compact.split_runs(text)
    if len(items) > runs_compact.MAX_RUNS:
        return fail(f"RUNS.md has {len(items)} runs, max {runs_compact.MAX_RUNS}")
    if len(text.encode()) > 16000:
        return fail(f"RUNS.md is {len(text.encode())} bytes")
    if "docs/runs_archive.md" not in text:
        return fail("archive pointer missing")
    if "Permanent log." not in footer:
        return fail("permanent log footer missing")
    archive = ROOT / "docs" / "runs_archive.md"
    if not archive.is_file():
        return fail("docs/runs_archive.md missing")
    archived = archive.read_text()
    if "Run 270" not in archived:
        return fail("Run 270 missing from archive")
    bloated = "\n\n".join(
        f"## Run {i} — 2026-01-01T00:00:00Z\n- filler {i}\n" for i in range(20, 0, -1)
    )
    new_runs, new_archive, moved = runs_compact.compact_text(
        bloated + "\nPermanent log. Newest first.\n",
        "# RUNS ARCHIVE\n\n",
    )
    if moved != 8:
        return fail(f"expected to move 8, moved {moved}")
    kept = runs_compact.split_runs(new_runs)[1]
    if len(kept) != 12:
        return fail("compact did not keep 12")
    if not kept[0].startswith("## Run 20"):
        return fail("kept the wrong end")
    if "## Run 8 —" not in new_archive:
        return fail("older run not archived")
    if "Permanent log." not in new_runs:
        return fail("footer dropped")
    again, _, moved_again = runs_compact.compact_text(new_runs, new_archive)
    if moved_again != 0 or again != new_runs:
        return fail("second compact must be a no-op")
    print("RUNS COMPACT CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
