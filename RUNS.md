# RUNS

## Run 366 — 2026-10-06T16:20:00Z
- Objective: Stop a shadowed stall-watch check from letting a broken contract print SELFTEST PASS.
- Action: Merged the two `check_stall_watch` definitions in `tools/selftest.py`. The remaining check runs `stall_watch_contract.py` and the inline OAuth-idle assertions. Removed the duplicate call. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: The later definition replaced the contract call. Selftest invoked the name twice and still never ran the contract.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 365 — 2026-10-06T15:20:00Z
- Objective: Restore a green selftest after a zero idle streak was treated as a stall flag and the live logs exceeded the compact cap.
- Action: `tools/stall_watch.py` omits `idle_streak: 0` from `flag_text`. A positive streak and `suspicious: oauth_idle_without_publish` at 8 or more stay. Compact moved the oldest STATE delta and the oldest NEXT note into the archives. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Stall contract passed. State and next compact contracts passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. Compact tools printed OK. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 364 made every file print a streak, including a clear file. Selftest treats a non-empty `flag_text` as a stall. The live STATE and NEXT files were also one section over the cap, so the compact contracts failed.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 364 — 2026-10-06T13:22:00Z
- Objective: Make the repeated unpublished OAuth stall countable so later runs can flag it instead of restating it.
- Action: `tools/stall_watch.py` prints `idle_streak` and `suspicious: oauth_idle_without_publish` at 8 or more consecutive unpublished unpolled deltas. Contract covers the streak, the suspicious line, and a reset when the newest delta is not that shape. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Contract passed. Videos published stay 0. No live execute. Idle streak on this STATE is 13.
- Verification: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. Actions not re-run. No provider write.
- Discovery: Runs 352-363 each said videos published stay 0 and OAuth was not polled. The idle flag already existed, but it did not say how long the stall had lasted.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 363 — 2026-10-06T12:20:00Z
- Objective: Stop a progress section that omits the Run heading from being dropped by the size cap.
- Action: `tools/log_compact.py` promotes a bare `NNN — timestamp` line to a Run heading before it splits sections. Restored the Run 360 heading. Moved Run 351 and Run 350 progress sections into `docs/progress_archive.md`. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Contract passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/log_compact_contract.py` printed LOG COMPACT CONTRACT PASS. Actions not re-run. No provider write.
- Discovery: Run 360 wrote `360 — 2026-10-06T09:11:00Z` without the section prefix. Compact splits only on the Run heading, so that lesson was body text of Run 361.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-idle runs have not published a video. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 362 — 2026-10-06T11:20:00Z
- Objective: Make the first private execute a copy-paste dispatch instead of an unscripted workflow click.
- Action: `tools/oauth_setup.py` now prints `gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false`. Selftest requires that command. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Recipe check passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `check_oauth_setup_recipe` returned no failures. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Step 8 named execute=true but not the `gh` invocation. A first dispatch with collect_feedback=true would fetch before a video id exists.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-idle runs have not published a video. Do not add another exchange parser.
- Next: A human stores the three secrets and runs that dispatch. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 361 — 2026-10-06T10:12:00Z
- Objective: Stop lock sentences from keeping stall flags set, and stop a last chapter inside the final 10 seconds from being uploaded as if YouTube would show it.
- Action: `stall_watch.py` scrubs do-not-add sentences before the pre-upload and upload-edge token checks. `chapter_sync_reason` takes an optional duration and refuses `chapter_last_under_10s_before_end`. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser.
- Result: Stall contract passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Newest STATE deltas repeated the lock sentence, and that sentence contained the same tokens as a wired probe. The flag could not clear. YouTube also drops a chapter list whose last stamp is inside the final 10 seconds. That check was missing.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-idle runs have not published a video. Do not add another exchange parser.
- Next: A human stores the three secrets and dispatches execute=true. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 360 — 2026-10-06T09:11:00Z
- Objective: Stop a second Active locks block from hiding the one human step on a truncated NEXT.md fetch.
- Action: `next_compact.py` keeps one Active locks block and drops a lone `.` paragraph. NEXT.md now names the three secrets as the step. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload probe. Did not add another OAuth exchange parser.
- Result: Contract passed. Oldest NEXT note archived. Videos published stay 0. No live execute.
- Verification: `python3 tools/next_compact_contract.py` printed NEXT COMPACT CONTRACT PASS. Actions not re-run. No provider write.
- Discovery: NEXT.md had two Active locks blocks plus a `.` paragraph. A truncated fetch could land in the copy and miss the human step. Runs 358-359 added exchange parsers and published nothing.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-helper runs have not published a video. Do not add another exchange parser.
- Next: A human stores the three secrets and dispatches execute=true. Do not add another probe. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 359 — 2026-10-06T08:11:00Z
- Objective: Stop the first OAuth exchange from failing when the human pastes the localhost address bar.
- Action: `oauth_exchange.py` extracts the code from a redirect URL or a raw code. Denied redirects are refused. The token still writes only outside the repo. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload probe.
- Result: Contract passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/oauth_exchange_contract.py` printed OAUTH EXCHANGE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Desktop consent does not load localhost. The code is in the address bar. A raw-code-only stdin read would send that URL to the token endpoint.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-idle runs have not published a video. Do not add another probe.
- Next: A human runs the exchange once and stores the three secrets. Paste the full redirect URL. Do not add another probe. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 358 — 2026-10-06T07:15:00Z
- Objective: Cut the manual OAuth token exchange down to one local command that cannot commit the refresh token.
- Action: Added `tools/oauth_exchange.py` and a contract. The recipe now points at it. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload probe.
- Result: Contract passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/oauth_exchange_contract.py` printed OAUTH EXCHANGE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: The setup recipe named the scopes but still left the consent URL and token POST to an unscripted browser step. A wrong scope still creates a private video that cannot take captions.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human runs the exchange once and stores the three secrets. Do not add another probe. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 357 — 2026-10-06T06:20:00Z
- Objective: Stop stacked FAILURES and PROGRESS headers from hiding the newest lesson.
- Action: `log_compact.py` drops a later file header and a repeated archive pointer. Both live logs now have one header and 12 sections. Finished the cut Run 356 STATE bullet. Did not poll secrets. Did not add a scanner or a probe.
- Result: Contracts passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/log_compact_contract.py` printed LOG COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 356 collapsed STATE headers only. FAILURES and PROGRESS still had stacked headers.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not prepend a second file header. Do not add another probe. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 356 — 2026-10-06T05:11:00Z
- Objective: Stop stacked STATE headers from hiding or truncating the current gate.
- Action: `state_compact.py` now keeps one preamble and strips later `# STATE` headers before the size cap. Collapsed the live file from 13 headers to 1. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload probe.
- Result: Contract passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/state_compact_contract.py` printed STATE COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Each run prepended a full `# STATE` file. Compact counted `## Run` only, so the Run 343 body was already cut and a dangling header remained.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not prepend a second `# STATE` header. Do not add another export probe, media checker, or caption cue gate. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

Older runs live in `docs/runs_archive.md`. Do not paste the archive back. `tools/runs_compact.py` moves extras. It does not delete history.
