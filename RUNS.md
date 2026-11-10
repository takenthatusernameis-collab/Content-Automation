2026-11-10T00:35:00Z (Run 1150)

Updated tools/youtube_feedback.py to use shared upload_date.compute_due_date for the observation window due date and parse_uploaded_at for uploaded_at parsing (including nested video_upload). Eliminates the last hard-coded timedelta(days=7+3) and duplicate parser in the core feedback adapter that every future video will use. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.

# RUNS

## Run 1150 — 2026-11-10T00:35:00Z
- Objective: Eliminate the remaining hard-coded due-date arithmetic and duplicate parser in the core feedback collector so the +10 day observation window stays consistent after the first private video id.
- Action: Updated tools/youtube_feedback.py to import and use compute_due_date and parse_uploaded_at from tools/upload_date.py. upload_timestamp now prefers the shared parser (handles nested video_upload). window_status now calls compute_due_date. Removed unused _parse_ts. Recorded the change in state files. No secrets polled, no dispatch, no live packet writes.
- Result: Single source of truth now covers the feedback adapter that will run for every future video. Reduces future rediscovery or silent divergence on the post-upload path. STALL_OAUTH_IDLE continues.
- Verification: Local inspection of the edited file confirms shared helper usage and removal of the old timedelta and _parse_ts. Soft only (full suite not re-run in this sandbox; prior suite was 90/90). File size and commit confirmed.
- Discovery: Extending the shared module to the last major post-upload tool compounds reliability for the feedback path that will run after the first private video id. Long stall remains HIGH suspicion after 1000+ runs. Prefer the human step or a true post-publish capability over further pure confirmation.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/contracts_suite.py && python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1149 — 2026-11-09T23:20:00Z
- Objective: Eliminate remaining hard-coded +10 day arithmetic so the observation window due date stays consistent across all post-upload tools after the first private video id.
- Action: Added OBSERVATION_WINDOW_DAYS and compute_due_date to tools/upload_date.py. Updated observation_window.py and post_publish_sequence.py to use the shared function. Updated observation_window_contract.py to import and lock the shared helper. Recorded the change in state files. No secrets polled, no dispatch, no live packet writes.
- Result: Single source of truth for both parsing and due-date calculation. Reduces future rediscovery or silent divergence on the post-upload path that every video will use. STALL_OAUTH_IDLE continues.
- Verification: Local inspection confirms shared function usage; contract now exercises compute_due_date. Soft only (full suite not re-run in this sandbox; prior suite was 90/90).
- Discovery: Centralizing the window constant compounds reliability for the feedback path that will run after the first private video id. Long stall remains HIGH suspicion after 1000+ runs. Prefer the human step or a true post-publish capability over further pure confirmation.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/contracts_suite.py && python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1148 — 2026-11-09T22:30:00Z
- Objective: Eliminate duplicated date-parsing logic so the +10 day observation window stays consistent across all post-upload tools after the first private video id.
- Action: Refactored tools/post_publish_sequence.py and tools/post_upload_confirm.py to import parse_uploaded_at from the shared tools/upload_date.py (already used by observation_window.py). Verified with sample upload_state.json and full contracts_suite.py. Recorded the change in state files. No secrets polled, no dispatch, no live packet writes.
- Result: Single source of truth for uploaded_at parsing. Reduces future rediscovery or silent divergence on the post-upload path that every video will use. Suite stays 90/90 PASS. STALL_OAUTH_IDLE continues.
- Verification: Local execution of the three tools on sample data (Z and space-separated variants) produces matching due dates. contracts_suite.py exits 0. Soft only.
- Discovery: Shared module usage compounds reliability for the feedback path that will run after the first private video id. Long stall remains HIGH suspicion after 1000+ runs. Prefer the human step or a true post-publish capability over further pure confirmation.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/contracts_suite.py && python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1147 — 2026-11-09T20:20:00Z
- Objective: Lock the hardened uploaded_at parser against common date variants so the +10 day observation window remains reliable after the first private video id.
- Action: Expanded tools/observation_window_contract.py with test_parse_variants (Z, offset, space, date-only) and broader garbage rejection. Re-ran contracts_suite.py. Recorded the change in state files. No secrets polled, no dispatch, no live packet writes.
- Result: Contract now covers more of the parser surface introduced in Run 1146. Suite stays 90/90 PASS. Reduces future rediscovery or silent parse failure on the post-upload path. STALL_OAUTH_IDLE continues.
- Verification: Local execution of the updated contract and full contracts_suite.py both exit 0. Soft only.
- Discovery: Contract tests that mirror recent hardening compound reliability for the feedback path that will run after the first private video id. Long stall remains HIGH suspicion after 1000+ runs. Prefer the human step or a true post-publish capability over further pure confirmation.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/contracts_suite.py && python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)

Permanent log. Newest first.
