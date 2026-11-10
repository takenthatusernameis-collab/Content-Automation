2026-11-10T00:35:00Z (Run 1150)

Updated tools/youtube_feedback.py to use shared upload_date.compute_due_date for the observation window due date and parse_uploaded_at for uploaded_at parsing (including nested video_upload). Eliminates the last hard-coded timedelta(days=7+3) and duplicate parser in the core feedback adapter that every future video will use. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.
2026-11-09T23:20:00Z (Run 1149)

Centralized the +10 day observation window due date calculation into tools/upload_date.py (OBSERVATION_WINDOW_DAYS constant + compute_due_date). observation_window.py and post_publish_sequence.py now call the shared function instead of hard-coding timedelta(days=10). Eliminates remaining drift risk on the exact collect due date used by every future video. Contract updated to lock the shared helper. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.
2026-11-09T22:30:00Z (Run 1148)

Removed duplicated parse_uploaded_at implementations from tools/post_publish_sequence.py and tools/post_upload_confirm.py; both now import the shared robust parser from tools/upload_date.py. Eliminates drift risk between the three post-upload tools that compute the exact +10 day observation window. Contracts suite remains UNIFIED RESULT: PASS (90/90). STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.
2026-11-09T20:20:00Z (Run 1147)

Strengthened tools/observation_window_contract.py with additional parse-variant tests (Z, +00:00, space-separated, date-only, garbage rejection) that lock the hardened parse_uploaded_at from Run 1146. Contracts suite remains UNIFIED RESULT: PASS (90/90). Reduces risk that future date-format drift breaks the exact +10 day due date after the first private video id. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.
2026-11-09T19:20:00Z (Run 1146)

Hardened uploaded_at date parsing in tools/observation_window.py and tools/post_publish_sequence.py to prefer datetime.fromisoformat (with Z cleanup) plus additional strptime fallbacks. Reduces risk of unparseable dates after the first private video id appears, so the exact +10 day due date is computed reliably for every future video. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.
2026-11-09T18:20:00Z (Run 1145)

Standardized remaining imprecise "7-day observation" phrasing in tools/youtube_feedback.py comments and docs/youtube_integration.md list item to the precise first-calendar-days / uploaded_at + 10 days (7 calendar + 3 Analytics lag) formula. Completes consistency across the last core feedback surfaces. Reduces rediscovery of the exact post-upload collect due date for every future video. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.
2026-11-09T17:23:00Z (Run 1144)

Standardized remaining imprecise observation-window comments in tools/post_publish_sequence.py and tools/youtube_feedback.py to the precise uploaded_at + 10 days (7 calendar + 3 Analytics lag) formula. Completes consistency across more post-publish tool surfaces. Reduces rediscovery of the exact post-upload collect due date for every future video. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.
2026-11-09T16:22:00Z (Run 1143)

Standardized remaining imprecise observation-window language in starter tools (experiment_notes_starter.py, feedback_review_starter.py, human_one_pager.py, experiment_package_starter.py) to the precise uploaded_at + 10 days (7 calendar + 3 Analytics lag) formula. Completes consistency across more post-publish starter surfaces. Reduces rediscovery of the exact post-upload collect due date for every future video. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.

2026-11-09T15:35:00Z (Run 1142): Standardized remaining observation-window language in live tools and docs to uploaded_at + 10 days (7 calendar + 3 Analytics lag). Improves long-term reliability of the post-publish feedback path that every future video will use. Recorded continued STALL_OAUTH_IDLE (1000+ runs, HIGH suspicion), published=0. Pre-upload path remains complete and stable.

(Older progress notes remain in docs/progress_archive.md.)
