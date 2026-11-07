# RUNS

## Run 1100 — 2026-11-07T21:20:00Z
- Objective: Confirm current system health on fresh clone including materialize path and selftest (with compact), record continued OAuth stall for future runs, and leave clear handoff without adding low-leverage artifacts.
- Action: Cloned repository. Ran materialize_q1_release.py (success). Ran media_qa.py (PASS). Ran next_action.py (upload-blocked). Detected NEXT.md over limit (9 notes). Ran next_compact.py (moved 3 notes). Selftest now PASS. No secrets polled, no dispatch, no media writes beyond materialize. Updated state files via record_run.
- Result: All local gates PASS. Videos published stay 0. Pre-upload path unchanged and verified. Estimated savings: future runs start from green selftest and verified materialize path without rediscovery.
- Verification: materialize exit 0; media_qa PASS; next_action upload-blocked; next_compact OK; selftest.py exit 0. Soft documentation only. No regressions.
- Discovery: NEXT.md can drift over the selftest note cap between runs; compact must be part of recording. STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable after materialize. Further pure verification has diminishing returns.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1099 — 2026-11-07T20:15:00Z
- Objective: Restore selftest green by compacting NEXT.md (which had exceeded the 6-note cap) and record the continued OAuth stall for future runs without adding low-leverage artifacts.
- Action: Cloned repository. Detected NEXT.md over limit. Ran next_compact.py (moved 2 notes). Selftest now PASS. No secrets polled, no dispatch, no media writes. Updated state files via record_run.
- Result: Selftest PASS. Videos published stay 0. Pre-upload path unchanged. Estimated savings: future runs start from green selftest without rediscovering the over-limit state.
- Verification: next_compact moved notes; selftest.py exit 0. Soft documentation only. No regressions.
- Discovery: NEXT.md can drift over the selftest note cap between runs; compact_all / next_compact must be part of recording. record_run.py now restores a missing # RUNS header (like other logs) so recording cannot fail partway. STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Further pure verification has diminishing returns.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1098 — 2026-11-07T19:16:00Z
- Objective: Reduce human friction on the remaining OAuth step by clarifying preferred scopes based on current Google documentation, while recording the continued stall.
- Action: Updated docs/HUMAN_PRIORITY.md and docs/human_oauth_checklist.md with preferred scopes (youtube.force-ssl + yt-analytics.readonly; note that force-ssl covers upload and overlapping scopes risk rejection). Updated state files. No secrets polled, no dispatch, no media changes.
- Result: Scope guidance improved. Videos published stay 0. Pre-upload path unchanged. Estimated savings: future human setup less likely to hit overlapping-scope consent rejection; stall status visible immediately.
- Verification: File updates committed successfully. Soft documentation only. No regressions.
- Discovery: Google docs indicate force-ssl covers broader methods including upload; requesting redundant scopes can cause rejection. STALL_OAUTH_IDLE persists across 1000+ runs.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1097 — 2026-11-07T18:15:00Z
- Objective: Confirm current system health on fresh clone including materialize path, record continued OAuth stall for future runs, and leave clear handoff without adding low-leverage artifacts.
- Action: Cloned repository. Ran materialize_q1_release.py (success). Ran media_qa.py (PASS). Ran next_action.py (upload-blocked). Ran selftest.py (PASS). No secrets polled, no dispatch. Updated state files with concise notes via record_run (partial; RUNS manually completed due to missing header).
- Result: All local gates PASS. Videos published stay 0. Pre-upload path unchanged and verified. Estimated savings: future runs can see the stall status and verified materialize path immediately without rediscovery; compactness maintained.
- Verification: materialize exit 0; media_qa PASS; next_action upload-blocked; selftest.py exit 0. Soft documentation only. No regressions.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable after materialize. Further pure verification has diminishing returns.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or docs/human_oauth_checklist.md then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1096 — 2026-11-07T17:15:00Z
- Objective: Confirm current system health on fresh clone, record continued OAuth stall for future runs, and leave clear handoff without adding low-leverage artifacts.
- Action: Cloned repository. Ran selftest.py (PASS). No secrets polled, no dispatch, no media materialize or writes. Updated state files with concise notes.
- Result: Selftest PASS. Videos published stay 0. Pre-upload path unchanged. Estimated savings: future runs can see the stall status immediately without rediscovery; compactness maintained.
- Verification: selftest.py exit 0. Soft documentation only. No regressions.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Further pure verification has diminishing returns.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or docs/human_oauth_checklist.md then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1095 — 2026-11-07T16:19:58Z
- Objective: Confirm current system health on fresh clone, record continued OAuth stall for future runs, and leave clear handoff without adding low-leverage artifacts.
- Action: Cloned repository. Ran selftest.py (PASS). No secrets polled, no dispatch, no media materialize or writes. Updated state files with concise notes.
- Result: Selftest PASS. Videos published stay 0. Pre-upload path unchanged. Estimated savings: future runs can see the stall status immediately without rediscovery; compactness maintained.
- Verification: selftest.py exit 0. Soft documentation only. No regressions.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Further pure verification has diminishing returns.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or docs/human_oauth_checklist.md then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)

Permanent log. Newest first.
