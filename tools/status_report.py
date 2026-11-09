#!/usr/bin/env python3
"""Concise current-system status. Reduces rediscovery of stall, next action, and published count.

Does not poll secrets, does not dispatch, does not write packets or media.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, args: list[str] | None = None) -> str:
    cmd = [sys.executable, str(ROOT / "tools" / script)] + (args or [])
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return (proc.stdout or "") + (proc.stderr or "")


def videos_published_from_state() -> str:
    """Extract the current published count from the most recent STATE.md entry.
    Prefers explicit published=0 / published: 0. Returns "0" for the known long stall.
    """
    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    for line in state.splitlines():
        low = line.lower()
        if "published=0" in low or "published: 0" in low or "published stay 0" in low or "videos published: 0" in low:
            return "0"
        import re
        m = re.search(r"published[=:\s]+(\d+)", low)
        if m:
            return m.group(1)
    return "0"


MASTER_SHA = "4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546"

def _sha256(path: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def media_status(packet: Path) -> str:
    vo = packet / "vo"
    cards = packet / "cards"
    master = packet / "export" / "master.mp4"
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


def remaining_open_boxes(packet: Path) -> str:
    """Parse unchecked human-work boxes from packet.md so agents see them without opening the file."""
    packet_md = packet / "packet.md"
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
    parser = argparse.ArgumentParser(description="Concise current-system status. Optional --packet defaults to Q1.")
    parser.add_argument("--packet", default="videos/002-stop-deciding-what-to-work-on-every-morning", help="Packet path (default: current Q1)")
    args = parser.parse_args()
    PACKET = (ROOT / args.packet).resolve()
    stall_out = run_tool("stall_watch.py")
    idle = parse_idle_streak(stall_out)
    print("STATUS REPORT")
    packet_rel = str(PACKET.relative_to(ROOT))
    print("packet:", packet_rel)
    print("videos_published:", videos_published_from_state())
    media = media_status(PACKET)
    print("media_status:", media)
    print("master_sha_target:", MASTER_SHA)
    print("exact_materialize_command:", "python3 tools/materialize_q1_release.py  # verified install of r249 VO+cards + r253 master only; ignores known-truncated r249 master; do not rematerialize if media_status=PRESENT; media stays gitignored")
    print("exact_post_materialize_verify:", f"python3 tools/media_qa.py {packet_rel} && python3 tools/next_action.py {packet_rel}  # expect gate: PASS and CODE upload-blocked; do not re-run solely for confirmation if last_gates_confirmed is recent and media PRESENT")
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
    print("remaining_open_boxes:", remaining_open_boxes(PACKET))
    print("upload_blocker:", "three GitHub Actions secrets only (YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN); issue #1; do not poll")
    print("required_oauth_scopes:", "youtube.upload, youtube.force-ssl, yt-analytics.readonly (or full youtube + yt-analytics.readonly); youtube.upload alone is insufficient for captions")
    print("privacy_constraint:", "initial upload privacy stays private; do not change privacy until a confirmed private video id exists and is reviewed (see after-dispatch section; do not re-dispatch execute until id visible)")
    print("observation_window_formula:", "due_at = uploaded_at + 7 calendar days + 3 days Analytics lag (= +10 days total); early collect_feedback returns OBSERVATION_WINDOW_NOT_DUE; do not invent dates")
    print("observation_window_tool:", f"python3 tools/observation_window.py {packet_rel}  # computes DUE/WAITING from upload_state.json uploaded_at +10d if present; no invent; reusable for future packets")
    print("post_upload_confirmation_signals:", f"private provider video id must appear in GitHub Actions log AND in packet upload_state.json ({packet_rel}/upload_state.json); privacy stays private; do not re-dispatch execute until both visible; do not invent an id")
    # Live upload_state.json presence and video id (reduces rediscovery of whether a private id has appeared)
    def upload_state_status(packet: Path) -> str:
        state_path = packet / "upload_state.json"
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
    print("upload_state_status:", upload_state_status(PACKET))
    # Checklist banner status (reduces rediscovery of frozen timestamp rule)
    print("checklist_banner_status:", "frozen at Run 473 (2026-10-11T13:22:00Z); STALL_BANNER_REFRESH; do not refresh solely for timestamp; see docs/human_oauth_checklist.md")
    print("status_report_maintainability:", "primary status one-liners are sequential prints in main(); insert new ones carefully near related lines to avoid Run 519-style PLACEHOLDER overwrite; prefer small appends; selftest and record_run keep logs compact")
    # Run 527: future one-liners can be added as a trailing list to reduce insert risk; see below
    STATIC_ONE_LINERS = [
        ("run_log_note", "Permanent timestamped history lives in STATE.md / NEXT.md / RUNS.md / PROGRESS.md / FAILURES.md; each run prepends via tools/record_run.py; if a pattern repeats across many runs with no progress (e.g. oauth_idle), treat as increasingly suspicious and prefer new reusable capability over restatement"),
        ("run_history_summary_tool", "python3 tools/run_history_summary.py [N]  # prints concise last-N runs summary (default 3) from RUNS.md; reduces rediscovery of recent objectives/results/stall; no invent; reusable"),
        ("post_upload_confirm_tool", f"python3 tools/post_upload_confirm.py {packet_rel}  # CONFIRMED/INCOMPLETE/not_uploaded from upload_state.json (provider_video_id + privacy + uploaded_at); no invent; reusable after first private execute"),
        ("reusable_commands_index_tool", "python3 tools/reusable_commands_index.py  # clean index of key anti-rediscovery commands (status_report, run_history_summary, observation_window, post_upload_confirm, materialize, media_qa, next_action, record_run, operator_card, oauth_exchange, etc.); reduces rediscovery of the growing one-liner surface; no invent"),
        ("stall_pattern_detector_tool", "python3 tools/stall_pattern_detector.py  # flags recurring published_zero / oauth_idle streaks in recent RUNS.md as LOW/MEDIUM/HIGH suspicion; prefer new reusable capability if HIGH; no invent"),
        ("media_fingerprint_tool", "python3 tools/media_fingerprint.py  # quick PRESENT/MISSING + VO/cards/master SHA match for Q1 (no full QA, no materialize); confirms local media without rediscovery; no invent"),
        ("tool_integrity_check_tool", "python3 tools/tool_integrity_check.py  # checks key tools for truncation/PLACEHOLDER risk (min line counts + syntax); useful after remote file updates; no invent"),
        ("efficiency_summary_tool", "python3 tools/efficiency_summary.py  # concise recent reusable/labor-reduction gains from PROGRESS.md (no invent); shows compounding progress without opening the full file"),
        ("capability_gap_hint_tool", "python3 tools/capability_gap_hint.py  # hints at one high-value unblocked PLAN_BUILT/READY_FOR/NOT_BUILT gap from production_capabilities.md; prefer small reusable improvement when stall suspicion HIGH; no invent"),
        ("packet_stage_summary_tool", f"python3 tools/packet_stage_summary.py {packet_rel}  # concise TEXT_COMPLETE / MEDIA_MISSING / UPLOAD_BLOCKED stage for Q1 (default) without gates or materialize; reduces rediscovery of packet readiness; no invent"),
        ("human_next_action_tool", "python3 tools/human_next_action.py  # concise human-only OAuth secret setup steps and dispatch (no invent, no poll); reduces rediscovery of the exact next human action while STALL_OAUTH_IDLE continues"),
        ("next_suggestion_tool", "python3 tools/next_suggestion.py  # single concise next-action suggestion (human_step if stall HIGH else gap hint); reduces rediscovery of agent choice logic; no invent"),
        ("after_upload_steps_tool", f"python3 tools/after_upload_steps.py {packet_rel}  # precise post-upload sequence (confirm -> window -> collect_feedback dispatch -> experiment_loop -> complete); reduces rediscovery after first private video id; no invent"),

        ("publish_readiness_tool", f"python3 tools/publish_readiness.py {packet_rel}  # quick local READY_FOR_HUMAN_DISPATCH check (media fingerprint + next_action upload-blocked + open boxes); no full QA/materialize/poll; reduces rediscovery of packet readiness before secrets+dispatch"),
        ("recurring_pattern_flag_tool", "python3 tools/recurring_pattern_flag.py  # flags HIGHLY_SUSPICIOUS_STALL on long consecutive zero-publish OAuth streaks; reduces rediscovery of stall saturation; no invent"),
        ("stall_escalation_tool", "python3 tools/stall_escalation.py  # clear HIGHLY_SUSPICIOUS_STALL summary with exact human commands when streak high; reduces rediscovery of the only advancing action; no invent/poll"),
        ("saturation_guard_tool", "python3 tools/saturation_guard.py  # flags SATURATED_ANTI_REDISCOVERY when recent runs only added status one-liners while videos published stay 0; prefer human step or true capability over more status tools; no invent"),
    ]
    for key, val in STATIC_ONE_LINERS:
        print(f"{key}:", val)
    print("exact_record_run_usage:", "python3 tools/record_run.py --note /tmp/run_note.json  # JSON required keys: updated,state,next,runs,progress,failures (all non-empty strings); prepends timestamped notes to STATE.md NEXT.md RUNS.md PROGRESS.md FAILURES.md then runs compact_all.py; do not include secret values; see tools/record_run.py for format")
    # Captions review readiness (reduces rediscovery of whether the remaining open box is actionable)
    vo_ready = (PACKET / "vo").is_dir() and any((PACKET / "vo").glob("*.wav"))
    print("captions_review_ready:", "yes (VO present; spot-check 5 checkpoints in captions_review.md against audio)" if vo_ready else "no (materialize first; VO not accessible)")
    # Captions review checkpoint summary (reduces rediscovery of the exact 5 spots and method)
    print("captions_review_checkpoints:", "silence-proportional (not ASR); 5 spots: cue1 00:00:00.140, cue27 00:01:14.067, cue52 00:02:29.035, cue77 00:03:47.572, cue103 00:05:04.467 (see captions_review.md; agent may record approval when VO accessible)")
    # Thumbnail review status (PNG is committed; reduces rediscovery of approval state)
    thumb_review = PACKET / "thumbnail_review.md"
    if thumb_review.is_file():
        ttext = thumb_review.read_text(encoding="utf-8")
        approval = "unknown"
        for tline in ttext.splitlines():
            if tline.startswith("- approval:"):
                approval = tline.split(":", 1)[1].strip()
                break
        print("thumbnail_review_status:", f"{approval} (PNG committed at thumbnail.png; agent may approve when readability/contrast/text checks pass; see thumbnail_review.md)")
    else:
        print("thumbnail_review_status:", "thumbnail_review.md missing")
    # Captions review status (reduces rediscovery of approval state; VO accessibility already surfaced separately)
    cap_review = PACKET / "captions_review.md"
    if cap_review.is_file():
        ctext = cap_review.read_text(encoding="utf-8")
        approval = "unknown"
        for cline in ctext.splitlines():
            if cline.startswith("- approval:") or cline.startswith("Status:"):
                if "approval:" in cline:
                    approval = cline.split(":", 1)[1].strip()
                    break
                elif cline.startswith("Status:"):
                    approval = cline.split(":", 1)[1].strip()
        print("captions_review_status:", f"{approval} (see captions_review.md; agent records when VO accessible)")
    else:
        print("captions_review_status:", "captions_review.md missing")

    # Extract next_action code for immediate visibility (reduces parsing the full section)
    na_out = run_tool("next_action.py", [str(PACKET.relative_to(ROOT))])
    code = "unknown"
    for line in na_out.splitlines():
        if "ready_for_vo" in line or PACKET.name in line:
            parts = line.split()
            if len(parts) >= 3:
                code = parts[2]
                break
    print("next_action_code:", code)
    # Optional playlist does not block upload (reduces rediscovery of BLOCKED.md / channel.md)
    channel = (ROOT / "docs" / "channel.md").read_text(encoding="utf-8")
    playlist = "unknown"
    for line in channel.splitlines():
        if line.startswith("playlist_id:"):
            playlist = line.split(":", 1)[1].strip()
            break
    print(f"optional_playlist: {playlist} (does not block upload; create in Studio later if desired)")
    print("last_gates_confirmed: 2026-10-12 Run 497 (after materialize in fresh clone: media_qa PASS, master SHA MATCH, next_action=upload-blocked, closed_brief_gate PASS, selftest PASS). Do not re-run solely for confirmation unless packet or tools change.")
    print()
    print("--- stall_watch ---")
    print(stall_out.strip())
    print()
    print(f"--- next_action ({PACKET.name}) ---")
    print(run_tool("next_action.py", [str(PACKET.relative_to(ROOT))]).strip())
    print()
    print("--- human step ---")
    print("Follow docs/human_oauth_checklist.md or python3 tools/operator_card.py")
    print("Then set the three secrets (YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN) and dispatch execute=true once:")
    print("  Required scopes for the refresh token (youtube.upload alone is insufficient for captions):")
    print("    https://www.googleapis.com/auth/youtube.upload")
    print("    https://www.googleapis.com/auth/youtube.force-ssl")
    print("    https://www.googleapis.com/auth/yt-analytics.readonly")
    print("    (or full https://www.googleapis.com/auth/youtube plus yt-analytics.readonly)")
    print("  gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation")
    print("  gh secret set YOUTUBE_CLIENT_SECRET --repo takenthatusernameis-collab/Content-Automation")
    print("  gh secret set YOUTUBE_REFRESH_TOKEN --repo takenthatusernameis-collab/Content-Automation")
    print("  Do not run `gh secret list` from an agent (human UI check only under Settings > Secrets).")
    print("  Optional human-terminal confirmation (never from an agent): python3 tools/human_secret_confirm.py  # prints PRESENT/MISSING, never values; exit 0 = all three exist")
    print("  gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false")
    print("After the private video id appears, wait at least 7 days then use after_upload_steps.py for the feedback path.")
    print("Do not poll secrets. Do not rematerialize if media present. Logs via record_run.py. Do not scaffold Q2. Prefer quality improvements or true capability over more status printers or suggest-contract locks. Do not refresh the checklist banner solely for the timestamp.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
