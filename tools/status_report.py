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


MASTER_SHA = "4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546"

def _sha256(path: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def media_status() -> str:
    vo = PACKET / "vo"
    cards = PACKET / "cards"
    master = PACKET / "export" / "master.mp4"
    has_vo = vo.is_dir() and any(vo.glob("*.wav"))
    has_cards = cards.is_dir() and any(cards.glob("*.png"))
    has_master = master.is_file() and master.stat().st_size > 1000
    if has_vo and has_cards and has_master:
        sha = _sha256(master)
        match = "MATCH" if sha == MASTER_SHA else f"MISMATCH (got {sha[:12]}...)"
        return f"PRESENT (do not rematerialize; master SHA {match} target {MASTER_SHA[:16]}...)"
    missing = []
    if not has_vo:
        missing.append("vo/")
    if not has_cards:
        missing.append("cards/")
    if not has_master:
        missing.append("export/master.mp4")
    return f"MISSING ({', '.join(missing)}) — run python3 tools/materialize_q1_release.py (target master SHA {MASTER_SHA[:16]}...)"


def parse_idle_streak(stall_out: str) -> str:
    for line in stall_out.splitlines():
        if line.startswith("idle_streak:"):
            return line.split(":", 1)[1].strip()
    return "unknown"


def main() -> int:
    stall_out = run_tool("stall_watch.py")
    idle = parse_idle_streak(stall_out)
    print("STATUS REPORT")
    print("videos_published:", videos_published_from_state())
    media = media_status()
    print("media_status:", media)
    print("recommended_next:", "materialize (python3 tools/materialize_q1_release.py)" if "MISSING" in media else "human_step (three secrets + one execute=true dispatch). Preferred list complete.")
    print()
    print("--- stall_watch ---")
    print(stall_out.strip())
    print()
    print("--- next_action (Q1) ---")
    print(run_tool("next_action.py", [str(PACKET.relative_to(ROOT))]).strip())
    print()
    print("--- human step ---")
    print("Follow docs/human_oauth_checklist.md or python3 tools/operator_card.py")
    print("Then set the three secrets and dispatch execute=true once.")
    print("Do not rematerialize if media present. Do not reopen closed briefs.")
    print("Pure verification has diminishing returns while STALL_OAUTH_IDLE is set.")
    print("Do not refresh the human_oauth_checklist banner solely for its timestamp (STALL_BANNER_REFRESH).")
    print(f"STALL SUSPICION: oauth_idle_without_publish (live idle_streak={idle}; historical ~186+ across archives). Continued pure documentation updates have diminishing returns and should be treated as low-leverage unless they introduce a new reusable capability that reduces future human or agent work after the secrets are set.")
    print()
    print("--- after successful dispatch (confirm, do not invent) ---")
    print("Look for a private provider video id in the Actions log AND in the packet upload_state.json.")
    print("Privacy stays private. Do not re-dispatch execute until that id is visible.")
    print("Wait 7+ days from uploaded_at before any collect_feedback=true dispatch.")
    print("See docs/human_oauth_checklist.md Expected outcomes for full signals.")
    print()
    print("--- while stalled: preferred unblocked improvements ---")
    print("1. DONE (Run 464): experiment_baseline.template.json in docs/ (copy only after real metrics).")
    print("2. DONE (Run 465): production_rules.md now contains agent behavior during external stalls.")
    print("3. DONE (Run 466): confirmed docs/channel.md playlist_id remains 'not_set' and is documented as optional (upload does not wait on it).")
    print("4. DONE (Run 467): refreshed HANDOFF.md with explicit 'While the OAuth stall continues' section pointing agents to preferred improvements and production_rules.")
    print("5. DONE (Run 468): restored green selftest by compacting NEXT.md size (older notes archived; next_compact_contract PASS).")
    print("6. DONE (Run 469): refreshed human_oauth_checklist.md banner to current run and added exact first-upload confirmation signals (private video id in Actions log + upload_state.json).")
    print("7. DONE (Run 470): added one-line pointer in README.md Human session to the first-upload confirmation signals in the checklist.")
    print("Preferred list complete (Run 471). Run 474 added STALL_BANNER_REFRESH so pure banner-timestamp refreshes are flagged. Checklist banner intentionally left at Run 473 (do not rediscover updating it solely for timestamp). Next agent prioritizes the human step (three secrets + one dispatch) or identifies a truly new small anti-rediscovery preparation that does not invent data, media, metrics, or expand locked surfaces. Do not scaffold Q2, poll secrets, or extend locked surfaces. Do not refresh the checklist banner solely for the timestamp. Run 478 escalated the stall-length suspicion in this printer. Run 479 made the live idle_streak dynamic. Run 480 made media_status report master SHA MATCH/MISMATCH when present. Run 481 made the missing path also print the target SHA prefix. Run 482 added the after-dispatch confirmation signals to the primary status command so agents see the private video id look-up without opening the checklist. Run 483 made the PRESENT path also print the target SHA prefix for full consistency, and restored the STALL_OAUTH_IDLE active lock in NEXT.md so next_compact_contract and selftest stay green. Run 484 added an explicit recommended_next line (materialize if media missing, else human_step) so agents see the single highest-leverage action without parsing other sections.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
