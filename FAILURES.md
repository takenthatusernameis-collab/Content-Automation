# FAILURES

Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.

## Run 354 — 2026-10-06T03:20:00Z
- Failed approach not retried: another export-probe lock, media checker, or caption cue gate while videos published stay 0.
- Lesson: Runs 350-353 each wired a pre-upload checker and published nothing. `STALL_PREUPLOAD_PROBE` is the stop. The unpublished video is the missing OAuth secrets.

## Run 353 — 2026-10-06T02:20:00Z
- Failed approach not retried: another export-probe lock or another media checker while videos published stay 0.
- Lesson: media QA and the export probe never read captions.srt. Wire the cue check. Do not invent a second media checker.

## Run 352 — 2026-10-06T01:15:00Z
- Failed approach not retried: another export-probe lock or upload-edge persist branch while videos published stay 0.
- Lesson: the job materialized media and then only probed the master. VO levels and card size already had a fail-closed tool. Wire that tool. Do not invent a second media checker.

## Run 350 — 2026-10-05T23:20:00Z
- Failed approach not retried: another upload-edge persist branch while videos published stay 0. `STALL_UPLOAD_EDGE` still stands.
- Lesson: the remaining pre-insert hole was the master itself. ftyp-only acceptance could still upload the wrong picture size or a silent file. Probe streams before execute. Do not encode in that step.

# FAILURES

Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.

## Run 349 — 2026-10-05T22:35:00Z
- Failed approach not retried: another upload-edge branch as the run objective while videos published stay 0. Runs 344-348 did that. Caption status early-persist closes the last kill hole in that chain.
- Lesson: `STALL_UPLOAD_EDGE` means stop. Do not add another Location, session hold, or early-persist call. The unpublished video is the missing OAuth secrets.

## Run 348 — 2026-10-05T22:15:00Z
- Failed approach not retried: treating the Location commit as enough once videos.insert has returned an id. Caption wait is long enough for a job kill. The id must be pushed before that wait.
- Lesson: early persist must cover every durable row that would otherwise exist only on the runner. Do not print the URI.

# LOG

Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.

## Run 347 — post-step Location commit
- What failed: Run 344 wrote the resumable Location on the runner and committed it only after the execute step returned. A killed or timed-out step never reached Persist non-secret upload state.
- Why: `always()` does not run when the job itself is cancelled. The next execute could POST videos.insert again.
- Do not: wait for the later persist step to be the only commit of an open Location. Do not print the URI.

# LOG

Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.

## Run 346 — dead-session hold had no recovery
- **Tried:** Leaving `session_expired_hold` as a permanent execute refusal after Run 345.
- **Evidence:** `execute_upload` raises `RESUMABLE_SESSION_EXPIRED` when the hold is set and there is no video id. No tool cleared it. Selftest now refuses a release without `no_video_in_studio`, with a video id, or with a remaining Location.
- **Result:** Release is local and committed. Production workflow has no release input. No provider write.
- **Avoid:** Passing `--release-session-expired-hold` from Actions. Releasing without the Studio token. Adding another scanner while `STALL_OAUTH_IDLE` is set. Polling OAuth secrets as the only work.

# FAILURES

Updated: 2026-10-05T18:20:00Z

Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.

## Run 345 — expired Location stayed committed as open
- **Tried:** Run 344 committed the Location. An expired session was still `skip_transient`, so the dead URI remained the next execute target.
- **Result:** Probe a saved Location. 404 or 410 sets `session_expired_hold`, drops the URI, and commits that hold. No new YouTubeAPIError reason. No provider write.
- **Do not retry:** Do not treat `RESUMABLE_SESSION_EXPIRED` with `session_expired_hold` as skip_transient. Do not POST videos.insert to replace a dead Location automatically.

## Run 344 — open Location was not durable
- **Tried:** Runs 340-343 each compacted a fetch file. That pattern is now suspicious if it continues with no production-path change. The upload path still dropped a Location that was not committed.
- **Result:** Persist now commits `commit_resumable_session` for an https session URI. A saved URI skips the session POST. No live execute. No new YouTubeAPIError reason.
- **Avoid:** Another compaction-only run while this URI rule is already locked. Printing the session URI. Starting a second videos.insert when Location exists. Adding a scanner while `STALL_OAUTH_IDLE` is set.

# FAILURES

Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.

## Run 343 — truncated PROGRESS and FAILURES hid older lessons

- **Tried:** Reading PROGRESS.md and FAILURES.md as the cumulative lesson log. They were 27269 and 30708 bytes.
- **Evidence:** After the move, each live file has 12 sections. Archives hold the older notes.
- **Result:** tools/log_compact.py keeps the cap. No provider write.
- **Avoid:** Pasting the archives back. Adding another scanner while STALL_OAUTH_IDLE is set. Polling OAuth secrets as the only work.

## Run 342 — truncated RUNS hid the newest action

- **Tried:** Reading RUNS.md as the permanent run log. The file was 108696 bytes and 71 entries. The fetch truncated before the newest recommended next action.
- **Evidence:** After the move, RUNS.md has 12 entries and the permanent footer. docs/runs_archive.md holds the older entries, including Run 270.
- **Result:** tools/runs_compact.py keeps the cap. No provider write.
- **Avoid:** Pasting the archive back into RUNS.md. Adding another scanner while STALL_OAUTH_IDLE is set. Polling OAuth secrets as the only work.

