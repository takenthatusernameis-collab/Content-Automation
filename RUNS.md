2026-11-10T01:26:00Z (Run 1151)

Centralized the 7-calendar-day query length and 3-day Analytics lag into tools/upload_date.py (CALENDAR_DAYS + DATA_LAG_DAYS = OBSERVATION_WINDOW_DAYS). youtube_feedback.py now imports the shared constants instead of maintaining local duplicates. Completes the single source of truth for the entire observation window formula used by every future video. Contracts suite remains UNIFIED RESULT: PASS (90/90). STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.

# RUNS

## Run 1151 — 2026-11-10T01:26:00Z
- Objective: Eliminate remaining local duplicates of the 7+3 observation window constants so the formula stays consistent in the core feedback adapter after the first private video id.
- Action: Added CALENDAR_DAYS=7 and DATA_LAG_DAYS=3 to tools/upload_date.py; OBSERVATION_WINDOW_DAYS now derived. Updated youtube_feedback.py to import and use them, removing local definitions. Verified contracts_suite.py. Recorded in state files. No secrets polled, no dispatch, no live packet writes.
- Result: Single source of truth now covers both the due-date arithmetic and the query length / lag components. Suite stays 90/90 PASS. Reduces future rediscovery or silent divergence on the post-upload path. STALL_OAUTH_IDLE continues.
- Verification: Local execution of contracts_suite.py exits 0 (90/90). Inspection confirms imports and derived constant. Soft only.
- Discovery: Completing the shared module for the full formula compounds reliability for the feedback path that will run after the first private video id. Long stall remains HIGH suspicion after 1000+ runs. Prefer the human step or a true post-publish capability over further pure confirmation.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/contracts_suite.py && python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1150 — 2026-11-10T00:35:00Z
- Objective: Eliminate the remaining hard-coded due-date arithmetic and duplicate parser in the core feedback collector so the +10 day observation window stays consistent after the first private video id.
- Action: Updated tools/youtube_feedback.py to import and use compute_due_date and parse_uploaded_at from tools/upload_date.py. upload_timestamp now prefers the shared parser (handles nested video_upload). window_status now calls compute_due_date. Removed unused _parse_ts. Recorded the change in state files. No secrets polled, no dispatch, no live packet writes.
- Result: Single source of truth now covers the feedback adapter that will run for every future video. Reduces future rediscovery or silent divergence on the post-upload path. STALL_OAUTH_IDLE continues.
- Verification: Local inspection of the edited file confirms shared helper usage and removal of the old timedelta and _parse_ts. Soft only (full suite not re-run in this sandbox; prior suite was 90/90). File size and commit confirmed.
- Discovery: Extending the shared module to the last major post-upload tool compounds reliability for the feedback path that will run after the first private video id. Long stall remains HIGH suspicion after 1000+ runs. Prefer the human step or a true post-publish capability over further pure confirmation.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/contracts_suite.py && python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)

Permanent log. Newest first.
