# LOG

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 349 — 2026-10-05T22:35:00Z
- Caption, thumbnail, and comment status now early-persist before the next post-upload call. Estimated save: one duplicate captions.insert if the runner dies after the caption write. Human minutes per video unchanged. Videos published stay 0.
- Automated step added: `STALL_UPLOAD_EDGE` after four OAuth-idle upload-edge runs. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call while that flag is set.

# LOG

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 348 — 2026-10-05T22:15:00Z
- Early persist of the provider video id before caption wait, and of dead-session holds before the step returns. Estimated save: one Studio check and one blocked re-execute if the job dies after videos.insert returns an id. Human minutes per video unchanged. Videos published stay 0.
- Automated step added: same UPLOAD_EARLY_PERSIST=1 path now covers the id and the holds. Remaining manual gate: YouTube OAuth secrets and Studio check before any session-hold release.

# LOG

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 347 — 2026-10-05T21:15:00Z
- Early persist of an open resumable Location before the first chunk. Estimated save: one duplicate videos.insert if the runner dies after the session POST. Human minutes per video unchanged. Videos published stay 0.
- Automated step added: production execute sets UPLOAD_EARLY_PERSIST=1. Remaining manual gate: YouTube OAuth secrets and Studio check before any session-hold release.

# LOG

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 346 — dead-session hold can be cleared after Studio shows no video
- Estimated human minutes per video: unchanged. Publish still blocked on OAuth.
- Automated step added: local hold release plus commit decision `commit_session_hold_released`. No provider write.
- Remaining manual steps: YouTube OAuth secrets, playlist id, Studio check before any hold release, pin after comment insert.
- Reliability: an expired Location no longer bricks later executes once a human confirms no video. The workflow cannot clear the hold by itself.

# PROGRESS

Updated: 2026-10-05T19:20:00Z

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 345 — 2026-10-05T19:20:00Z
A dead resumable Location is no longer reused as an open session. 404 or 410 commits a hold and the next execute does not start another videos.insert. Estimated effect: one less duplicate private video if the first session expires before the runner can finish. Human minutes per video unchanged. Videos published stay 0.

## Run 344 — 2026-10-05T18:20:00Z
A killed upload no longer has to start a second videos.insert after Location exists. The session URI is written before the first chunk and committed. Estimated effect: one less duplicate private video on the first real execute if the runner dies mid-upload. Human minutes per video unchanged. Videos published stay 0.

# PROGRESS

Updated: 2026-10-05T17:25:00Z

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 343 — 2026-10-05T17:25:00Z
PROGRESS.md and FAILURES.md no longer sit past the known fetch cut. Newest 12 sections stay live. Older notes are in docs/progress_archive.md and docs/failures_archive.md. Estimated agent minutes saved on the next runs: about 10, by not reconstructing a cut lesson. Human minutes per video unchanged. Videos published stay 0.

## Run 342 — 2026-10-05T17:15:00Z
RUNS.md no longer truncates before the newest run log. Newest 12 entries stay in the live file. Older entries are in docs/runs_archive.md. Estimated agent minutes saved on the next runs: about 10, by not reconstructing the latest action from a cut fetch. Human minutes per video unchanged. Videos published stay 0.

## Run 341 (2026-10-05T16:20:00Z)
- NEXT.md dropped from 28596 bytes to 12 notes. Older notes are in docs/next_archive.md. Estimated agent minutes saved on the next truncated-fetch rediscovery: about 10, if the newest locks are read first. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 340 (2026-10-05T15:20:00Z)
- STATE.md dropped from 52418 bytes and 67 run sections to 12 sections. Older deltas are in docs/state_archive.md. Estimated agent minutes saved on the next truncated-fetch rediscovery: about 10, if the newest gate is read first. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 339 — 2026-10-05T14:20:00Z
The production stall printer no longer treats `No new scanner` as a local-gate run. Estimated agent minutes saved on the next runs: about 10, by not following a false `STALL_LOCAL_GATE` that Runs 336-338 kept rewriting. Human minutes per video unchanged. Videos published stay 0.

## Run 338 — 2026-10-05T12:30:00Z
Persist no longer commits a COLLECTED analytics file that lacks the first-calendar-days stamp. Estimated effect: one less way a sliding or unstamped window becomes the comparison evidence after a later collect. Videos published stay 0. Human minutes on Q1 unchanged.

# PROGRESS

Updated: 2026-10-05T11:20:00Z

- Run 337: a collected analytics file no longer counts unless its window is the video's first 7 calendar days. Estimated agent minutes saved on the first comparison: about 15, by not treating a sliding or unstamped file as the observation. Human minutes per video unchanged. Videos published stay 0.

