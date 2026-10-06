# PROGRESS

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 357 — 2026-10-06T06:20:00Z
Log compact now collapses stacked file headers. FAILURES.md and PROGRESS.md each show one header and 12 sections. Estimated effect: a truncated fetch no longer hides the newest lesson behind a second file header. Human minutes per video unchanged. Videos published stay 0.

## Run 356 — 2026-10-06T05:11:00Z
- Improvement: the current-gate file is one header again. A truncated fetch no longer lands on a second `# STATE` that looks like a new file, and compact can no longer cut a delta in half by treating the next header as part of the previous section.
- Efficiency: estimated human minutes per video unchanged. Saves a future agent from reconstructing which delta is current. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: state compact contract PASS. Videos published stay 0.


## Run 355 — 2026-10-06T04:15:00Z
- Viewer-facing upload copy no longer includes the chapter-draft label or the draft-pin sentence.
- Estimated human minutes saved on the first upload: about 5 (description and pin edit in Studio after insert). The strip also covers a future packet that still has the old stub sentence.
- Automated steps unchanged. Remaining manual step is still the three YouTube secrets. Videos published stay 0.



## Run 354 — 2026-10-06T03:20:00Z
- Improvement: a repeated pre-upload probe is now machine-visible. `STALL_PREUPLOAD_PROBE` stops the next run from wiring another export, media, or caption checker while videos published stay 0.
- Efficiency: avoids another probe-only run. Estimated human minutes per video unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: stall watch contract PASS. Selftest PASS. No provider write.

## Run 353 — 2026-10-06T02:20:00Z
- A present captions.srt is now rejected before captions.insert when a cue is empty, overlapping, reversed, longer than 42 characters, or past the selected wav. Estimated save: one private video with unreadable or late captions if execute starts before a human opens the srt. Human minutes per video unchanged until secrets exist. Videos published stay 0.
- Automated step added: `tools/caption_gate.py` on the production job after media QA. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call. Do not add another export-probe lock. Do not add another media checker.

## Run 352 — 2026-10-06T01:15:00Z
- The production job now runs media QA after materialize. Estimated save: one private upload of a wrong-size card or a clipped take if execute starts before a human opens the packet. Human minutes per video unchanged until secrets exist. Videos published stay 0.
- Automated step changed: existing `tools/media_qa.py` on the production job. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call. Do not add another export-probe lock.

## Run 351 — 2026-10-06T00:20:00Z
- The production export probe now refuses the known truncated r249 master and a present master that is not 30fps yuv420p h264 with stereo AAC at 48000 Hz. Estimated save: one private upload of the truncated file if execute starts before a human checks duration. Human minutes per video unchanged until secrets exist. Videos published stay 0.
- Automated step changed: existing `tools/export_probe.py` on the production job. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call while `STALL_UPLOAD_EDGE` is set.



## Run 350 — 2026-10-05T23:20:00Z
- A present master is now rejected before videos.insert unless it is 1920x1080 h264 with audio and at least 20s. Estimated save: one bad private upload and one Studio cleanup if the first execute used a wrong-size file. Human minutes per video unchanged until secrets exist. Videos published stay 0.
- Automated step added: `tools/export_probe.py` in the production workflow before upload gates. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call while `STALL_UPLOAD_EDGE` is set.



## Run 349 — 2026-10-05T22:35:00Z
- Caption, thumbnail, and comment status now early-persist before the next post-upload call. Estimated save: one duplicate captions.insert if the runner dies after the caption write. Human minutes per video unchanged. Videos published stay 0.
- Automated step added: `STALL_UPLOAD_EDGE` after four OAuth-idle upload-edge runs. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call while that flag is set.



## Run 348 — 2026-10-05T22:15:00Z
- Early persist of the provider video id before caption wait, and of dead-session holds before the step returns. Estimated save: one Studio check and one blocked re-execute if the job dies after videos.insert returns an id. Human minutes per video unchanged. Videos published stay 0.
- Automated step added: same UPLOAD_EARLY_PERSIST=1 path now covers the id and the holds. Remaining manual gate: YouTube OAuth secrets and Studio check before any session-hold release.



## Run 347 — 2026-10-05T21:15:00Z
- Early persist of an open resumable Location before the first chunk. Estimated save: one duplicate videos.insert if the runner dies after the session POST. Human minutes per video unchanged. Videos published stay 0.
- Automated step added: production execute sets UPLOAD_EARLY_PERSIST=1. Remaining manual gate: YouTube OAuth secrets and Studio check before any session-hold release.



## Run 346 — dead-session hold can be cleared after Studio shows no video
- Estimated human minutes per video: unchanged. Publish still blocked on OAuth.
- Automated step added: local hold release plus commit decision `commit_session_hold_released`. No provider write.
- Remaining manual steps: YouTube OAuth secrets, playlist id, Studio check before any hold release, pin after comment insert.
- Reliability: an expired Location no longer bricks later executes once a human confirms no video. The workflow cannot clear the hold by itself.


Updated: 2026-10-05T19:20:00Z


