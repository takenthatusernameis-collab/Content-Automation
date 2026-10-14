#!/usr/bin/env python3
"""Print a clean index of key reusable anti-rediscovery commands.

Reduces rediscovery of the growing list of one-liners and tools that prevent
agents from opening multiple files or guessing commands. Does not poll secrets,
dispatch, or modify files. Prefer this when you need the exact invocation
without parsing the full status_report output.
"""

from __future__ import annotations

COMMANDS = [
    ("status_report", "python3 tools/status_report.py", "Primary current-system status (stall, media, next, all one-liners)"),
    ("run_history_summary", "python3 tools/run_history_summary.py [N]", "Concise last-N runs from RUNS.md (default 3)"),
    ("observation_window", "python3 tools/observation_window.py videos/002-stop-deciding-what-to-work-on-every-morning", "DUE/WAITING for +10d post-upload window from upload_state.json"),
    ("post_upload_confirm", "python3 tools/post_upload_confirm.py videos/002-stop-deciding-what-to-work-on-every-morning", "CONFIRMED/INCOMPLETE/not_uploaded from upload_state.json"),
    ("materialize", "python3 tools/materialize_q1_release.py", "Install r249 VO+cards + r253 master (ignore truncated r249 master); only if media MISSING"),
    ("media_qa", "python3 tools/media_qa.py videos/002-stop-deciding-what-to-work-on-every-morning", "Fail-closed media QA (expect PASS when present)"),
    ("next_action", "python3 tools/next_action.py videos/002-stop-deciding-what-to-work-on-every-morning", "Read-only next step code (expect upload-blocked)"),
    ("record_run", "python3 tools/record_run.py --note /tmp/run_note.json", "Prepend timestamped notes to STATE/NEXT/RUNS/PROGRESS/FAILURES then compact"),
    ("operator_card", "python3 tools/operator_card.py", "Human step card for secrets + dispatch"),
    ("oauth_exchange", "python3 tools/oauth_exchange.py", "Human-only token minting (consent URL then --exchange)"),
    ("human_secret_confirm", "python3 tools/human_secret_confirm.py", "Human-only PRESENT/MISSING check for the three secrets (never values)"),
    ("stall_watch", "python3 tools/stall_watch.py", "Machine-visible stall flags and idle_streak"),
    ("stall_pattern_detector", "python3 tools/stall_pattern_detector.py", "Flags recurring published_zero / oauth_idle streaks in recent RUNS.md (LOW/MEDIUM/HIGH); prefer new capability if HIGH"),
    ("tool_integrity_check", "python3 tools/tool_integrity_check.py", "Checks key tools for truncation/PLACEHOLDER risk (min line counts + syntax); useful after file updates via remote tools"),
    ("media_fingerprint", "python3 tools/media_fingerprint.py", "Quick PRESENT/MISSING + VO/cards/master SHA match for Q1 packet (no full QA or materialize)"),
    ("efficiency_summary", "python3 tools/efficiency_summary.py", "Concise recent reusable/labor-reduction gains from PROGRESS.md (no invent); shows compounding progress"),
    ("capability_gap_hint", "python3 tools/capability_gap_hint.py", "Scans production_capabilities.md for PLAN_BUILT/READY_FOR gaps; suggests one unblocked reusable improvement when stall suspicion is HIGH"),
    ("packet_stage_summary", "python3 tools/packet_stage_summary.py [PACKET]", "Concise local stage for packet (TEXT_COMPLETE_MEDIA_MISSING_UPLOAD_BLOCKED etc.); no gates/materialize/invent"),
    ("human_next_action", "python3 tools/human_next_action.py", "Concise human-only next action: OAuth secret setup steps + dispatch (no invent, no poll); reduces rediscovery of exact human path"),
    ("next_suggestion", "python3 tools/next_suggestion.py", "Single concise next-action suggestion (human_step if stall HIGH, else gap); reduces rediscovery of choice logic"),
    ("publish_readiness", "python3 tools/publish_readiness.py [PACKET]", "Quick local READY_FOR_HUMAN_DISPATCH (media PRESENT+MATCH + next_action=upload-blocked + open boxes); no full QA/materialize/poll"),
    ("recurring_pattern_flag", "python3 tools/recurring_pattern_flag.py", "Flags HIGHLY_SUSPICIOUS_STALL if consecutive zero-publish OAuth runs exceed threshold; reduces rediscovery of stall saturation"),
    ("after_upload_steps", "python3 tools/after_upload_steps.py [PACKET]", "Precise sequence of reusable commands and dispatches after first private provider_video_id exists (confirm, window, collect, experiment, complete); no invent"),
    ("stall_escalation", "python3 tools/stall_escalation.py", "Clear HIGHLY_SUSPICIOUS_STALL summary with exact human commands when zero-publish streak is high; reduces rediscovery of the only advancing action"),
    ("saturation_guard", "python3 tools/saturation_guard.py", "Flags SATURATED_ANTI_REDISCOVERY when recent runs only added status tools while videos=0; steers away from more one-liners"),
]

def main() -> int:
    print("REUSABLE COMMANDS INDEX (anti-rediscovery; do not invent)")
    print("Use these exact invocations. Full details in tools/status_report.py and HANDOFF.md.")
    print()
    for key, cmd, desc in COMMANDS:
        print(f"{key}:")
        print(f"  {cmd}")
        print(f"  # {desc}")
        print()
    print("After secrets are set and first private video id exists, use post_upload_confirm then observation_window then collect_feedback dispatch.")
    print("Do not rematerialize if media PRESENT. Do not re-verify gates solely for confirmation. Do not refresh checklist banner solely for timestamp.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
