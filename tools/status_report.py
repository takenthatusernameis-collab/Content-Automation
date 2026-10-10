#!/usr/bin/env python3
"""Concise current-system status. Reduces rediscovery of stall, next action, and published count.

Does not poll secrets, does not dispatch, does not write packets or media.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, args: list[str] | None = None) -> str:
    cmd = [sys.executable, str(ROOT / "tools" / script)] + (args or [])
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return (proc.stdout or "") + (proc.stderr or "")


def videos_published_from_state() -> str:
    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    # Look for the most recent mention
    for line in state.splitlines():
        if "Videos published stay 0" in line or "Videos published: 0" in line or "videos published stay 0" in line.lower():
            return "0"
        if "Videos published" in line and "stay" not in line.lower():
            return line.strip()
    return "unknown (see STATE.md)"


def main() -> int:
    print("STATUS REPORT")
    print("videos_published:", videos_published_from_state())
    print()
    print("--- stall_watch ---")
    print(run_tool("stall_watch.py").strip())
    print()
    print("--- next_action (Q1) ---")
    print(run_tool("next_action.py", ["videos/002-stop-deciding-what-to-work-on-every-morning"]).strip())
    print()
    print("--- human step ---")
    print("Follow docs/human_oauth_checklist.md or python3 tools/operator_card.py")
    print("Then set the three secrets and dispatch execute=true once.")
    print("Do not rematerialize if media present. Do not reopen closed briefs.")
    print("Pure verification has diminishing returns while STALL_OAUTH_IDLE is set.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
