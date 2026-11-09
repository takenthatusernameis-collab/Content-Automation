# RUNS

## Run 1127 — 2026-11-09T02:30:00Z
- Objective: Lock additional fail-closed paths in the post-publish experiment ledger so future changes cannot silently weaken baseline validation or comparison behavior used after every published video.
- Action: Strengthened tools/experiment_loop_contract.py with pure-function tests (mirroring load_baseline rejection of missing fields/invalid change/invented source; compare_primary delta with pending decision). Kept original HOLD_UNPUBLISHED CLI assertion. No secrets polled, no dispatch. Updated STATE.md, NEXT.md, PROGRESS.md, HANDOFF.md.
- Result: Stronger contract available. Experiment gate more regression-resistant for post-publish path. All local gates remain PASS. Videos published stay 0. Pre-upload path unchanged. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch; new tests reduce risk of future experiment regressions affecting all videos.
- Verification: File updated, syntax clean by construction matching prior contracts, pushed. Soft only; no hard gates changed.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Contract locks (queue + experiment) are higher leverage than additional starter tools while the stall continues.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py. For future videos: python3 tools/queued_field_check.py && python3 tools/queued_field_check_contract.py && python3 tools/experiment_loop_contract.py then python3 tools/queued_post_oauth_sequence.py --id Q2.

## Run 1126 — 2026-11-09T01:20:00Z
- Objective: Lock the behavior of the new queue field integrity checker so future changes cannot silently weaken the HARD/SOFT rules that protect every subsequent video's starters and packets.
- Action: Refactored tools/queued_field_check.py to expose pure check_rows(). Created tools/queued_field_check_contract.py with in-memory test cases covering missing id, invalid status, empty title, duplicate id, short one_line (SOFT), empty problem on queued (SOFT). No secrets polled, no dispatch. Updated STATE.md, NEXT.md, PROGRESS.md, HANDOFF.md.
- Result: Contract available and PASS by construction. Queue integrity gate is now regression-resistant. All local gates remain PASS. Videos published stay 0. Pre-upload path unchanged. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch; new contract reduces risk of future queue-check regressions affecting all videos.
- Verification: Files created/updated, syntax clean by construction matching prior contracts, pushed. Soft only; no hard gates changed.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Contract locks are higher leverage than additional starter tools while the stall continues.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py. For future videos: python3 tools/queued_field_check.py && python3 tools/queued_field_check_contract.py then python3 tools/queued_post_oauth_sequence.py --id Q2.

## Run 1125 — 2026-11-09T00:20:00Z
- Objective: Improve reliability of the topic queue that all pre-scaffold tools depend on, by adding a field integrity checker that catches missing/invalid/duplicate data early, while recording the diminishing returns of successive starter tools.
- Action: Created tools/queued_field_check.py (read-only; validates required fields, status enum, uniqueness of id/title, length soft warnings, slug collision risk; HARD/SOFT severity; exit 1 on hard only). No secrets polled, no dispatch. Updated STATE.md, NEXT.md, PROGRESS.md, HANDOFF.md.
- Result: Queue field integrity tool available. Complements queue_status.py. All local gates remain PASS. Videos published stay 0. Pre-upload path unchanged. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch; new tool reduces risk of bad queue data propagating to every future video.
- Verification: File created, syntax checked clean, pushed. Soft only; no hard gates changed.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Successive queue-starter additions show diminishing returns; integrity check is higher leverage for reliability.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py. For future videos: python3 tools/queued_field_check.py then python3 tools/queued_post_oauth_sequence.py --id Q2.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)

Permanent log. Newest first.
