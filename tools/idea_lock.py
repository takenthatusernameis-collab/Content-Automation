#!/usr/bin/env python3
"""Read-only idea-lock overlap printer.

Prints the same INFO lines apply_script.py dry-run prints, against
PATH/draft.md when present else PATH/script.md. Never writes. Never
changes an exit code. A lock miss is not apply --write.

Run after words.py, or rely on words.py once it imports idea_lock_notes.
Unmapped. Not a reconstruct wave.
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python3 tools/idea_lock.py PATH", file=sys.stderr)
        print("This command writes nothing.", file=sys.stderr)
        return 2
    target = Path(sys.argv[1])
    packet = target if target.is_dir() else target.parent
    if target.is_file():
        draft = target
    elif (packet / "draft.md").is_file():
        draft = packet / "draft.md"
    elif (packet / "script.md").is_file():
        draft = packet / "script.md"
    else:
        print(f"INFO no draft.md or script.md under {packet}")
        print("This command writes nothing.")
        return 0
    text = draft.read_text(encoding="utf-8")
    print(f"Source: {draft}")
    try:
        from apply_script import idea_lock_notes, extract_script

        body = extract_script(text)
        for note in idea_lock_notes(packet, body):
            print(note)
    except Exception as exc:
        print(f"INFO idea lock printer unavailable ({exc}); apply dry-run still prints it")
    print("This command writes nothing.")
    print("Lock INFO does not block apply --write.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
