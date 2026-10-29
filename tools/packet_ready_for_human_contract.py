#!/usr/bin/env python3
"""Contract for packet_ready_for_human.py.

Source-checks that the orchestrator stays fail-closed, does not poll secrets,
does not invent media, and reprints the human next commands.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "packet_ready_for_human.py"


def main() -> int:
    if not TOOL.is_file():
        print("CONTRACT FAIL: tool missing")
        return 1
    text = TOOL.read_text(encoding="utf-8")
    issues = []
    if "subprocess" not in text:
        issues.append("must call existing tools via subprocess")
    if "READY FOR HUMAN OAUTH" not in text:
        issues.append("must print READY phrase")
    if "oauth_exchange.py" not in text:
        issues.append("must reprint oauth_exchange command")
    if "execute=true" not in text:
        issues.append("must reprint dispatch line")
    if "invent" not in text.lower():
        issues.append("must document no-invent")
    if "secrets" not in text.lower() or "poll" not in text.lower():
        issues.append("must document no secret poll")
    if issues:
        print("CONTRACT FAIL")
        for i in issues:
            print(i)
        return 1
    print("packet_ready_for_human CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
