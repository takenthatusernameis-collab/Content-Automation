#!/usr/bin/env python3
"""Print a clean index of key reusable anti-rediscovery commands.

Reduces rediscovery of the growing list of one-liners and tools that prevent
agents from opening multiple files or guessing commands. Does not poll secrets,
dispatch, or modify files. Prefer this when you need the exact invocation
without parsing the full status_report output.
"""

from __future__ import annotations

COMMANDS = [
    ("stall_summary", "python3 tools/stall_summary.py", "Concise one-command STALL_OAUTH_IDLE status: published=0, HIGH suspicion, exact human OAuth commands, unblocked pointers. Preferred entry during long stall."),
    ("unblocked_next", "python3 tools/unblocked_next.py", "Concrete unblocked next actions while stalled (experiment prep, caption quality, metadata polish, etc.). Prefer over new printers."),
    ("niche_consistency_scan", "python3 tools/niche_consistency_scan.py", "Soft combined niche-alignment scan of topic queue + all non-template video packets. Reduces sequential separate checks as packet count grows. No invent."),
    ("niche_metric_bridge", "python3 tools/niche_metric_bridge.py [PACKET]", "Soft bridge from channel promise (install default same day) to measurable signals (comment mentions + proxies). Complements generic Analytics for this niche. No invent."),
    ("same_day_install_observability", "python3 tools/same_day_install_observability.py [PACKET]", "Soft suggestor for making the channel promise more observable in comments via reportable cues and phrasing. Grounded in niche. No invent or scaffold."),
    ("feedback_to_topic_suggest", "python3 tools/feedback_to_topic_suggest.py [PACKET]", "Soft guidance for feeding observed operational feedback or weak points back into topic queue candidates. Grounded in niche promise. No invent or scaffold."),
    ("post_publish_prep_summary", "python3 tools/post_publish_prep_summary.py [PACKET]", "One-command aggregator of experiment_prep + feedback_review_starter + fixed post-collect sequence. Use after first private id or for readiness."),
    ("packet_prep_summary", "python3 tools/packet_prep_summary.py [PACKET]", "One-command soft pre-upload checks: sources coverage, uncovered claims research directions, mechanism language in metadata. Reduces sequential rediscovery. No invent."),
    ("feedback_ingestion_readiness", "python3 tools/feedback_ingestion_readiness.py", "Structural readiness check for the post-publish feedback ingestion path (adapter, window helpers, review/suggest tools present). Fail-closed sequence printer. No invent."),
    ("experiment_loop_readiness", "python3 tools/experiment_loop_readiness.py", "Structural readiness check for the post-publish experiment/learning loop (key templates, starters, validators present). Fail-closed sequence printer. No invent."),
    ("first_experiment_suggest", "python3 tools/first_experiment_suggest.py [PACKET]", "Soft grounded first-experiment hypothesis suggestion from idea.md mechanism (prefers hook). Points to baseline starter. No invented metrics. Reduces post-publish planning labor."),
    ("metric_focus_suggest", "python3 tools/metric_focus_suggest.py [PACKET]", "Soft suggestion of primary metric and guardrails grounded from idea.md mechanism. Reduces labor of choosing what to measure for the first experiment. No invented numbers."),
    ("experiment_full_prep", "python3 tools/experiment_full_prep.py [PACKET]", "Packet-specific: grounded hypothesis + ready-to-adapt baseline/decision JSON examples with hypothesis filled. Combines suggest + examples. No invented numbers. Reduces sequential prep labor."),
    ("baseline_source_example", "python3 tools/baseline_source_example.py", "Example documented source phrasing that passes experiment_loop source check. Reduces labor of writing a valid non-rejected source field. No invented numbers."),
    ("decision_source_example", "python3 tools/decision_source_example.py", "Example documented source phrasing for experiment_decision.json that passes rejected-words check. Reduces labor of writing a valid source after comparison. No invented decisions."),
    ("experiment_json_examples", "python3 tools/experiment_json_examples.py", "Complete ready-to-adapt example JSON for both experiment_baseline.json and experiment_decision.json with valid sources. Reduces sequential lookup. No invented numbers or decisions."),
    ("topic_queue_mechanism_check", "python3 tools/topic_queue_mechanism_check.py", "Soft niche-alignment check on topic_queue.md one_line/problem vs channel operational keywords. Reduces recurring queue-review labor before scaffolding future packets. No invent."),
    ("packet_niche_check", "python3 tools/packet_niche_check.py [PACKET]", "Soft niche-alignment check on a packet's idea.md mechanism/problem/topic vs channel operational keywords. Reduces recurring packet-review labor after scaffold. No invent."),
    ("upload_path_readiness", "python3 tools/upload_path_readiness.py", "Structural readiness check for the pre-upload / YouTube upload path. Fail-closed human+dispatch sequence. No invent."),
    ("sources_validator", "python3 tools/sources_validator.py [PACKET]", "Claim-to-source coverage report: detects digits/hedges in script and checks non-placeholder sources in sources.md/research.md. Soft signal; reduces manual cross-check. No invent."),
    ("uncovered_claims_suggest", "python3 tools/uncovered_claims_suggest.py [PACKET]", "Soft research direction suggestions for uncovered claims (digits/hedges). Reuses coverage logic; no invented sources or searches. Reduces research planning labor."),
    ("metadata_mechanism_align_suggest", "python3 tools/metadata_mechanism_align_suggest.py [PACKET]", "Soft check that title/description/thumbnail surface key words from the packet mechanism (from idea.md). Reduces manual consistency verification. No invent."),
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
    ("quality_scan", "python3 tools/quality_scan.py [PACKET]", "Reports high-precision anti-slop phrases in script.md WORDS; revision signal only; --strict fails on hits; set_status refuses ready_for_vo while hits remain"),
    ("claim_scan", "python3 tools/claim_scan.py [PACKET]", "Reports unsourced digit tokens and survey hedges in script WORDS; revision signal only; --strict fails on hits; set_status refuses ready_for_vo while hits remain"),
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
