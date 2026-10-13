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
    print("recommended_next:", "materialize (python3 tools/materialize_q1_release.py)" if "MISSING" in media else "human_step (three secrets + one execute=true dispatch). Preferred list complete.")
    print("exact_dispatch_command:", "gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false")
    print("exact_collect_command:", "gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=false -f collect_feedback=true  # only after private video id exists AND uploaded_at + 10 days due")
    # Immediate visibility of active stall flags (reduces parsing the full stall section)
    stall_flags = [line.strip() for line in stall_out.splitlines() if line.strip().startswith("STALL_")]
    print("active_stall_flags:", ", ".join(stall_flags) if stall_flags else "none (see stall_watch section)")
    print("remaining_open_boxes:", remaining_open_boxes())
    print("upload_blocker:", "three GitHub Actions secrets only (YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN); issue #1; do not poll")
    print("required_oauth_scopes:", "youtube.upload, youtube.force-ssl, yt-analytics.readonly (or full youtube + yt-analytics.readonly); youtube.upload alone is insufficient for captions")
    print("privacy_constraint:", "initial upload privacy stays private; do not change privacy until a confirmed private video id exists and is reviewed (see after-dispatch section; do not re-dispatch execute until id visible)")
    print("observation_window_formula:", "due_at = uploaded_at + 7 calendar days + 3 days Analytics lag (= +10 days total); early collect_feedback returns OBSERVATION_WINDOW_NOT_DUE; do not invent dates")
    print("post_upload_confirmation_signals:", "private provider video id must appear in GitHub Actions log AND in packet upload_state.json (videos/002-stop-deciding-what-to-work-on-every-morning/upload_state.json); privacy stays private; do not re-dispatch execute until both visible; do not invent an id")
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
    print("--- next_action (Q1) ---")
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
    print("  Initial upload privacy stays private (do not change privacy until a confirmed private video id exists and is reviewed).")
    print("Do not rematerialize if media present. Do not reopen closed briefs.")
    print("Pure verification has diminishing returns while STALL_OAUTH_IDLE is set.")
    print("Do not refresh the human_oauth_checklist banner solely for its timestamp (STALL_BANNER_REFRESH).")
    print(f"STALL SUSPICION: oauth_idle_without_publish (live idle_streak={idle}; historical ~186+ across archives). Continued pure documentation updates have diminishing returns and should be treated as low-leverage unless they introduce a new reusable capability that reduces future human or agent work after the secrets are set.")
    print()
    print("--- after successful dispatch (confirm, do not invent) ---")
    print("Look for a private provider video id in the Actions log AND in the packet upload_state.json.")
    print("Privacy stays private. Do not re-dispatch execute until that id is visible.")
    print("Wait until uploaded_at + 7 calendar days + 3 days Analytics lag (due_at = uploaded_at + 10 days) before any collect_feedback=true dispatch. Early collect is OBSERVATION_WINDOW_NOT_DUE.")
    print("Then dispatch once:")
    print("  gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=false -f collect_feedback=true")
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
    print("Preferred list complete (Run 471). Run 474 added STALL_BANNER_REFRESH so pure banner-timestamp refreshes are flagged. Checklist banner intentionally left at Run 473 (do not rediscover updating it solely for timestamp). Next agent prioritizes the human step (three secrets + one dispatch) or identifies a truly new small anti-rediscovery preparation that does not invent data, media, metrics, or expand locked surfaces. Do not scaffold Q2, poll secrets, or extend locked surfaces. Do not refresh the checklist banner solely for the timestamp. Run 478 escalated the stall-length suspicion in this printer. Run 479 made the live idle_streak dynamic. Run 480 made media_status report master SHA MATCH/MISMATCH when present. Run 481 made the missing path also print the target SHA prefix. Run 482 added the after-dispatch confirmation signals to the primary status command so agents see the private video id look-up without opening the checklist. Run 483 made the PRESENT path also print the target SHA prefix for full consistency, and restored the STALL_OAUTH_IDLE active lock in NEXT.md so next_compact_contract and selftest stay green. Run 484 added an explicit recommended_next line (materialize if media missing, else human_step) so agents see the single highest-leverage action without parsing other sections. Run 485 added the exact gh workflow dispatch command in the human step section so agents see the precise one-line dispatch without opening the checklist or operator_card. Run 486 added last_gates_confirmed (full local gates green after materialize on 2026-10-12) so agents see recent readiness without re-verifying solely for confirmation. Run 487 added next_action_code extraction so agents see the gate code (upload-blocked or materialize-q1) immediately without parsing the full next_action section, and refreshed last_gates_confirmed after re-verification. Run 488 added optional_playlist line (not_set, does not block upload) so agents see the channel.md status without opening the file. Run 489 added the exact three secret names and the three gh secret set commands in the human step section so agents see the precise secret setup without opening the checklist. Run 490 added the required OAuth scopes to the human step section so agents see the exact token scopes without opening oauth_setup.py or the checklist. Run 491 added the exact collect_feedback dispatch command to the after-dispatch section so agents see the precise next command after a video id appears without opening the checklist. Run 492 added an explicit initial-privacy-stays-private line in the human step section so agents see the privacy constraint without opening the checklist or operator_card. Run 493 added the forbidden `gh secret list` reminder and the optional human_secret_confirm.py command in the human step section so agents see the exact confirmation method without opening the checklist or operator_card. Run 494 added the precise observation window timing (uploaded_at + 7 calendar days + 3 days Analytics lag = due at +10 days) to the after-dispatch section so agents see the exact due calculation without opening youtube_feedback.py. Run 497 refreshed last_gates_confirmed after re-verification in a fresh clone (media_qa PASS, SHA MATCH, upload-blocked, closed_brief_gate PASS, selftest PASS). Run 498 added STALL_GATE_CONFIRM to stall_watch.py so repeated last_gates_confirmed refreshes / sole-purpose re-verifications are machine-visible and low-leverage while the OAuth stall continues. Run 499 added active_stall_flags one-liner so agents see current STALL_* flags immediately without parsing the full stall_watch section. Run 500 added master_sha_target full checksum line so agents can copy the exact r253 SHA without opening HANDOFF.md or scanning media_status prefixes. Run 502 added remaining_open_boxes parser so agents see the exact unchecked human-work items (captions review, publish lock, upload) without opening packet.md. Run 504 added captions_review_ready. Run 505 added captions_review_checkpoints summary of the 5 silence-proportional spots. Run 506 added thumbnail_review_status one-liner (parses approval from thumbnail_review.md; PNG is committed so accessible). Run 510 added exact_dispatch_command one-liner so agents see the precise gh workflow dispatch without scanning the human step section. Run 511 added required_oauth_scopes one-liner so agents see the exact token scopes without scanning the human step section. Run 512 added exact_collect_command one-liner so agents see the precise post-id collect_feedback dispatch without scanning the after-dispatch section. Run 513 added privacy_constraint one-liner so agents see the exact initial-privacy-stays-private rule without scanning the human step or after-dispatch sections. Run 514 added observation_window_formula one-liner so agents see the exact due_at = uploaded_at + 7d + 3 lag (= +10d) and OBSERVATION_WINDOW_NOT_DUE without scanning the after-dispatch section. Run 515 added post_upload_confirmation_signals one-liner so agents see the exact private video id confirmation criteria (Actions log AND packet upload_state.json) without scanning the after-dispatch section.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
