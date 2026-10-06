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
    """Return the newest preamble and run bodies.

    Agents prepend a full `# STATE` file. Those extra headers used to stay
    inside the previous section, so a size cap could cut a delta and leave
    a dangling header. Only the first preamble is kept. Each `## Run` body
    is stored without a following header.
    """
    preamble = ""
    runs: list[str] = []
    chunks = text.split("# STATE")
    if len(chunks) == 1:
        parts = text.split(SPLIT)
        pre = parts[0]
        return (pre if pre.strip() else "# STATE\n\n"), parts[1:]
    for chunk in chunks:
        body = chunk.strip()
        if not body:
            continue
        if SPLIT not in body:
            if not preamble:
                preamble = "# STATE\n\n" + body + "\n\n"
            continue
        pre, rest = body.split(SPLIT, 1)
        if not preamble and pre.strip():
            preamble = "# STATE\n\n" + pre.strip() + "\n\n"
        for part in rest.split(SPLIT):
            part = part.strip()
            if part:
                runs.append(part + "\n\n")
    if not preamble:
        preamble = "# STATE\n\n"
    return preamble, runs


def compact_text(text: str, archive_text: str, max_runs: int = MAX_RUNS) -> tuple[str, str, int]:
    """Return new STATE, new archive, and how many sections were moved."""
    preamble, runs = split_runs(text)
    if not preamble.endswith("\n"):
        preamble += "\n"
    def render(parts: list[str]) -> str:
        return preamble + "".join(SPLIT + part for part in parts)

    if len(runs) <= max_runs:
        cleaned = render(runs)
        if cleaned == text:
            return text, archive_text, 0
        return cleaned, archive_text, 0
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
    new_state = render(kept)
    return new_state, new_archive, len(older)


def main() -> int:
    if not STATE.is_file():
        print("REFUSE: STATE.md missing", file=sys.stderr)
        return 2
    archive_text = ARCHIVE.read_text() if ARCHIVE.is_file() else (
        "# STATE ARCHIVE\n\nOlder STATE deltas. Do not delete.\n\n"
    )
    new_state, new_archive, moved = compact_text(STATE.read_text(), archive_text)
    if moved == 0 and new_state == STATE.read_text():
        print(f"STATE COMPACT OK runs={new_state.count(SPLIT)} moved=0")
        return 0
    if new_archive != archive_text:
        ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
        ARCHIVE.write_text(new_archive)
    STATE.write_text(new_state)
    if moved == 0:
        print(f"STATE COMPACT OK runs={new_state.count(SPLIT)} moved=0 collapsed=1")
        return 0
    print(f"STATE COMPACT OK runs={new_state.count(SPLIT)} moved={moved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
