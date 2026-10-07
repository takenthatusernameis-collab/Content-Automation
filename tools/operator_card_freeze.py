#!/usr/bin/env python3
"""Freeze the operator-card surface while nothing is published.

Runs 383-384 each extended the one human command while videos published
stayed 0. A prose lock did not stop the next reprint. This check fails if
operator_card.py grows another function, if a second card module appears,
or if the card starts calling GitHub or YouTube. It does not poll secrets
and does not add a recovery edge.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD = ROOT / "tools" / "operator_card.py"
TOOLS = ROOT / "tools"

# Exact surface on the Run 385 tree. A new def is another card extension.
EXPECTED_DEFS = (
    "def dispatch_line(",
    "def console_steps(",
    "def card_text(",
    "def problems(",
    "def main(",
)
ALLOWED_CARD_FILES = {
    "operator_card.py",
    "operator_card_contract.py",
    "operator_card_freeze.py",
    "operator_card_freeze_contract.py",
}
FORBIDDEN_IMPORTS = ("subprocess", "requests", "urllib", "http.client")


def card_files() -> list[str]:
    return sorted(path.name for path in TOOLS.glob("operator_card*.py") if path.is_file())


def mismatches(card: str, files: list[str]) -> list[str]:
    problems = []
    defs = [line.strip() for line in card.splitlines() if line.startswith("def ")]
    if len(defs) != len(EXPECTED_DEFS) or any(
        not defs[i].startswith(EXPECTED_DEFS[i]) for i in range(min(len(defs), len(EXPECTED_DEFS)))
    ):
        problems.append(f"def surface {defs}, want prefixes {list(EXPECTED_DEFS)}")
    elif len(defs) != len(EXPECTED_DEFS):
        problems.append(f"def count {len(defs)}, want {len(EXPECTED_DEFS)}")
    unexpected = [name for name in files if name not in ALLOWED_CARD_FILES]
    for name in unexpected:
        problems.append(f"unexpected card module {name}")
    if "operator_card.py" not in files:
        problems.append("operator_card.py missing")
    for token in FORBIDDEN_IMPORTS:
        if f"import {token}" in card or f"from {token}" in card:
            problems.append(f"card imports {token}")
    if card.count("Human step:") != 1:
        problems.append(f"Human step count {card.count('Human step:')}, want 1")
    return problems


def main() -> int:
    if not CARD.is_file():
        print("OPERATOR CARD FREEZE FAIL")
        print("operator_card.py missing")
        return 1
    problems = mismatches(CARD.read_text(encoding="utf-8"), card_files())
    if problems:
        print("OPERATOR CARD FREEZE FAIL")
        print("Do not extend the operator card while videos published stay 0.")
        for item in problems:
            print(item)
        return 1
    print("OPERATOR CARD FREEZE PASS")
    print("operator_card defs=5 card_modules=frozen")
    print("did not extend operator_card")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
