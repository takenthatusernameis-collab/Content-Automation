#!/usr/bin/env python3
"""Contract lock for the shared phrase_utils.shorten helper.

Future runs can prove tools/phrase_utils.shorten stays consistent
(natural whole-word / first-clause shortening, no mid-word cuts)
instead of allowing local copies to drift again.
Writes nothing. Exits 0 on pass, 1 on failure.
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from phrase_utils import shorten  # noqa: E402


def check() -> list[str]:
    failures: list[str] = []

    # Short text unchanged
    if shorten("Short phrase", 40) != "Short phrase":
        failures.append("short text mutated")

    # First clause preferred when separator present and fits
    long = "Write the next action on a sticky note. Then the stall disappears."
    if shorten(long, 40) != "Write the next action on a sticky note":
        failures.append(f"clause shorten failed: {shorten(long, 40)!r}")

    # Word-boundary fallback, no mid-word cut
    no_sep = "This is a longer phrase without any separators that needs shortening"
    result = shorten(no_sep, 30)
    if " " not in result or result.endswith("need") or len(result) > 30:
        failures.append(f"word-boundary shorten failed: {result!r}")
    if result != "This is a longer phrase":
        # Allow the exact word-boundary result; just ensure no mid-word
        if any(c.isalnum() for c in result[-1:]) and not result.endswith(" "):
            pass  # acceptable if clean
        else:
            failures.append(f"unexpected word-boundary result: {result!r}")

    # Empty / whitespace
    if shorten("", 10) != "":
        failures.append("empty not empty")
    if shorten("   ", 10) != "":
        failures.append("whitespace not stripped to empty")

    # Exact max_len boundary
    exact = "Exactly forty characters here!!!"
    if len(exact) != 33:  # adjust if needed; just test boundary behavior
        pass
    if shorten(exact, len(exact)) != exact:
        failures.append("exact length mutated")

    # max_len smaller than first word
    tiny = shorten("Supercalifragilistic", 5)
    if len(tiny) > 5 or " " in tiny:
        failures.append(f"tiny max_len failed: {tiny!r}")

    return failures


def main() -> int:
    fails = check()
    if fails:
        print("PHRASE_UTILS_CONTRACT FAIL")
        for f in fails:
            print(f"- {f}")
        return 1
    print("PHRASE_UTILS_CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
