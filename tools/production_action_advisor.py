#!/usr/bin/env python3
"""Single-command production next-action advisor.

Combines saturation guard, stall duration, publish readiness, and capability-gap hints
into one concise recommendation. Prefers the human OAuth step when saturated or long-stalled,
otherwise points to the highest-priority unblocked production capability.
No writes, no secret polling, no invented data. Stdlib only.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str) -> str:
    cmd = [sys.executable, str(ROOT / "tools" / script)]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return (proc.stdout or "") + (proc.stderr or "")


def main() -> int:
    print("PRODUCTION ACTION ADVISOR (consolidated; no invent, no poll)")
    print()

    sat = run("saturation_guard.py")
    stall = run("stall_duration.py")
    ready = run("publish_readiness.py")
    gap = run("capability_gap_hint.py")

    saturated = "SATURATED_ANTI_REDISCOVERY" in sat
    long_stall = "LONG_OAUTH_IDLE" in stall
    ready_for_dispatch = "READY_FOR_HUMAN_DISPATCH" in ready

    if saturated or long_stall or ready_for_dispatch:
        print("PRIMARY RECOMMENDATION: human OAuth step")
        print("  Reason: saturation / long stall / local readiness detected.")
        print("  Action: python3 tools/human_next_action.py")
        print("  Then set the three GitHub Actions secrets and dispatch execute=true once.")
        print("  Do not add another brief, candidates, or pure status tool.")
    else:
        print("PRIMARY RECOMMENDATION: advance a production capability")
        print("  Local readiness not fully confirming dispatch path; inspect capability gaps.")
        # Extract first gap line if present
        for line in gap.splitlines():
            if line.strip().startswith("1."):
                print(f"  Suggested: {line.strip()}")
                break
        else:
            print("  Run python3 tools/capability_gap_hint.py for details.")

    print()
    print("--- Supporting signals ---")
    print(sat.splitlines()[0] if sat else "saturation_guard unavailable")
    print(stall.splitlines()[0] if stall else "stall_duration unavailable")
    print(ready.splitlines()[0] if ready else "publish_readiness unavailable")
    print()
    print("Videos published remain 0 until OAuth secrets are set. Preferred list complete.")
    print("Do not poll secrets. Do not scaffold Q2.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
