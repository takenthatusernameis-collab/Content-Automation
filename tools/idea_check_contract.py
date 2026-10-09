#!/usr/bin/env python3
"""--check must accept a filled later packet that is not a queue row.

Read-only. Does not write idea.md, the queue, or videos/.
Run 417: suggested paste already kept the packet lines. --check still
compared those lines to the queue placeholder and printed PASTE INCOMPLETE.
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_brief import check_fields  # noqa: E402

BODY = """# Idea

- Topic: Close the extra tab before the next block
- Viewer: someone who opens a second tab instead of finishing the block
- Problem: an extra tab steals the next block
- Mechanism: close the extra tab before the next block
- Why now: the next block starts with one tab still open
"""


def main() -> int:
    failures: list[str] = []
    code, lines = check_fields(
        BODY,
        "Close the extra tab before the next block",
        Path("009-close-the-extra-tab-before-the-next-block"),
    )
    text = "\n".join(lines)
    if code != 0:
        failures.append(f"filled later packet --check exit {code}, want 0")
    if "PASTE READY" not in text:
        failures.append("filled later packet --check did not say PASTE READY")
    if "PASTE INCOMPLETE" in text:
        failures.append("filled later packet --check still says PASTE INCOMPLETE")
    if "MATCH problem" not in text:
        failures.append("filled later packet --check did not match the packet problem")
    if "no matching queue row" in text:
        failures.append("filled later packet --check still wants the queue placeholder")
    if "morning still reopens" in text:
        failures.append("filled later packet --check still wants the channel morning line")
    if failures:
        print("IDEA CHECK CONTRACT FAIL")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("IDEA CHECK CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
