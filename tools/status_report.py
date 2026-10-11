#!/usr/bin/env python3
"""Concise current-system status. Reduces rediscovery of stall, next action, and published count.

Does not poll secrets, does not dispatch, does not write packets or media.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


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


def media_status() -> str:
    vo = PACKET / "vo"
    cards = PACKET / "cards"
    master = PACKET / "export" / "master.mp4"
    has_vo = vo.is_dir() and any(vo.glob("*.wav"))
    has_cards = cards.is_dir() and any(cards.glob("*.png"))
    has_master = master.is_file() and master.stat().st_size > 1000
    if has_vo and has_cards and has_master:
        return "PRESENT (do not rematerialize)"
    missing = []
    if not has_vo:
        missing.append("vo/")
    if not has_cards:
        missing.append("cards/")
    if not has_master:
        missing.append("export/master.mp4")
    return f"MISSING ({', '.join(missing)}) — run python3 tools/materialize_q1_release.py"


def main() -> int:
    print("STATUS REPORT")
    print("videos_published:", videos_published_from_state())
    print("media_status:", media_status())
    print()
    print("--- stall_watch ---")
    print(run_tool("stall_watch.py").strip())
    print()
    print("--- next_action (Q1) ---")
    print(run_tool("next_action.py", [str(PACKET.relative_to(ROOT))]).strip())
    print()
    print("--- human step ---")
    print("Follow docs/human_oauth_checklist.md or python3 tools/operator_card.py")
    print("Then set the three secrets and dispatch execute=true once.")
    print("Do not rematerialize if media present. Do not reopen closed briefs.")
    print("Pure verification has diminishing returns while STALL_OAUTH_IDLE is set.")
    print()
    print("--- while stalled: preferred unblocked improvements ---")
    print("1. DONE (Run 464): experiment_baseline.template.json in docs/ (copy only after real metrics).")
    print("2. DONE (Run 465): production_rules.md now contains agent behavior during external stalls.")
    print("3. DONE (Run 466): confirmed docs/channel.md playlist_id remains 'not_set' and is documented as optional (upload does not wait on it).")
    print("4. DONE (Run 467): refreshed HANDOFF.md with explicit 'While the OAuth stall continues' section pointing agents to preferred improvements and production_rules.")
    print("5. DONE (Run 468): restored green selftest by compacting NEXT.md size (older notes archived; next_compact_contract PASS).")
    print("6. Keep the human_oauth_checklist.md banner current with the latest stall observation.")
    print("Prefer one of these over pure verification. Do not scaffold Q2, poll secrets, or extend locked surfaces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
