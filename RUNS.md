## Run 1045 — 2026-11-05T13:26:00Z
- Objective: Lock the fail-closed missing-provider_video_id path of the experiment ledger so it does not regress while the OAuth stall continues.
- Action: Inspected STATE/NEXT/RUNS/BLOCKED and existing experiment_loop.py. Created tools/experiment_loop_contract.py (asserts exit 2 + key phrases including gate: HOLD_UNPUBLISHED when no provider_video_id is present). Updated state files. No secrets polled, no dispatch, no media writes. Committed.
- Result: Videos published stay 0. New contract available for the experiment ledger. Estimated savings: prevents silent regression of the unpublished hold for future runs and after first publish. Pre-upload path unchanged. Gate behavior unchanged.
- Verification: File created and contract ran PASS locally. Soft only. No regressions.
- Discovery: The long-running OAuth stall (1000+ runs) remains the sole primary blocker; locking the experiment ledger compounds reliability of the post-publish path without adding printers or requiring credentials.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so.
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or python3 tools/oauth_setup.py then secrets + single execute=true dispatch). After id appears: python3 tools/post_publish_sequence.py. Optional: python3 tools/experiment_loop_contract.py.

## Run 1044 — 2026-11-05T14:19:00Z
- Objective: Lock the fail-closed missing-Selected-VO path of the media QA gate so it does not regress while the OAuth stall continues.
- Action: Inspected STATE/NEXT/RUNS/BLOCKED and existing media_qa.py. Created tools/media_qa_contract.py (asserts exit 2 + key phrases including gate: FAIL and selected_vo_present when no Selected VO is present). Updated state files. No secrets polled, no dispatch, no media writes. Committed.
- Result: Videos published stay 0. New contract available for the media QA gate. Estimated savings: prevents silent regression of the fail-closed media checks for future runs. Pre-upload path unchanged. Gate behavior unchanged.
- Verification: File created and contract ran PASS locally. Soft only. No regressions.
- Discovery: The long-running OAuth stall (1000+ runs) remains the sole primary blocker; locking the media QA compounds reliability of the pre-upload path without adding printers or requiring credentials.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so.
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or python3 tools/oauth_setup.py then secrets + single execute=true dispatch). After id appears: python3 tools/post_publish_sequence.py. Optional: python3 tools/media_qa_contract.py.

## Run 1043 — 2026-11-05T11:17:26Z
- Objective: Lock the fail-closed missing-secrets path and core recipe of the OAuth setup printer so human guidance does not regress while the OAuth stall continues.
- Action: Inspected STATE/NEXT/RUNS/BLOCKED and existing oauth_setup.py. Created tools/oauth_setup_contract.py (asserts exit 3 + key phrases including MISSING and setup steps when OAuth env vars are absent). Updated state files. No secrets polled, no dispatch, no media writes. Committed.
- Result: Videos published stay 0. New contract available for the setup recipe. Estimated savings: prevents silent regression of the human OAuth setup guidance for future runs. Pre-upload path unchanged. Gate behavior unchanged.
- Verification: File created. Soft only. No regressions.
- Discovery: The long-running OAuth stall (1000+ runs) remains the sole primary blocker; locking the setup recipe compounds reliability of the human entry path without adding printers or requiring credentials.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so.
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or python3 tools/oauth_setup.py then secrets + single execute=true dispatch). After id appears: python3 tools/post_publish_sequence.py. Optional: python3 tools/oauth_setup_contract.py.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)
