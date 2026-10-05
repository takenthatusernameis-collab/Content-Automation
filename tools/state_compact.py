#!/usr/bin/env python3
"""Keep STATE.md short enough that a truncated fetch still shows the current gate.

Stall watch reads the newest deltas only. Older sections move to
docs/state_archive.md. This tool does not poll OAuth and does not write packets.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "STATE.md"
ARCHIVE = ROOT / "docs" / "state_archive.md"
MAX_RUNS = 12
SPLIT = "## Run "


def split_runs(text: str) -> tuple[str, list[str]]:
    parts = text.split(SPLIT)
    return parts[0], parts[1:]


def compact_text(text: str, archive_text: str, max_runs: int = MAX_RUNS) -> tuple[str, str, int]:
    """Return new STATE, new archive, and how many sections were moved."""
    _preamble, runs = split_runs(text)
    if len(runs) <= max_runs:
        return text, archive_text, 0
    kept = runs[:max_runs]
    older = runs[max_runs:]
    moved = []
    for part in older:
        marker = SPLIT + part[:24]
        if marker in archive_text:
            continue
        moved.append(SPLIT + part)
    addition = "".join(moved)
    if addition and not archive_text.endswith("\n"):
        archive_text += "\n"
    new_archive = archive_text + addition
    # Preserve the current preamble. Callers that add a delta do that before compact.
    preamble = _preamble if _preamble.strip() else "# STATE\n\n"
    if not preamble.endswith("\n"):
        preamble += "\n"
    new_state = preamble + "".join(SPLIT + part for part in kept)
    return new_state, new_archive, len(older)


def main() -> int:
    if not STATE.is_file():
        print("REFUSE: STATE.md missing", file=sys.stderr)
        return 2
    archive_text = ARCHIVE.read_text() if ARCHIVE.is_file() else (
        "# STATE ARCHIVE\n\nOlder STATE deltas. Do not delete.\n\n"
    )
    new_state, new_archive, moved = compact_text(STATE.read_text(), archive_text)
    if moved == 0:
        print(f"STATE COMPACT OK runs={new_state.count(SPLIT)} moved=0")
        return 0
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE.write_text(new_archive)
    STATE.write_text(new_state)
    print(f"STATE COMPACT OK runs={new_state.count(SPLIT)} moved={moved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
