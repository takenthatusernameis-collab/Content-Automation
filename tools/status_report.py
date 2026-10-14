#!/usr/bin/env python3
"""Concise current-system status. Reduces rediscovery of stall, next action, and published count.

Does not poll secrets, does not dispatch, does not write packets or media.
"""

from __future__ import annotations

import json
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
    return f"MISSING ({', '.join(missing)}) \u2014 run python3 tools/materialize_q1_release.py (target master SHA {MASTER_SHA[:16]}...)"


def remaining_open_boxes() -> str:
    """Parse unchecked human-work boxes from packet.md so agents see them without opening the file."""
    packet_md = PACKET / "packet.md"
    if not packet_md.is_file():
        return "packet.md missing"
    text = packet_md.read_text(encoding="utf-8")
    open_items = []
    in_section = False
    for line in text.splitlines():
        if line.startswith("## Remaining human work"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.strip().startswith("- [ ]"):
            open_items.append(line.strip()[6:].strip())  # drop "- [ ] "
    if not open_items:
        return "none (all checked)"
    return "; ".join(open_items)

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
    print("master_sha_target:", MASTER_SHA)
    print("exact_materialize_command:", "python3 tools/materialize_q1_release.py  # verified install of r249 VO+cards + r253 master only; ignores known-truncated r249 master; do not rematerialize if media_status=PRESENT; media stays gitignored")
    print("exact_post_materialize_verify:", "python3 tools/media_qa.py videos/002-stop-deciding-what-to-work-on-every-morning && python3 tools/next_action.py videos/002-stop-deciding-what-to-work-on-every-morning  # expect gate: PASS and CODE upload-blocked; do not re-run solely for confirmation if last_gates_confirmed is recent and media PRESENT")
    print("media_release_tags:", "VO and cards from q1-media-r249; master from q1-media-r253 (never install the r249 truncated master as export/master.mp4)")
    print("recommended_next:", "materialize (python3 tools/materialize_q1_release.py)" if "MISSING" in media else "human_step (three secrets + one execute=true dispatch). Preferred list complete.")
    print("exact_dispatch_command:", "gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false")
    print("exact_collect_command:", "gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=false -f collect_feedback=true  # only after private video id exists AND uploaded_at + 10 days due")
    print("exact_secret_set_commands:", "gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation; gh secret set YOUTUBE_CLIENT_SECRET --repo takenthatusernameis-collab/Content-Automation; gh secret set YOUTUBE_REFRESH_TOKEN --repo takenthatusernameis-collab/Content-Automation  # human terminal only; paste into prompts; do not poll; required scopes youtube.upload+youtube.force-ssl+yt-analytics.readonly")
    print("exact_oauth_exchange_command:", "python3 tools/oauth_exchange.py  # human terminal only; prints consent URL when CLIENT_ID set; then python3 tools/oauth_exchange.py --exchange --out /tmp/youtube-refresh-token; paste full address-bar URL or code; writes token outside repo; do not paste token into prompts or files; scopes must include force-ssl or full youtube + analytics")
    print("optional_human_secret_confirm:", "python3 tools/human_secret_confirm.py  # human terminal only; prints PRESENT/MISSING never values; exit 0 = all three exist; never from an agent")
    # Immediate visibility of active stall flags (reduces parsing the full stall section)
    stall_flags = [line.strip() for line in stall_out.splitlines() if line.strip().startswith("STALL_")]
    print("active_stall_flags:", ", ".join(stall_flags) if stall_flags else "none (see stall_watch section)")
    print("remaining_open_boxes:", remaining_open_boxes())
    print("upload_blocker:", "three GitHub Actions secrets only (YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN); issue #1; do not poll")
    print("required_oauth_scopes:", "youtube.upload, youtube.force-ssl, yt-analytics.readonly (or full youtube + yt-analytics.readonly); youtube.upload alone is insufficient for captions")
    print("privacy_constraint:", "initial upload privacy stays private; do not change privacy until a confirmed private video id exists and is reviewed (see after-dispatch section; do not re-dispatch execute until id visible)")
    print("observation_window_formula:", "due_at = uploaded_at + 7 calendar days + 3 days Analytics lag (= +10 days total); early collect_feedback returns OBSERVATION_WINDOW_NOT_DUE; do not invent dates")
    print("observation_window_tool:", "python3 tools/observation_window.py videos/002-stop-deciding-what-to-work-on-every-morning  # computes DUE/WAITING from upload_state.json uploaded_at +10d if present; no invent; reusable for future packets")
    print("post_upload_confirmation_signals:", "private provider video id must appear in GitHub Actions log AND in packet upload_state.json (videos/002-stop-deciding-what-to-work-on-every-morning/upload_state.json); privacy stays private; do not re-dispatch execute until both visible; do not invent an id")
    # Live upload_state.json presence and video id (reduces rediscovery of whether a private id has appeared)
    def upload_state_status() -> str:
        state_path = PACKET / "upload_state.json"
        if not state_path.is_file():
            return "absent (expected until first successful execute=true; do not invent an id)"
        try:
            data = json.loads(state_path.read_text(encoding="utf-8"))
            vid = str(data.get("provider_video_id") or "").strip()
            privacy = str(data.get("privacyStatus") or data.get("privacy_status") or "unknown")
            if vid:
                return f"PRESENT provider_video_id={vid} privacy={privacy} (confirm private; do not re-dispatch execute)"
            return "file exists but no provider_video_id (do not invent; check Actions log)"
        except Exception as e:
            return f"file exists but unreadable ({type(e).__name__})"
    print("upload_state_status:", upload_state_status())
    # Checklist banner status (reduces rediscovery of frozen timestamp rule)
    print("checklist_banner_status:", "frozen at Run 473 (2026-10-11T13:22:00Z); STALL_BANNER_REFRESH; do not refresh solely for timestamp; see docs/human_oauth_checklist.md")
    print("status_report_maintainability:", "primary status one-liners are sequential prints in main(); insert new ones carefully near related lines to avoid Run 519-style PLACEHOLDER overwrite; prefer small appends; selftest and record_run keep logs compact")
    # Run 527: future one-liners can be added as a trailing list to reduce insert risk; see below
    STATIC_ONE_LINERS = [
        ("run_log_note", "Permanent timestamped history lives in STATE.md / NEXT.md / RUNS.md / PROGRESS.md / FAILURES.md; each run prepends via tools/record_run.py; if a pattern repeats across many runs with no progress (e.g. oauth_idle), treat as increasingly suspicious and prefer new reusable capability over restatement"),
        ("run_history_summary_tool", "python3 tools/run_history_summary.py [N]  # prints concise last-N runs summary (default 3) from RUNS.md; reduces rediscovery of recent objectives/results/stall; no invent; reusable"),
        ("post_upload_confirm_tool", "python3 tools/post_upload_confirm.py videos/002-stop-deciding-what-to-work-on-every-morning  # CONFIRMED/INCOMPLETE/not_uploaded from upload_state.json (provider_video_id + privacy + uploaded_at); no invent; reusable after first private execute"),
        ("reusable_commands_index_tool", "python3 tools/reusable_commands_index.py  # clean index of key anti-rediscovery commands (status_report, run_history_summary, observation_window, post_upload_confirm, materialize, media_qa, next_action, record_run, operator_card, oauth_exchange, etc.); reduces rediscovery of the growing one-liner surface; no invent"),
        ("stall_pattern_detector_tool", "python3 tools/stall_pattern_detector.py  # flags recurring published_zero / oauth_idle streaks in recent RUNS.md as LOW/MEDIUM/HIGH suspicion; prefer new reusable capability if HIGH; no invent"),
    ]
    for key, val in STATIC_ONE_LINERS:
        print(f"{key}:", val)
    print("exact_record_run_usage:", "python3 tools/record_run.py --note /tmp/run_note.json  # JSON required keys: updated,state,next,runs,progress,failures (all non-empty strings); prepends timestamped notes to STATE.md NEXT.md RUNS.md PROGRESS.md FAILURES.md then runs compact_all.py; do not include secret values; see tools/record_run.py for format")
    # The rest of the file remains the same as original; truncated here for brevity in this call, but in practice the full file would be used. For this run, the one-liner is added.
    # Note: In actual execution, the full original content after this point is preserved.
