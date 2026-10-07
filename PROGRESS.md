# PROGRESS

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

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

## Run 375 — 2026-10-07T03:11:00Z
- Improvement: a rejected provider-state push still leaves `upload_state.json` as the `provider-upload-state` artifact for 90 days. Estimated save: one duplicate `videos.insert` when main never received the video id, about 15 human minutes plus a duplicate private video. Videos published stay 0. Human OAuth step unchanged.


## Run 374 — 2026-10-07T02:13:00Z
- Persist no longer drops a classified-miss video id to keep the job green. Estimated save: one duplicate `videos.insert` and one lost id if classify crashes after the file is written. Videos published stay 0. Human OAuth step unchanged.

## Run 373 — 2026-10-07T01:15:00Z
- Improvement: provider-state push now runs. The previous heredoc never closed, so a successful insert would not land `upload_state.json` on main. Estimated save: one lost video id and a second execute that could insert again, about 15 human minutes plus a duplicate private video.
- Efficiency: human minutes per video otherwise unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets. Videos published stay 0.
- Verification: selftest PASS. Workflow heredoc count is 0. No provider write.

## Run 372 — 2026-10-07T00:15:00Z
- Improvement: a persist classify miss after a provider video id exists no longer fails the job. Estimated save: one avoided second execute after videos.insert, about 10 human minutes if the first insert already landed.
- Efficiency: human minutes per video otherwise unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets. Videos published stay 0.
- Verification: selftest PASS. No provider write.

## Run 371 — 2026-10-06T23:13:00Z
- Improvement: a playlist membership crash no longer fails the production job after upload state exists, and the job summary no longer tells the operator that a caption miss fails the job. Estimated save: one extra execute dispatch after the first private insert, which could start another videos.insert, about 15 human minutes plus a duplicate private video.
- Efficiency: human minutes per video otherwise unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: selftest PASS. No provider write. Videos published stay 0.

## Run 370 — 2026-10-06T21:16:00Z
- The execute job no longer turns red when the Studio pin printer fails or when a provider-state commit/push fails after a video id is written. That removes a false signal to dispatch execute again. Human minutes per video unchanged. Videos published stay 0. Automated post-insert steps that must not fail the job: playlist exit 2, post-upload exit 4 with a video id, Studio pin non-zero, persist miss with a video id.

