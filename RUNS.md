2026-11-09T22:30:00Z (Run 1148)

Removed duplicated parse_uploaded_at implementations from tools/post_publish_sequence.py and tools/post_upload_confirm.py; both now import the shared robust parser from tools/upload_date.py. Eliminates drift risk between the three post-upload tools that compute the exact +10 day observation window. Contracts suite remains UNIFIED RESULT: PASS (90/90). STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.

# RUNS

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
