#!/usr/bin/env python3
"""Lock the STATE.md size cap. A truncated fetch must still show the newest deltas."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import state_compact  # noqa: E402


def fail(msg: str) -> int:
    print(f"FAIL: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    state = (ROOT / "STATE.md").read_text()
    runs = state.count("## Run ")
    if runs > state_compact.MAX_RUNS:
        return fail(f"STATE.md has {runs} run sections, max {state_compact.MAX_RUNS}")
    if not (ROOT / "docs" / "state_archive.md").is_file():
        return fail("docs/state_archive.md missing")
    newest = state.split("## Run ", 1)
    if len(newest) < 2 or "delta" not in newest[1][:80]:
        return fail("newest delta missing from STATE.md")
    bloated = "# STATE\n\n" + "".join(
        f"## Run {i} delta\n- filler\n\n" for i in range(20, 0, -1)
    )
    new_state, new_archive, moved = state_compact.compact_text(bloated, "# STATE ARCHIVE\n\n")
    if moved != 8:
        return fail(f"expected to move 8, moved {moved}")
    if new_state.count("## Run ") != 12:
        return fail("compact did not keep 12")
    if "## Run 20 delta" not in new_state or "## Run 9 delta" not in new_state:
        return fail("kept the wrong end")
    if "## Run 8 delta" not in new_archive:
        return fail("older delta not archived")
    again, _, moved_again = state_compact.compact_text(new_state, new_archive)
    if moved_again != 0 or again != new_state:
        return fail("second compact must be a no-op")
    if new_state.count("# STATE") != 1:
        return fail("compact left more than one STATE header")
    stacked = ""
    for i in range(15, 0, -1):
        stacked += f"# STATE\n\nUpdated: run {i}\n\n## Run {i} delta\n- filler\n\n"
    stacked_state, stacked_archive, stacked_moved = state_compact.compact_text(
        stacked, "# STATE ARCHIVE\n\n"
    )
    if stacked_state.count("# STATE") != 1:
        return fail("stacked headers were not collapsed")
    if stacked_moved != 3 or stacked_state.count("## Run ") != 12:
        return fail(f"stacked compact moved {stacked_moved}")
    if "Updated: run 15" not in stacked_state or "## Run 3 delta" not in stacked_archive:
        return fail("stacked compact kept the wrong end")
    if state.count("# STATE") != 1:
        return fail(f"STATE.md has {state.count('# STATE')} headers; compact before commit")
    print("STATE COMPACT CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
