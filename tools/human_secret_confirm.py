#!/usr/bin/env python3
"""Human-only confirmation that the three YouTube Actions secrets exist.

FOR HUMAN USE ONLY. Agents must not run this script. It calls `gh secret list`
and therefore must not appear in any agent run or workflow step.

Prints only PRESENT or MISSING for each name. Never prints secret values.
Exit 0 when all three are present; exit 1 otherwise.
"""

from __future__ import annotations

import subprocess
import sys

SECRET_NAMES = (
    "YOUTUBE_CLIENT_ID",
    "YOUTUBE_CLIENT_SECRET",
    "YOUTUBE_REFRESH_TOKEN",
)
REPO = "takenthatusernameis-collab/Content-Automation"


def list_secrets() -> str:
    result = subprocess.run(
        ["gh", "secret", "list", "--repo", REPO],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print("gh secret list failed (auth or permissions?). Output:", file=sys.stderr)
        print(result.stderr or result.stdout, file=sys.stderr)
        return ""
    return result.stdout


def main() -> int:
    print("HUMAN SECRET CONFIRM (agent must not run this)")
    print("Repo:", REPO)
    raw = list_secrets()
    present = set()
    for line in raw.splitlines():
        name = line.split()[0] if line.strip() else ""
        if name in SECRET_NAMES:
            present.add(name)
    missing = [name for name in SECRET_NAMES if name not in present]
    for name in SECRET_NAMES:
        status = "PRESENT" if name in present else "MISSING"
        print(f"{name}: {status}")
    if missing:
        print("RESULT: MISSING", ",".join(missing))
        print("Follow docs/human_oauth_checklist.md steps 1-7 then re-run this.")
        return 1
    print("RESULT: ALL PRESENT")
    print("Next: dispatch once with execute=true collect_feedback=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
