#!/usr/bin/env python3
"""Print a single concise next-action suggestion for agents while stalled.

Combines stall pattern suspicion with a preferred unblocked path (human step
or one capability gap) so agents do not rediscover the choice logic.
Does not poll secrets, does not dispatch, does not invent data or files.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str) -> str:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / script)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return (proc.stdout or "") + (proc.stderr or "")


def main() -> int:
    stall = run("stall_pattern_detector.py")
    suspicion = "UNKNOWN"
    for line in stall.splitlines():
        if "suspicion:" in line.lower() or line.strip().startswith("HIGH") or "HIGH" in line:
            if "HIGH" in line:
                suspicion = "HIGH"
            elif "MEDIUM" in line:
                suspicion = "MEDIUM"
            elif "LOW" in line:
                suspicion = "LOW"
            break
    print("NEXT SUGGESTION (anti-rediscovery; no invent)")
    print(f"stall_suspicion: {suspicion}")
    if suspicion == "HIGH":
        print("preferred: human_step (OAuth secrets + one private execute=true dispatch)")
        print("exact: python3 tools/human_next_action.py")
        print("or: new small reusable capability that compounds after publish")
        print("gap_hint: python3 tools/capability_gap_hint.py")
    else:
        print("preferred: inspect capability gaps or continue anti-rediscovery")
        print("gap_hint: python3 tools/capability_gap_hint.py")
        print("human_step still required for publish: python3 tools/human_next_action.py")
    print()
    print("Do not rematerialize if media PRESENT. Do not re-verify gates solely for confirmation.")
    print("Do not poll secrets. Preferred unblocked list remains complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
