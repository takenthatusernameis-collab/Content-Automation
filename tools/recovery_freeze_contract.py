#!/usr/bin/env python3
"""Lock the recovery-surface freeze. Does not call YouTube or GitHub."""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from recovery_freeze import mismatches


def fail(msg: str) -> int:
    print("RECOVERY FREEZE CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    workflow = (
        "name: provider-upload-state\n"
        "python3 tools/persist_provider_state.py recover\n"
        "python3 tools/persist_provider_state.py push\n"
        "python3 tools/persist_provider_state.py push\n"
        "echo tools/persist_provider_state.py push\n"
    )
    persist = (
        'RECOVERY_ARTIFACT = "provider-upload-state"\n'
        "def artifact_recovery_command():\n"
        "    return None\n"
    )
    if mismatches(workflow, persist):
        return fail("frozen counts must pass")
    grown = workflow + "name: provider-upload-state\n"
    if not mismatches(grown, persist):
        return fail("a second provider-upload-state artifact must fail")
    extra_recover = workflow + "python3 tools/persist_provider_state.py recover\n"
    if not mismatches(extra_recover, persist):
        return fail("a second recover call must fail")
    print("RECOVERY FREEZE CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
