#!/usr/bin/env python3
"""Print a concise one-page system status summary.

Aggregates key signals from STATE.md, NEXT.md, HANDOFF.md, and labor map
into a single short output. Reduces time for humans and agents to grasp
current state, blocker, and next action. Does not invent data, poll secrets,
or write files. Soft informational only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extract_latest_run(text: str) -> str:
    m = re.search(r"Run\s+(\d+)", text)
    return m.group(1) if m else "unknown"


def main() -> int:
    print("STATUS ONE-PAGER (concise current state; no invent, no poll)")
    print("=" * 60)

    state_path = ROOT / "STATE.md"
    if state_path.is_file():
        state = state_path.read_text(encoding="utf-8")
        print(f"Latest STATE note starts with Run {extract_latest_run(state)}")
        if "STALL_OAUTH_IDLE" in state:
            print("Primary blocker: STALL_OAUTH_IDLE (human OAuth secrets)")
        if "published=0" in state or "published: 0" in state.lower():
            print("Videos published: 0")
    else:
        print("STATE.md: MISSING")

    next_path = ROOT / "NEXT.md"
    if next_path.is_file():
        nxt = next_path.read_text(encoding="utf-8")
        if "human only" in nxt.lower() or "OAuth" in nxt:
            print("Next action: human OAuth (three secrets + execute=true dispatch)")
            print("  Start: python3 tools/human_starter.py")
            print("  Or: python3 tools/oauth_complete_guide.py")
    else:
        print("NEXT.md: MISSING")

    handoff_path = ROOT / "HANDOFF.md"
    if handoff_path.is_file():
        ho = handoff_path.read_text(encoding="utf-8")
        print(f"HANDOFF latest Run {extract_latest_run(ho)}")
        if "pre-upload path reliable" in ho.lower() or "Pre-upload path" in ho:
            print("Pre-upload path: reliable / complete")
    else:
        print("HANDOFF.md: MISSING")

    labor_path = ROOT / "docs" / "labor_reduction_map.md"
    if labor_path.is_file():
        labor = labor_path.read_text(encoding="utf-8")
        if "10–20" in labor or "10-20" in labor:
            print("Estimated human minutes to first private video: ~10–20 (OAuth only)")
        if "recurring human minutes" in labor.lower():
            print("Target recurring after first publish: < 30 min/video")
    else:
        print("labor_reduction_map.md: MISSING")

    print()
    print("Verification tip: after any update, run:")
    print("  python3 tools/tracking_integrity_check.py")
    print("  python3 tools/run_number_consistency_check.py")
    print()
    print("Do not rematerialize media if present. Do not poll secrets.")
    print("STATUS ONE-PAGER END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
