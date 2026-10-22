#!/usr/bin/env python3
"""Contract lock for the shared idea.md field extractor.

Future runs can prove tools/idea_utils.extract stays consistent
instead of allowing local parsers to drift again.
Writes nothing. Exits 0 on pass, 1 on failure.
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract  # noqa: E402


def check() -> list[str]:
    failures: list[str] = []

    # Full fields
    text = """# Idea
mechanism: Write the next action on a sticky note.
problem: The stall is deciding what to work on.
topic: Stop deciding what to work on every morning
"""
    mech, problem, topic = extract(text)
    if mech != "Write the next action on a sticky note":
        failures.append(f"full mech mismatch: {mech!r}")
    if problem != "The stall is deciding what to work on":
        failures.append(f"full problem mismatch: {problem!r}")
    if topic != "Stop deciding what to work on every morning":
        failures.append(f"full topic mismatch: {topic!r}")

    # Missing fields stay empty
    text2 = """# Idea
topic: Only a topic
"""
    mech2, problem2, topic2 = extract(text2)
    if mech2 or problem2:
        failures.append(f"missing fields not empty: {mech2!r} {problem2!r}")
    if topic2 != "Only a topic":
        failures.append(f"topic-only mismatch: {topic2!r}")

    # Case insensitivity and trailing period strip
    text3 = """MECHANISM: The written default.
PROBLEM: Naming the next action.
TOPIC: Morning decision stall.
"""
    mech3, problem3, topic3 = extract(text3)
    if mech3 != "The written default":
        failures.append(f"case/period mech: {mech3!r}")
    if problem3 != "Naming the next action":
        failures.append(f"case/period problem: {problem3!r}")
    if topic3 != "Morning decision stall":
        failures.append(f"case/period topic: {topic3!r}")

    # Extra prose does not break
    text4 = """Some intro.
mechanism: Concrete install step.
Then more text.
problem: The reopen loop.
topic: Default on a note
End.
"""
    mech4, problem4, topic4 = extract(text4)
    if mech4 != "Concrete install step" or problem4 != "The reopen loop" or topic4 != "Default on a note":
        failures.append(f"extra prose broke extract: {mech4!r} {problem4!r} {topic4!r}")

    # Empty input
    if extract("") != ("", "", ""):
        failures.append("empty input not all empty")

    return failures


def main() -> int:
    fails = check()
    if fails:
        print("IDEA_UTILS_CONTRACT FAIL")
        for f in fails:
            print(f"- {f}")
        return 1
    print("IDEA_UTILS_CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
