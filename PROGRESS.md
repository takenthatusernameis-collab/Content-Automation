# LOG

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 351 — 2026-10-06T00:20:00Z
- The production export probe now refuses the known truncated r249 master and a present master that is not 30fps yuv420p h264 with stereo AAC at 48000 Hz. Estimated save: one private upload of the truncated file if execute starts before a human checks duration. Human minutes per video unchanged until secrets exist. Videos published stay 0.
- Automated step changed: existing `tools/export_probe.py` on the production job. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call while `STALL_UPLOAD_EDGE` is set.

# LOG

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 350 — 2026-10-05T23:20:00Z
- A present master is now rejected before videos.insert unless it is 1920x1080 h264 with audio and at least 20s. Estimated save: one bad private upload and one Studio cleanup if the first execute used a wrong-size file. Human minutes per video unchanged until secrets exist. Videos published stay 0.
- Automated step added: `tools/export_probe.py` in the production workflow before upload gates. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call while `STALL_UPLOAD_EDGE` is set.

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

