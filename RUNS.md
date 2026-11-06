## Run 1073 — 2026-11-06T17:19:00Z
- Objective: Lock the observation window due-date calculation against drift so post-publish readiness stays reliable once a video id exists.
- Action: Inspected observation_window.py, STATE/NEXT/RUNS. Added tools/observation_window_contract.py that self-tests parse_uploaded_at + 10-day due date and rejects garbage dates. Updated state files. No secrets polled, no dispatch, no media writes. Committed.
- Result: Videos published stay 0. Due-date logic now has a mechanical lock. Estimated savings: reduced chance of rediscovering or breaking the +10 day window formula. Pre-upload path unchanged. Gate behavior unchanged.
- Verification: observation_window_contract.py created and committed. Soft contract only. No regressions.
- Discovery: The long-running OAuth stall (1000+ runs) remains the sole primary blocker; a small contract on the observation helper continues to compound readiness for the eventual publish and feedback loop.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so.
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or docs/human_oauth_checklist.md then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py. Optional: python3 tools/observation_window_contract.py.

## Run 1072 — 2026-11-06T16:20:00Z
- Objective: Reduce rediscovery by aligning the human OAuth checklist description with the actual sequence in the preferred single entry point.
- Action: Inspected human_starter.py, human_oauth_checklist.md, STATE/NEXT/RUNS. Updated docs/human_oauth_checklist.md Quick start and Current stall note to include observation_window.py sequencing and the post-id next steps summary printed by the starter. Updated state files. No secrets polled, no dispatch, no media writes. Committed.
- Result: Videos published stay 0. Checklist now accurately describes the starter's full sequence. Estimated savings: reduced lookup for what the starter runs and the post-id path. Pre-upload path unchanged. Gate behavior unchanged.
- Verification: human_oauth_checklist.md updated and committed. Soft documentation only. No regressions.
- Discovery: The long-running OAuth stall (1000+ runs) remains the sole primary blocker; keeping the checklist in sync with starter enhancements continues to compound readiness for the eventual publish and feedback loop.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so.
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or docs/human_oauth_checklist.md then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py. Optional: python3 tools/contract_streak_detector.py.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)
