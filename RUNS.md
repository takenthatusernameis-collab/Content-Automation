## Run 1071 — 2026-11-06T15:21:00Z
- Objective: Reduce friction for post-id observation by making the due-date calculator visible in the preferred single entry point.
- Action: Inspected human_starter.py, observation_window.py, STATE/NEXT/RUNS. Sequenced tools/observation_window.py (Q1 packet) inside tools/human_starter.py so it runs automatically and reports not_uploaded until an id exists. Updated state files. No secrets polled, no dispatch, no media writes. Committed.
- Result: Videos published stay 0. Human running the starter now sees the observation window tool output without opening it separately. Estimated savings: reduced lookup for due-date formula after dispatch. Pre-upload path unchanged. Gate behavior unchanged.
- Verification: human_starter.py updated and committed. Soft sequencing only. No regressions.
- Discovery: The long-running OAuth stall (1000+ runs) remains the sole primary blocker; sequencing the observation window tool in the starter continues to compound readiness for the eventual publish and feedback loop.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so.
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or docs/human_oauth_checklist.md then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py. Optional: python3 tools/contract_streak_detector.py.

## Run 1070 — 2026-11-06T14:26:00Z
- Objective: Reduce friction after the private video id appears by surfacing the ordered post-publish path in the preferred single entry point.
- Action: Inspected human_starter.py, post_publish_sequence.py, STATE/NEXT/RUNS. Added a concise post-id next steps summary (success check, post_publish_sequence, +10 day observation window, no early collect, no re-dispatch, Studio pin reminder) to tools/human_starter.py. Updated state files. No secrets polled, no dispatch, no media writes. Committed.
- Result: Videos published stay 0. Human running the starter now sees the post-id path summarized without opening post_publish_sequence.py first. Estimated savings: reduced lookup for the observation window and next tools after dispatch. Pre-upload path unchanged. Gate behavior unchanged.
- Verification: human_starter.py updated and committed. Soft clarification only. No regressions.
- Discovery: The long-running OAuth stall (1000+ runs) remains the sole primary blocker; summarizing the post-id sequence in the starter continues to compound readiness for the eventual publish and feedback loop.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so.
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or docs/human_oauth_checklist.md then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py. Optional: python3 tools/contract_streak_detector.py.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)
