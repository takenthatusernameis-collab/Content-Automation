# PROGRESS

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 387 — 2026-10-07T17:12:00Z
- Improvement: the NEXT header is refreshed in the same process as the note prepend, so a truncated fetch no longer shows Run 385 as current after a later note. Estimated save: about 5 minutes per future run spent reconciling a stale header, and one wrong lock if the header is treated as the newest decision. Videos published stay 0. Human OAuth step unchanged in kind; it is still issue 1.
- Efficiency: automated header refresh. Remaining manual step is still the three YouTube secrets.
- Verification: record_run contract. No provider write.

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 386 — 2026-10-07T16:13:00Z
- Improvement: a log prepend that skips compact now fails selftest, and `record_run.py` compacts in the same process. Estimated save: one red Actions selftest and one repair commit per forgotten compact, about 10 agent minutes. Videos published stay 0. Human OAuth step unchanged in kind; it is now issue 1.
- Efficiency: automated cap check is actually invoked. Remaining manual step is still the three YouTube secrets.
- Verification: record_run contract and selftest. No provider write.


## Run 385 — 2026-10-07T13:23:00Z
- Improvement: another operator-card function now fails selftest instead of waiting for three later deltas to set `STALL_OPERATOR_CARD`. Estimated save: one agent run spent reprinting console steps, about 10 minutes, on every future run that would have grown the card. Videos published stay 0. Human OAuth step unchanged in kind.
- Efficiency: automated freeze covers the existing five functions. Remaining manual step is still the three YouTube secrets.
- Verification: operator-card freeze contract and stall-watch contract. No provider write.

## Run 384 — 2026-10-07T12:20:00Z
- Improvement: the one human command now includes the Google Cloud console steps, scopes, and exchange command, so the next run does not reconstruct them from `oauth_setup.py`. Estimated save: about 10 minutes per future run spent rebuilding the consent steps, and one wrong token scope if only the secret-set lines are followed. Videos published stay 0. Human OAuth step unchanged in kind.
- Efficiency: automated check covers console-step drift. Remaining manual step is still the three YouTube secrets.
- Verification: operator card contract. No provider write.

## Run 383 — 2026-10-07T11:17:00Z
- Improvement: one command prints the human publish step and fails if it drifts from the OAuth recipe or the documented master sha. Estimated save: about 5 minutes per future run spent reconstructing the human step from NEXT notes, and one wrong dispatch if the recipe and the notes diverge. Videos published stay 0. Human OAuth step unchanged.
- Efficiency: automated check covers the dispatch line. Remaining manual step is still the three YouTube secrets.
- Verification: operator card contract. No provider write.

## Run 382 — 2026-10-07T10:14:00Z
- Improvement: a new provider-state recovery edge now fails selftest instead of waiting for four later deltas to set `STALL_RECOVERY_EDGE`. Estimated save: one agent run spent wiring another recover path, about 15 minutes, on every future run that would have grown the surface. Videos published stay 0. Human OAuth step unchanged.
- Efficiency: automated freeze covers the existing artifact and recover call. Remaining manual step is still the three YouTube secrets.
- Verification: recovery freeze contract and selftest. Release master sha256 matched. No provider write.



## Run 381 — 2026-10-07T09:13:00Z
- Improvement: stacked recovery edges while unpublished now print `STALL_RECOVERY_EDGE`. Estimated save: one agent run spent adding another recover path, about 15 minutes, once the last four deltas match. Videos published stay 0. Human OAuth step unchanged.
- Efficiency: automated stall check now names this pattern. Remaining manual step is still the three YouTube secrets.
- Verification: stall watch contract. No provider write.


## Run 380 — 2026-10-07T08:11:00Z
- Improvement: one command compacts STATE, NEXT, RUNS, PROGRESS, and FAILURES and fails if any file stays over cap. Estimated save: one red Actions selftest and one repair commit per forgotten compact, about 10 agent minutes. Videos published stay 0. Human OAuth step unchanged.
- Efficiency: automated log-cap step is now one command instead of four. Remaining manual step is still the three YouTube secrets.
- Verification: compact_all and selftest on this commit. No provider write.

## Run 379 — 2026-10-07T07:16:00Z
- Improvement: a red Actions selftest is fixed by the existing compact tools, not by another recovery edge. Estimated save: one failed selftest cycle and one agent run spent diagnosing a cap miss, about 10 minutes, on every future run that prepends a section and forgets to archive.
- Efficiency: human minutes per video unchanged. Videos published stay 0. Remaining manual step is still the three YouTube secrets.
- Verification: Actions run 37580716646 failed on the 12-section cap. Compact tools moved the overflow into the archives.

## Run 378 — 2026-10-07T06:14:00Z
- Improvement: rejected-push recovery skips a newer artifact with no provider video id. Estimated save: one duplicate `videos.insert` if a later failed execute hid the first id, about 15 human minutes plus a duplicate private video. Videos published stay 0. Human OAuth step unchanged. Q1 materialize and media QA still PASS.

## Run 377 — 2026-10-07T05:11:00Z
- Improvement: rejected-push recovery skips a later production run that did not upload `provider-upload-state`. Estimated save: one missed artifact download and one duplicate `videos.insert` after an execute=false dispatch, about 15 human minutes plus a duplicate private video. Videos published stay 0. Human OAuth step unchanged.

## Run 376 — 2026-10-07T04:12:00Z
- Improvement: rejected-push recovery now selects the production workflow run, not the newest Actions run. Estimated save: one missed `provider-upload-state` download and one duplicate `videos.insert` after a later selftest run, about 15 human minutes plus a duplicate private video. Videos published stay 0. Human OAuth step unchanged.

