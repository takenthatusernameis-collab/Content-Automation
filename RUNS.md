# RUNS
## Run 931 — 2026-10-31T13:25:00Z
- Objective: Eliminate remaining clock divergence in the cut-list planner so timeline.md stays consistent with speaking-time and end-screen estimates on every future packet.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Updated tools/timeline.py to import and use phrase_utils.effective_rate, extract_sections, and count_spoken_words. Removed hardcoded 150 wpm and local extract/word-count. Cut lists now prefer observed WPM when a Selected VO exists, otherwise the calibrated 190/140. No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. Timeline planner now shares the same rate path as the other duration tools. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Code change committed; timeline.py now calls effective_rate and shared helpers. No packet writes. Logical consistency with prior duration alignment verified by inspection.
- Discovery: timeline.py had retained a fixed 150 wpm while speaking-time, end-screen, and minimum-timeline tools had moved to effective_rate; this was a remaining source of divergent hold and end-screen planning.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

## Run 929 — 2026-10-31T11:21:00Z
- Objective: Make duration estimates self-calibrating to a real Selected VO so tools no longer require manual rate overrides once a take exists.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Added observed_wpm + effective_rate helpers to tools/phrase_utils.py (prefers observed WPM within 80-250 bounds when Selected VO is present, else falls back to select_rate). Updated tools/speaking_time_estimate.py, tools/end_screen_reserve_check.py, and tools/minimum_timeline_estimate.py to call effective_rate. No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. Duration tools now automatically use the packet's real observed rate when a take exists, eliminating remaining manual calibration labor. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Local run of speaking_time_estimate.py on Q1 (no VO in clone) still prints 190 wpm generated fallback; code changes committed and pulled cleanly. No packet writes.
- Discovery: Prior select_rate only covered origin default; once a take exists the tools still needed a human or agent to notice and override the rate. effective_rate closes that gap permanently.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

## Run 928 — 2026-10-31T10:17:00Z
- Objective: Eliminate remaining local duplication of generated/human WPM rate selection so duration tools stay permanently consistent.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Added select_rate + HUMAN_WPM/GENERATED_WPM constants to tools/phrase_utils.py. Updated tools/speaking_time_estimate.py, tools/end_screen_reserve_check.py, and tools/minimum_timeline_estimate.py to import and call the shared helper instead of local copies. No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. Rate selection is now a single source of truth. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Code changes committed; the three tools now share the identical select_rate path. No packet writes.
- Discovery: Local rate logic remaining in each tool after prior alignment still created a maintenance surface for future divergence.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

## Run 927 — 2026-10-31T09:17:00Z
- Objective: Eliminate remaining rate divergence across duration planning tools so generated-narration packets receive consistent estimates.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Updated tools/end_screen_reserve_check.py and tools/minimum_timeline_estimate.py to select 190 wpm when vo_origin.md marks generated and 140 wpm otherwise, matching the logic already present in speaking_time_estimate.py. No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. End-screen reserve and minimum-timeline estimates now share the same calibrated rate path as speaking-time estimates. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Code changes committed; rate selection is identical across the three duration tools. No packet writes.
- Discovery: Fixed 150 wpm in the two planning tools continued to diverge from the calibrated 190/140 path, risking inconsistent end-screen and hold planning on future generated packets.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)
