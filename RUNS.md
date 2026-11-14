# RUNS

## Run 1257 — 2026-11-14T16:45:00Z
- Objective: Prevent recurring RUNS.md size-cap overflows by making compaction size-aware.
- Action: Inspected STATE.md, NEXT.md, RUNS.md. Cloned repo. Confirmed contracts 96/96 and selftest PASS. Patched tools/runs_compact.py to enforce a 15500-byte soft target (in addition to max 12 entries) by moving additional older sections when needed. Ran compact; it moved 1 entry. Verified contracts_suite.py PASS (96/96) and selftest PASS. No secrets polled, no dispatch, no media writes, no scaffolding.
- Result: Live run log now 14288 bytes with margin. Contracts 96/96. Selftest PASS. Pre-upload path unchanged and reliable. STALL_OAUTH_IDLE continues (HIGH suspicion). Long stall is increasingly suspicious.
- Verification: Local contracts 96/96; selftest PASS; runs_compact_contract PASS; post-compact size under target.
- Discovery: Count-only compaction can still overflow the byte contract when recent sections are long; a soft byte target with a floor of 4 newest entries prevents the failure mode seen in prior runs without breaking the existing contract test.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py). After Q1 ships and window due, use after_upload_steps.py then feedback_review_brief.py.

## Run 1256 — 2026-11-14T15:30:00Z
- Objective: Restore RUNS.md hard size cap after prior compaction left the file over the 16000-byte limit.
- Action: Inspected STATE.md, NEXT.md, RUNS.md. Cloned repo. Confirmed runs_compact_contract FAIL (16026 bytes). Extracted oldest section (Run 1244) and prepended to docs/runs_archive.md. Truncated live RUNS.md. Verified contracts_suite.py PASS (96/96) and selftest PASS. No secrets polled, no dispatch, no media writes, no scaffolding.
- Result: Live run log under size cap. Contracts 96/96. Selftest PASS. Pre-upload path unchanged and reliable. STALL_OAUTH_IDLE continues (HIGH suspicion). Long stall is increasingly suspicious.
- Verification: Local contracts 96/96; selftest PASS; runs_compact_contract PASS. Files updated via record_run.
- Discovery: Prior compaction claim left residual overflow; exact size check is sensitive to trailing content. Compaction must leave clear margin.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py). After Q1 ships and window due, use after_upload_steps.py then feedback_review_brief.py.

## Run 1254 — 2026-11-14T11:25:00Z
- Objective: Reduce a recurring post-publish failure mode by making the OAuth consent-screen Production publish a hard critical step (Testing-mode tokens expire after 7 days; feedback window is +10 days).
- Action: Inspected STATE.md, NEXT.md, RUNS.md, PROGRESS.md, BLOCKED.md, ROADMAP.md, HUMAN_PRIORITY.md, human_starter.py, oauth_complete_guide.py. Cloned repo, confirmed contracts_suite.py PASS (96/96) and selftest PASS. Updated phased plan in human_starter.py and section 1 of oauth_complete_guide.py to call out the Production publish as CRITICAL with the exact lifetime reason. No secrets polled, no dispatch, no media writes, no scaffolding.
- Result: Human guides now surface the token-lifetime pitfall more prominently before minting. Contracts remain 96/96. Selftest PASS. Pre-upload path unchanged and reliable. STALL_OAUTH_IDLE continues (HIGH suspicion). Long stall is increasingly suspicious.
- Verification: Local contracts 96/96; selftest PASS; human_starter and oauth_complete_guide print the new CRITICAL lines. Files updated with single newest-first entries.
- Discovery: The 7-day vs 10-day mismatch is a silent failure mode that pure confirmation runs cannot catch; elevating it in the primary human entry points reduces the chance the first feedback collect fails for token expiry.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py). After Q1 ships and window due, use after_upload_steps.py then feedback_review_brief.py.

## Run 1253 — 2026-11-14T10:20:00Z
- Objective: Make the remaining human OAuth step clearer by adding a phased action plan early in human_starter.py.
- Action: Inspected STATE.md, NEXT.md, RUNS.md, PROGRESS.md, BLOCKED.md, ROADMAP.md, HUMAN_PRIORITY.md, human_starter.py, long_stall_report.py. Cloned repo, confirmed contracts_suite.py PASS (96/96) and selftest PASS. Added PHASED ACTION PLAN (A: Cloud setup, B: mint, C: secrets, D: dispatch+confirm) near the top of human_starter.py. No secrets polled, no dispatch, no media writes, no scaffolding.
- Result: Human starter now surfaces the ordered phases immediately. Contracts remain 96/96. Selftest PASS. Pre-upload path unchanged and reliable. STALL_OAUTH_IDLE continues (HIGH suspicion). Long stall is increasingly suspicious.
- Verification: Local contracts 96/96; selftest PASS; human_starter_contract PASS; human_starter prints the new plan. Files updated with single newest-first entries.
- Discovery: Explicit early phased plan reduces chance a human skips the Production publish step or mixes phases.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py). After Q1 ships and window due, use after_upload_steps.py then feedback_review_brief.py.

## Run 1252 — 2026-11-14T09:20:00Z
- Objective: Make long-stall consecutive evidence clearer by counting recent RUNS.md sections that contain STALL_OAUTH_IDLE.
- Action: Inspected STATE.md, NEXT.md, RUNS.md, PROGRESS.md, BLOCKED.md, ROADMAP.md, HUMAN_PRIORITY.md, long_stall_report.py. Cloned repo, confirmed contracts_suite.py PASS (96/96) and selftest PASS. Updated count_zero_publish_runs to also match STALL_OAUTH_IDLE. No secrets polled, no dispatch, no media writes, no scaffolding.
- Result: Stall report now surfaces consecutive recent idle sections (8 in main file). Contracts remain 96/96. Selftest PASS. Pre-upload path unchanged and reliable. STALL_OAUTH_IDLE continues (HIGH suspicion). Long stall is increasingly suspicious.
- Verification: Local contracts 96/96; selftest PASS; long_stall_report runs and prints streak of 8. Files updated with single newest-first entries.
- Discovery: Exact published=0 phrase matching missed recent sections that use STALL_OAUTH_IDLE in the blocker line; broader matching gives accurate consecutive streak in the live file.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py). After Q1 ships and window due, use after_upload_steps.py then feedback_review_brief.py.

## Run 1251 — 2026-11-14T08:25:00Z
- Objective: Make long-stall evidence clearer by reporting the highest run number from live RUNS.md, reinforcing the scale of the sole human OAuth blocker.
- Action: Inspected STATE.md, NEXT.md, RUNS.md, PROGRESS.md, BLOCKED.md, ROADMAP.md, HUMAN_PRIORITY.md, long_stall_report.py. Cloned repo, confirmed contracts_suite.py PASS (96/96) and selftest PASS. Added max_run_number helper and print to long_stall_report.py. No secrets polled, no dispatch, no media writes, no scaffolding.
- Result: Stall report now surfaces approximate total runs (~1250). Contracts remain 96/96. Selftest PASS. Pre-upload path unchanged and reliable. STALL_OAUTH_IDLE continues (HIGH suspicion). Long stall is increasingly suspicious.
- Verification: Local contracts 96/96; selftest PASS; long_stall_report runs and prints highest run. Files updated with single newest-first entries.
- Discovery: Reporting the concrete highest run number makes the duration of the stall more immediately visible without relying solely on the "1000+" label.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py). After Q1 ships and window due, use after_upload_steps.py then feedback_review_brief.py.

## Run 1250 — 2026-11-14T09:20:00Z
- Objective: Improve long_stall_report clarity on streak duration and reinforce diminishing returns of pure-confirmation runs while STALL_OAUTH_IDLE is the sole blocker.
- Action: Inspected STATE.md, NEXT.md, RUNS.md, PROGRESS.md, BLOCKED.md, ROADMAP.md, HUMAN_PRIORITY.md, stall_watch.py, long_stall_report.py. Cloned repo, confirmed contracts_suite.py PASS (96/96) and selftest PASS. Enhanced long_stall_report.py to print clearer date range and suspicion note. No secrets polled, no dispatch, no media writes, no scaffolding.
- Result: Stall report more actionable for humans. Contracts remain 96/96. Selftest PASS. Pre-upload path unchanged and reliable. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Long stall is increasingly suspicious.
- Verification: Local contracts 96/96; selftest PASS. Files updated with single newest-first entries.
- Discovery: Visible streak in main RUNS.md is short; full history is in archive. Pure confirmation continues to have diminishing returns.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py). After Q1 ships and window due, use after_upload_steps.py then feedback_review_brief.py.

## Run 1249 — 2026-11-14T06:20:00Z
- Objective: Make stall detection more reliable by expanding is_idle_delta to catch common wording variants of the long OAuth idle, so pure-confirmation runs correctly surface the HIGH suspicion flag.
- Action: Inspected STATE.md, NEXT.md, RUNS.md, PROGRESS.md, BLOCKED.md, ROADMAP.md, HUMAN_PRIORITY.md, stall_watch.py. Cloned repo, confirmed contracts_suite.py PASS (96/96) and selftest PASS. Expanded no_poll and published_zero predicates in tools/stall_watch.py. Verified the change detects the recent notes as idle (streak now reported). No secrets polled, no dispatch, no media writes, no scaffolding.
- Result: Stall detection is more robust. Contracts remain 96/96. Selftest PASS. Pre-upload path unchanged and reliable. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Long stall is increasingly suspicious.
- Verification: Local contracts 96/96; selftest PASS; stall_watch now reports idle_streak on current STATE.md. Files updated with single newest-first entries.
- Discovery: Exact phrase matching for idle detection was fragile to normal status-note paraphrasing; broader but still fail-closed predicates prevent silent under-detection of the sole blocker.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py). After Q1 ships and window due, use after_upload_steps.py then feedback_review_brief.py.

## Run 1248 — 2026-11-14T05:15:00Z
- Objective: Confirm current reliable state after the refuse-guard addition and record continued stall without introducing new low-value changes.
- Action: Inspected STATE.md, NEXT.md, RUNS.md, PROGRESS.md, BLOCKED.md, ROADMAP.md, HUMAN_PRIORITY.md, NEXT_RUN_PROMPT.md. Cloned repo, confirmed contracts_suite.py PASS (96/96) and selftest PASS. Reviewed record_run.py guard. No secrets polled, no dispatch, no media writes, no scaffolding, no new status printers.
- Result: System remains green and pre-upload path reliable. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Refuse-guard protects against known exact-string regression.
- Verification: Local contracts 96/96; selftest PASS. Files will be updated with single newest-first entries via record_run.
- Discovery: The combination of exact-string compact checks and status notes is fragile; the writer-side refuse is the correct fix. Pure confirmation runs continue to have diminishing returns while the sole blocker is human OAuth.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py). After Q1 ships and window due, use after_upload_steps.py then feedback_review_brief.py.

## Run 1247 — 2026-11-14T04:15:00Z
- Objective: Prevent recurrence of the exact-string archive pointer failure that broke selftest in Runs 1245-1246 by adding a refuse-guard in the recording path.
- Action: Inspected STATE.md, NEXT.md, RUNS.md, PROGRESS.md. Cloned repo, confirmed contracts_suite.py PASS (96/96) and selftest PASS. Patched tools/record_run.py to refuse any progress/failures note that contains the exact archive pointer string before writing. Verified syntax. No secrets polled, no dispatch, no media writes, no scaffolding.
- Result: Guard in place. Future runs using record_run.py cannot accidentally reintroduce the count!=1 failure. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload path unchanged and reliable.
- Verification: Local contracts 96/96; selftest PASS; py_compile OK on patched file. Files will be updated with single newest-first entries.
- Discovery: Exact-string checks in compact_all are fragile to self-referential notes; a writer-side refuse is more reliable than post-hoc rewording.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py). After Q1 ships and window due, use after_upload_steps.py then feedback_review_brief.py.

Permanent log. Newest first.
