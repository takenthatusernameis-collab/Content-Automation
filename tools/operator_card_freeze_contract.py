#!/usr/bin/env python3
"""Contract for the operator-card freeze. Does not poll secrets."""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from operator_card_freeze import ALLOWED_CARD_FILES, EXPECTED_DEFS, mismatches  # noqa: E402


def fail(msg: str) -> int:
    print("OPERATOR CARD FREEZE CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    card = (TOOLS / "operator_card.py").read_text(encoding="utf-8")
    files = sorted(path.name for path in TOOLS.glob("operator_card*.py"))
    if mismatches(card, files):
        return fail(f"live surface drifted: {mismatches(card, files)}")
    grown = card + "\ndef extra_printer() -> None:\n    return None\n"
    if not mismatches(grown, files):
        return fail("an extra function must fail the freeze")
    extra_files = files + ["operator_card_v2.py"]
    if not mismatches(card, extra_files):
        return fail("a second card module must fail the freeze")
    polling = card.replace("from oauth_setup import", "import subprocess\nfrom oauth_setup import", 1)
    if not mismatches(polling, files):
        return fail("a subprocess import must fail the freeze")
    if "operator_card.py" not in ALLOWED_CARD_FILES:
        return fail("allowed set lost the card")
    if len(EXPECTED_DEFS) != 5:
        return fail("frozen def count drifted")
    print("OPERATOR CARD FREEZE CONTRACT PASS")
    print("extra def, extra module, and subprocess import fail")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
