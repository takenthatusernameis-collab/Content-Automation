# RUNS

Older runs live in `docs/runs_archive.md`. Do not paste the archive back. `tools/runs_compact.py` moves extras. It does not delete history.

## Run 353 — 2026-10-06T02:20:00Z
- Objective: Stop a bad captions.srt from reaching captions.insert after media QA.
- Action: Production workflow now runs `tools/caption_gate.py` after media QA and before the export probe. A present empty, overlapping, reversed, overlong, or past-wav cue fails the job. A missing srt fails only when execute=true. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add an upload-edge persist call. Did not add an export-probe lock. Did not add another media checker.
- Result: Local Q1 captions printed caption_gate PASS (103 cues). Contract passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/caption_gate.py` on the Q1 packet printed PASS. `python3 tools/caption_gate_contract.py` printed CAPTION GATE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: media QA and the export probe never read captions.srt. The file is committed and the dry-run only checked that it exists.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: pre-upload probe patches have not published a video. Do not add another export-probe lock or another media checker.
- Next: Do not install the r249 master. Do not add another Location, session hold, or early-persist call. Do not add another export-probe lock. Do not add another media checker. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 352 — 2026-10-06T01:15:00Z
- Objective: Stop a bad take or wrong-size card from reaching the upload gates after materialize.
- Action: Production workflow now runs `tools/media_qa.py` after materialize and before the export probe. Q1 must pass. A non-Q1 missing take fails only when execute=true. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add an upload-edge persist call. Did not add an export-probe lock.
- Result: Local Q1 media printed media_qa gate PASS. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/media_qa.py` on the r253 master plus r249 wav/cards printed gate PASS (308.4s, 7/7 cards, export ftyp). `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: The job probed the master and never checked VO levels or card size. Those checks already existed and passed on the release files.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: upload-edge and export-probe patches have not published a video. Do not add another one.
- Next: Do not install the r249 master. Do not add another Location, session hold, or early-persist call. Do not add another export-probe lock. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 351 — 2026-10-06T00:20:00Z
- Objective: Stop the known truncated r249 master, and an off-rate or silent-codec master, from passing the production export probe.
- Action: `tools/export_probe.py` now returns EXPORT_BANNED_MASTER for the r249 master sha before ffprobe. A present master must be 30fps yuv420p h264 with stereo AAC at 48000 Hz, still 1920x1080 and at least 20s. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add an upload-edge persist call.
- Result: Export probe contract passed. Selftest passed. The r253 master probed PASS at 328.40s. Videos published stay 0. No live execute.
- Verification: `python3 tools/export_probe_contract.py` printed EXPORT PROBE CONTRACT PASS. `python3 tools/export_probe.py` on the r253 file printed PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 350's 20s floor still accepted the 308.40s truncated master. The stream lock matches the only approved master and the format note in docs/format.md.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: upload-edge fixes have not published a video. Do not add another one.
- Next: Do not install the r249 master. Do not add another Location, session hold, or early-persist call. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 350 — 2026-10-05T23:20:00Z
- Objective: Stop a wrong-size or silent master from reaching videos.insert once OAuth exists.
- Action: Added tools/export_probe.py. It requires 1920x1080, h264, an audio stream, and at least 20s when export/master.mp4 is present. The production workflow runs it before upload gates. Exit 1 fails the job. Exit 2 fails only on execute. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add an upload-edge persist call.
- Result: Export probe contract passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/export_probe_contract.py` printed EXPORT PROBE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: media_qa still refuses to run ffmpeg and only hard-fails a missing ftyp box. That was not enough to reject a wrong geometry before the first insert.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: upload-edge fixes have not published a video. Do not add another one.
- Next: Do not add another Location, session hold, or early-persist call. Do not treat ftyp as a finished master. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 349 — 2026-10-05T22:35:00Z
- Objective: Stop a kill after captions.insert from retrying captions, and flag the upload-edge loop.
- Action: Early-persist caption, thumbnail, and comment status after each write when UPLOAD_EARLY_PERSIST=1. stall_watch now sets STALL_UPLOAD_EDGE after four OAuth-idle upload-edge deltas. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a YouTubeAPIError reason.
- Result: Selftest passed. Stall contract passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. Actions not re-run. No provider write.
- Discovery: Runs 344-348 each added a resumable or early-persist branch while OAuth stayed absent. That is the credential stall. Caption status was the remaining kill hole in that chain, and it is now the last early-persist call site while the flag is set.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: upload-edge fixes have not published a video. Do not add another one.
- Next: Do not add another Location, session hold, or early-persist call. Do not add a scanner. Do not scaffold Q2. Do not poll secrets. Wait for the three YouTube secrets, or fix a production tool that is not the uploader.

## Run 348 — 2026-10-05T22:15:00Z
- Objective: Stop a job kill during caption wait from losing the provider video id.
- Action: Early-persist the provider video id before caption wait when UPLOAD_EARLY_PERSIST=1. Early-persist a 404/410 hold and a completed-without-id hold before those exceptions leave the step. Selftest locks the extra calls and that early persist pushes. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a YouTubeAPIError reason.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 347 pushed the Location only. Caption wait can outlive the job. A later 404 on that Location would set session_expired_hold with no video id even if the upload had already completed.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Ten-plus runs of upload-edge fixes have not published; that idle is the known credential stall, not a missing scanner.
- Next: Do not print the session URI. Do not start a second videos.insert when a video id or Location exists or when session_expired_hold is set. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 347 — 2026-10-05T21:15:00Z
- Objective: Stop a killed execute from losing the open Location and starting a second videos.insert.
- Action: Persist an open resumable session from the uploader before the first chunk when UPLOAD_EARLY_PERSIST=1. The production execute step sets that env. The plan does not contain the URI. A git failure does not raise into the upload. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a YouTubeAPIError reason.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 344 committed the Location only after the execute step returned. A timeout or runner kill skipped that step, so the next execute could POST videos.insert again.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Nine-plus runs of upload-edge fixes have not published; that idle is the known credential stall, not a missing scanner.
- Next: Do not print the session URI. Do not start a second videos.insert when Location exists or when session_expired_hold is set. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 346 — 2026-10-05T20:15:00Z
- Objective: Stop a committed dead-session hold from bricking the first upload after Studio shows no video.
- Action: Added a local release that clears `session_expired_hold` only with studio token `no_video_in_studio`, no provider video id, and no remaining Location. Persist commits that release. The production workflow does not pass the flag. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a YouTubeAPIError reason.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 345 fail-closed on 404/410, but nothing could clear the hold, so the first expired session would block every later execute even after a human checked Studio.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Eight-plus runs of upload-edge fixes have not published; that idle is the known credential stall, not a missing scanner.
- Next: Do not pass the release flag from Actions. Do not release without the Studio token. Do not start a second videos.insert when Location exists or when session_expired_hold is set. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 345 — 2026-10-05T19:20:00Z
- Objective: Stop a dead resumable Location from being reused forever or turning into a second videos.insert.
- Action: Probe a saved session URI before any chunk. A 404 or 410 drops the URI, sets session_expired_hold, and commits that hold. The next execute raises RESUMABLE_SESSION_EXPIRED and does not POST videos.insert. Did not add a reason. Did not poll secrets. Did not add a scanner. Did not scaffold Q2.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 344 committed the Location, but an expired session was skip_transient, so the dead URI stayed the next execute target.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not start a second videos.insert when Location exists or when session_expired_hold is set. Do not print the URI. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 344 — 2026-10-05T18:20:00Z
- Objective: Stop a killed execute from starting a second videos.insert after Location exists.
- Action: Saved the resumable session URI into upload_state.json and committed that row. The next execute resumes that URI and does not POST videos.insert. Fingerprint mismatch reuses the existing mismatch reason. Did not poll secrets. Did not add a scanner. Did not scaffold Q2.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Runs 340-343 only compacted fetch files. The open Location was still not durable, so the first real upload could duplicate if the runner died after the session POST.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not print the session URI. Do not start a second videos.insert when Location exists. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 343 — 2026-10-05T17:25:00Z
- Objective: Stop PROGRESS.md and FAILURES.md from truncating before the newest lesson on the next agent fetch.
- Action: Moved sections older than the newest 12 to docs/progress_archive.md and docs/failures_archive.md. Added tools/log_compact.py and a contract. Selftest runs the contract. Did not poll secrets. Did not add a scanner. Did not scaffold Q2.
- Result: Both live files are 12 sections. Archives hold the older notes. Videos published stay 0.
- Verification: log_compact_contract printed LOG COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: PROGRESS.md was 27269 bytes and FAILURES.md was 30708 bytes. NEXT.md truncated near 28KB, so both were already past the known fetch cut.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not paste the archives back. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 342 — 2026-10-05T17:15:00Z
- Objective: Stop RUNS.md from truncating before the newest run log on the next agent fetch.
- Action: Moved entries older than the newest 12 from RUNS.md to docs/runs_archive.md. Added tools/runs_compact.py and a contract. Selftest runs the contract. Did not poll secrets. Did not add a scanner. Did not scaffold Q2.
- Result: RUNS.md keeps 12 entries plus the permanent footer. Archive holds the older entries, including Run 270. Videos published stay 0.
- Verification: runs_compact_contract printed RUNS COMPACT CONTRACT PASS. python3 tools/selftest.py printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: RUNS.md was 108696 bytes and 71 entries. The agent fetch cut the newest section before the recommended next action.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not paste the archive back into RUNS.md. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.
Earlier runs through Run 269 remain in git at `9416aae2c482ca08fd55642e0fff94568482ee51` (`RUNS.md` blob `243e47753b76bbd636a59dddb00e8c1c6f2e90c1`) and before that at `65cca063`.
