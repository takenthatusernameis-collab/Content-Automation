2026-11-10T05:20:00Z (Run 1153)

Enhanced tools/experiment_readiness.py to also report experiment_decision.json status (absent/template/recorded/incomplete) after a filled baseline. Expanded recommended_actions in experiment_decision_starter.py to include notes, package, and readiness commands for consistency with other starters. Advances post-publish readiness and reduces human rediscovery of next steps for every future video without credentials or invented results. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.
2026-11-10T04:20:00Z (Run 1152)

Added tools/experiment_decision_starter.py: prints a fail-closed experiment_decision.json skeleton that leaves the decision as TEMPLATE and requires a documented review after a numeric comparison. Complements the existing baseline starter. Advances post-publish readiness for every future video without credentials or invented results. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.
2026-11-10T01:26:00Z (Run 1151)

Centralized the 7-calendar-day query length and 3-day Analytics lag into tools/upload_date.py (CALENDAR_DAYS + DATA_LAG_DAYS = OBSERVATION_WINDOW_DAYS). youtube_feedback.py now imports the shared constants instead of maintaining local duplicates. Completes the single source of truth for the entire observation window formula used by every future video. Contracts suite remains UNIFIED RESULT: PASS (90/90). STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.
2026-11-10T00:35:00Z (Run 1150)

Updated tools/youtube_feedback.py to use shared upload_date.compute_due_date for the observation window due date and parse_uploaded_at for uploaded_at parsing (including nested video_upload). Eliminates the last hard-coded timedelta(days=7+3) and duplicate parser in the core feedback adapter that every future video will use. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.
2026-11-09T23:20:00Z (Run 1149)

Centralized the +10 day observation window due date calculation into tools/upload_date.py (OBSERVATION_WINDOW_DAYS constant + compute_due_date). observation_window.py and post_publish_sequence.py now call the shared function instead of hard-coding timedelta(days=10). Eliminates remaining drift risk on the exact collect due date used by every future video. Contract updated to lock the shared helper. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.

# STATE

2026-11-09T15:35:00Z (Run 1142)

Standardized remaining observation-window language in live tools and docs (next_after_publish.py, human_next_action.py, post_publish_sequence.py, README.md, ROADMAP.md) to the precise uploaded_at + 10 days (7 calendar + 3 Analytics lag) formula. Completes consistency across more human-facing and agent-facing surfaces. Reduces rediscovery of the exact post-upload collect due date for every future video. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.

(Older state notes remain below or in docs/state_archive.md. Do not paste the archive back.)
