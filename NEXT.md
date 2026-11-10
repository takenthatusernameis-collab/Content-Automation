2026-11-10T04:20:00Z (Run 1152)

Added tools/experiment_decision_starter.py: prints a fail-closed experiment_decision.json skeleton that leaves the decision as TEMPLATE and requires a documented review after a numeric comparison. Complements the existing baseline starter. Advances post-publish readiness for every future video without credentials or invented results. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.
2026-11-10T01:26:00Z (Run 1151)

Centralized the 7-calendar-day query length and 3-day Analytics lag into tools/upload_date.py (CALENDAR_DAYS + DATA_LAG_DAYS = OBSERVATION_WINDOW_DAYS). youtube_feedback.py now imports the shared constants instead of maintaining local duplicates. Completes the single source of truth for the entire observation window formula used by every future video. Contracts suite remains UNIFIED RESULT: PASS (90/90). STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.

(Older next actions live in `docs/next_archive.md`. Do not paste the archive back.)

2026-11-09T15:35:00Z (Run 1142)
Standardized remaining observation-window language in live tools and docs to precise +10 days. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload complete and stable. Next remains human OAuth step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). Do not poll. Do not rematerialize if present. Do not scaffold Q2.
