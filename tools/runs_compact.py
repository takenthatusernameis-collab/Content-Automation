#!/usr/bin/env python3
"""Keep RUNS.md short enough that a truncated fetch still shows the newest runs.

Older entries move to docs/runs_archive.md. This tool does not delete history,
does not poll OAuth, and does not write packets.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RUNS.md"
ARCHIVE = ROOT / "docs" / "runs_archive.md"
MAX_RUNS = 12
HEADING = re.compile(r"^## (?:Run \d+\b|\d{4}-\d{2}-\d{2}.*\bRun \d+\b)")


def split_runs(text: str) -> tuple[str, list[str], str]:
    """Return preamble, newest-first entries, and the permanent footer."""
    lines = text.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if HEADING.match(line)]
    if not starts:
        return text, [], ""
    preamble = "".join(lines[: starts[0]])
    entries: list[str] = []
    for idx, start in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(lines)
        entries.append("".join(lines[start:end]).strip() + "\n")
    footer = ""
    if entries and "Permanent log." in entries[-1]:
        body, marker, rest = entries[-1].partition("Permanent log.")
        entries[-1] = body.strip() + "\n"
        footer = "Permanent log." + rest
        if not footer.endswith("\n"):
            footer += "\n"
    return preamble, entries, footer


TARGET_BYTES = 15500  # leave margin under the 16000 hard cap

def compact_text(text: str, archive_text: str, max_runs: int = MAX_RUNS) -> tuple[str, str, int]:
    """Return new RUNS, new archive, and how many entries were moved.
    
    Enforces both count and a soft byte target so a single long entry cannot
    push the live file over the hard size contract after a normal prepend.
    """
    preamble, entries, footer = split_runs(text)
    # First pass: respect max_runs
    if len(entries) <= max_runs:
        kept = entries
        older = []
    else:
        kept = entries[:max_runs]
        older = entries[max_runs:]
    # Size-aware second pass: drop more from the oldest end of kept until under target
    def current_size(k):
        body = preamble + "\n".join(part.strip() + "\n" for part in k)
        if footer:
            body = body.rstrip() + "\n\n" + footer.strip() + "\n"
        if not body.endswith("\n"):
            body += "\n"
        return len(body.encode()), body
    size, body = current_size(kept)
    extra_moved = []
    while size > TARGET_BYTES and len(kept) > 4:  # never go below 4 newest
        extra = kept.pop()  # remove oldest of the kept set
        extra_moved.append(extra)
        size, body = current_size(kept)
    older = older + extra_moved
    if not older:
        out = text if text.endswith("\n") else text + "\n"
        return out, archive_text, 0
    moved: list[str] = []
    for part in older:
        marker = part[:64]
        if marker in archive_text:
            continue
        moved.append(part.strip() + "\n")
    addition = "\n".join(moved)
    if addition:
        if archive_text and not archive_text.endswith("\n"):
            archive_text += "\n"
        archive_text = archive_text + ("\n" if archive_text.endswith("\n") else "") + addition
        if not archive_text.endswith("\n"):
            archive_text += "\n"
    body = preamble + "\n".join(part.strip() + "\n" for part in kept)
    if footer:
        body = body.rstrip() + "\n\n" + footer.strip() + "\n"
    if not body.endswith("\n"):
        body += "\n"
    return body, archive_text, len(older)


def main() -> int:
    if not RUNS.is_file():
        print("REFUSE: RUNS.md missing", file=sys.stderr)
        return 2
    archive_text = ARCHIVE.read_text() if ARCHIVE.is_file() else (
        "# RUNS ARCHIVE\n\n"
        "Older run log entries. Newest first inside each move. "
        "Do not paste these back into RUNS.md. Do not delete this file.\n\n"
    )
    new_runs, new_archive, moved = compact_text(RUNS.read_text(), archive_text)
    if moved == 0:
        print(f"RUNS COMPACT OK items={len(split_runs(new_runs)[1])} moved=0")
        return 0
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE.write_text(new_archive)
    RUNS.write_text(new_runs)
    print(f"RUNS COMPACT OK items={len(split_runs(new_runs)[1])} moved={moved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
