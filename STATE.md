# STATE

Updated: 2026-10-06T04:15:00Z (Run 355)

## Run 355 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `STALL_PREUPLOAD_PROBE` still stands. `playlist_id` remains `not_set`. Do not add another export probe, media checker, or caption cue gate. Do not add another upload-edge persist call.
- The approved Q1 description still contained `Chapter draft (not ASR, not an approval...)` and the approved pin still ended with `This comment is a draft pin, not posted.` `videos.insert` and `commentThreads.insert` would have published those notes. `parse_publish` now drops that chapter label and that pin sentence. Chapter timestamp lines stay. `publish.md` and `publish_brief.py` no longer emit them. This does not call YouTube.
- Local dry-run still HOLD_LOCAL (missing master in this checkout, missing OAuth). Chapter label and draft-pin sentence were absent from the dry-run text. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-06T03:20:00Z (Run 354)

## Run 354 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. Do not add another upload-edge persist call. Do not add another export-probe lock. Do not add another media checker. Do not add another caption cue gate.
- Runs 350-353 each wired a pre-upload checker (`tools/export_probe.py`, `tools/media_qa.py`, `tools/caption_gate.py`) while videos published stayed 0. `tools/stall_watch.py` now prints `STALL_PREUPLOAD_PROBE` after four such deltas. The flag does not fail the job. It does not call YouTube. Do not wire another export probe, media checker, or caption cue gate while it is set.
- `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-06T02:20:00Z (Run 353)

## Run 353 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. `tools/stall_watch.py` was not given a new flag. Do not add another upload-edge persist call. Do not add another export-probe lock. Do not add another media checker.
- The production job ran media QA and the export probe, then still called captions.insert on any present srt. An overlapping cue, a line over 42 characters, or a cue past the selected wav could reach the provider. `tools/caption_gate.py` now runs after media QA. A present bad cue fails the job. A missing srt fails only when execute=true. It does not rewrite captions and does not call YouTube.
- Local Q1 captions printed caption_gate PASS (103 cues). `python3 tools/caption_gate_contract.py` printed CAPTION GATE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-06T01:15:00Z (Run 352)

## Run 352 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. `tools/stall_watch.py` was not given a new flag. Do not add another upload-edge persist call. Do not add another export-probe lock.
- The production job materialized Q1 and then probed the master, but it never ran `tools/media_qa.py`. A bad take or a wrong-size card could still reach the upload gates. The workflow now runs media QA after materialize and before the export probe. It does not encode and does not call YouTube. Q1 must pass. A non-Q1 missing take fails the job only when execute=true.
- Local Q1 media from `q1-media-r253` and the r249 wav/cards printed media_qa gate PASS (308.4s wav, 7/7 cards, export ftyp). `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-06T00:20:00Z (Run 351)

## Run 351 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. `tools/stall_watch.py` printed `STALL_OAUTH_IDLE` only. The newest four deltas are no longer all upload-edge, so `STALL_UPLOAD_EDGE` did not print. The NEXT.md lock against another upload-session patch remains.
- `tools/export_probe.py` accepted the known truncated r249 master because 308s still cleared the 20s floor and the file is 1920x1080 h264 with audio. It now refuses that sha as `EXPORT_BANNED_MASTER` before ffprobe. A present master must also be 30fps yuv420p with stereo AAC at 48000 Hz. The r253 master probed PASS at 328.40s. The probe still does not encode and does not call YouTube.
- `python3 tools/export_probe_contract.py` printed EXPORT PROBE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T23:20:00Z (Run 350)

## Run 350 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `STALL_UPLOAD_EDGE` still stands. `playlist_id` remains `not_set`.
- An ftyp box was the only hard export check. A wrong-size or silent master could still reach videos.insert. `tools/export_probe.py` now requires 1920x1080, h264, an audio stream, and at least 20s before execute. Absent export fails execute only. The probe does not encode and does not call YouTube.
- `python3 tools/export_probe_contract.py` printed EXPORT PROBE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T22:35:00Z (Run 349)

## Run 349 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- Runs 344-348 each patched a resumable or early-persist edge while videos published stayed 0. That pattern is now `STALL_UPLOAD_EDGE`. Do not add another Location, session hold, or early-persist call while it is set.
- Caption, thumbnail, and comment status are early-persisted after each of those writes when `UPLOAD_EARLY_PERSIST=1`. A kill after `captions.insert` no longer loses the uploaded status. The URI is not printed. The later persist step still runs. This is the last early-persist call site for that stall.
- `python3 tools/selftest.py` printed SELFTEST PASS. `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T22:15:00Z (Run 348)

## Run 348 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- Run 347 pushed an open Location before the first chunk. A job kill during caption wait still happened after the video id existed and before the later persist step, so the next execute could see only the Location. If that Location then 404'd, the hold could hide a video that already existed. The uploader now early-persists the provider video id before caption wait, and early-persists a 404/410 hold and a completed-without-id hold before the step returns. The URI is not printed. The later persist step still runs.
- `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T21:15:00Z (Run 347)

## Run 347 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- An open Location was committed only after the execute step returned. A killed step never reached that persist, so the next execute could POST another videos.insert. `remember_session` now calls `early_persist_file` when `UPLOAD_EARLY_PERSIST=1`. The production execute step sets that env. The plan does not contain the URI. A git failure does not raise into the upload. The later persist step still runs.
- `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T20:15:00Z (Run 346)

## Run 346 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- A committed `session_expired_hold` used to be permanent. The next execute raises `RESUMABLE_SESSION_EXPIRED` and does not insert, which is correct until Studio is checked. `apply_session_hold_release` clears that hold only when `studio_checked` is `no_video_in_studio`, no video id exists, and no https Location remains. Persist commits `commit_session_hold_released`. The production workflow has no release input.
- `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T19:20:00Z (Run 345)

## Run 345 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- A committed Location that later returned 404 stayed in git because `RESUMABLE_SESSION_EXPIRED` was skip_transient. The next execute would query that dead URI forever, or a future change could start another videos.insert. A saved Location is probed first. 200 returns the video id. 308 resumes that offset. 404 or 410 raises the existing `RESUMABLE_SESSION_EXPIRED`, drops the URI, and sets `session_expired_hold`. Persist commits `commit_session_expired_hold`. The next execute raises the same reason and does not POST videos.insert.
- `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T19:20:00Z (Run 345)

## Run 344 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- An open resumable Location used to stay off git. A killed execute could start another videos.insert. `upload_video` now accepts a saved session URI and skips the session POST. `on_session` writes `resumable_session_uri` before the first chunk. Persist commits that row as `commit_resumable_session`. A fingerprint mismatch reuses `EXISTING_VIDEO_FINGERPRINT_MISMATCH`. The URI is not printed.
- `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T17:25:00Z (Run 343)

