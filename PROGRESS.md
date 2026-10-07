# PROGRESS

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

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

## Run 369 — 2026-10-06T19:12:00Z
- Improvement: a post-upload caption, thumbnail, or comment miss no longer fails the production job when the video id is already written. Estimated save: one extra execute dispatch after the first private insert, which could start another videos.insert, about 15 human minutes plus a duplicate private video.
- Efficiency: human minutes per video otherwise unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: selftest PASS. No provider write. Videos published stay 0.

## Run 368 — 2026-10-06T18:12:00Z
- Improvement: a failed playlist insert no longer fails the production job. Estimated save: one extra execute dispatch after the first private insert, which could start another videos.insert, about 15 human minutes plus a duplicate private video.
- Efficiency: human minutes per video otherwise unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: selftest PASS. No provider write. Videos published stay 0.

## Run 367 — 2026-10-06T17:11:00Z
- Improvement: the first Studio end-screen note no longer asks for a playlist element while playlist_id is not_set. Estimated save: one failed end-screen setup after the first private insert, about 5 human minutes.
- Efficiency: human minutes per video otherwise unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: selftest PASS. No provider write. Videos published stay 0.

## Run 366 — 2026-10-06T16:20:00Z
- Improvement: selftest now executes `stall_watch_contract.py` again. A later duplicate function had shadowed that call since the inline checks were added.
- Efficiency: a broken stall contract fails here instead of on a later run that happens to invoke the contract alone. Estimated human minutes per video unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: selftest PASS. No provider write. Videos published stay 0.

