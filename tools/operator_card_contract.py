#!/usr/bin/env python3
"""Lock the operator card to the oauth_setup dispatch. Does not call GitHub."""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from operator_card import DISPATCH, MASTER_SHA, SECRET_NAMES, problems


def fail(msg: str) -> int:
    print("OPERATOR CARD CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    from oauth_setup import recipe
    from operator_card import card_text, console_steps
    handoff = f"SHA256: `{MASTER_SHA}`\n"
    setup = recipe()
    card = card_text()
    if problems(handoff, setup, card):
        return fail("aligned card must pass: " + ", ".join(problems(handoff, setup, card)))
    if console_steps(setup) not in card or "Desktop app" not in card:
        return fail("aligned card must reprint console steps")
    if not problems("no sha here", setup, card):
        return fail("a missing master sha must fail")
    drifted = setup.replace(DISPATCH, DISPATCH + " -f packet=q2")
    if not problems(handoff, drifted, card):
        return fail("a drifted dispatch must fail")
    polling = card.replace("Do not run gh secret list. ", "gh secret list\n")
    if not problems(handoff, setup, polling):
        return fail("a secret poll command must fail")
    print("OPERATOR CARD CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
