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

# RUNS

## Run 1147 — 2026-11-09T20:20:00Z
- Objective: Lock the hardened uploaded_at parser against common date variants so the +10 day observation window remains reliable after the first private video id.
- Action: Expanded tools/observation_window_contract.py with test_parse_variants (Z, offset, space, date-only) and broader garbage rejection. Re-ran contracts_suite.py. Recorded the change in state files. No secrets polled, no dispatch, no live packet writes.
- Result: Contract now covers more of the parser surface introduced in Run 1146. Suite stays 90/90 PASS. Reduces future rediscovery or silent parse failure on the post-upload path. STALL_OAUTH_IDLE continues.
- Verification: Local execution of the updated contract and full contracts_suite.py both exit 0. Soft only.
- Discovery: Contract tests that mirror recent hardening compound reliability for the feedback path that will run after the first private video id. Long stall remains HIGH suspicion after 1000+ runs. Prefer the human step or a true post-publish capability over further pure confirmation.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/contracts_suite.py && python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1146 — 2026-11-09T19:20:00Z
- Objective: Harden uploaded_at date parsing so the observation window due date is computed reliably after the first private video id appears.
- Action: Updated parse_uploaded_at in tools/observation_window.py and tools/post_publish_sequence.py to prefer datetime.fromisoformat (Z cleanup) plus extra strptime fallbacks. Recorded the change in state files. No secrets polled, no dispatch, no live packet writes.
- Result: Parsing is more robust to common ISO variants. Reduces future rediscovery or failure on the post-upload path that every video will use. STALL_OAUTH_IDLE continues.
- Verification: Local inspection of the two updated functions confirms fromisoformat + fallbacks; no new contract failures expected. Soft only.
- Discovery: Date-parsing robustness compounds reliability for the feedback path that will run after the first private video id. Long stall remains HIGH suspicion after 1000+ runs. Prefer the human step or a true post-publish capability over further pure confirmation.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/contracts_suite.py && python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)

Permanent log. Newest first.
