#!/usr/bin/env python3
"""Freeze the provider-state recovery surface while nothing is published.

Runs 368-378 each added another recover path. A prose lock did not stop the
next edge. This check fails if the production workflow grows another
provider-upload-state artifact or another recover call. It does not call
YouTube or GitHub and does not add a recovery edge.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "youtube-production.yml"
PERSIST = ROOT / "tools" / "persist_provider_state.py"

# Exact counts on the Run 382 tree. A comment that names the push command is
# included. Raising any count is a new recovery edge.
EXPECTED = {
    "name: provider-upload-state": 1,
    "persist_provider_state.py recover": 1,
    "persist_provider_state.py push": 3,
}
PERSIST_EXPECTED = {
    'RECOVERY_ARTIFACT = "provider-upload-state"': 1,
    "def artifact_recovery_command": 1,
}


def surface_counts(workflow: str, persist: str) -> dict[str, int]:
    counts = {token: workflow.count(token) for token in EXPECTED}
    counts.update({token: persist.count(token) for token in PERSIST_EXPECTED})
    return counts


def mismatches(workflow: str, persist: str) -> list[str]:
    counts = surface_counts(workflow, persist)
    expected = {**EXPECTED, **PERSIST_EXPECTED}
    problems = []
    for token, want in expected.items():
        got = counts[token]
        if got != want:
            problems.append(f"{token!r} count {got}, want {want}")
    return problems


def main() -> int:
    if not WORKFLOW.is_file() or not PERSIST.is_file():
        print("RECOVERY FREEZE FAIL")
        print("missing workflow or persist_provider_state.py")
        return 1
    problems = mismatches(
        WORKFLOW.read_text(encoding="utf-8"),
        PERSIST.read_text(encoding="utf-8"),
    )
    if problems:
        print("RECOVERY FREEZE FAIL")
        print("Do not add another provider-state recovery edge while videos published stay 0.")
        for item in problems:
            print(item)
        return 1
    print("RECOVERY FREEZE PASS")
    print("provider-upload-state artifact=1 recover_call=1")
    print("no new recovery edge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
