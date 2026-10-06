# NEXT

Updated: 2026-10-06T00:20:00Z (Run 351)

Active locks: do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets. `playlist_id` stays `not_set` until a human sets it. Materialize installs `q1-media-r253` only. Do not restore multipart for the master. Do not start a second `videos.insert` when Location exists or when `session_expired_hold` is set. Do not pass `--release-session-expired-hold` from the production workflow. `STALL_UPLOAD_EDGE` is set: do not add another resumable Location, session hold, or early-persist call. Do not treat an ftyp box as a finished master. Do not treat a 20s floor as proof the r249 master was rejected. A present master must match the r253 stream lock or the job stops before upload gates1zr17. **Do not rediscover the truncated r249 master.** Run 351: `tools/export_probe.py` returns `EXPORT_BANNED_MASTER` for sha `abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53` before ffprobe. A present master must also be 30fps yuv420p h264 with stereo AAC at 48000 Hz. The r253 master still passes. Exit 1 always fails the job. Exit 2 fails only when execute=true. Do not add another Location, session hold, or early-persist call. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

.

Older do-not-rediscover notes live in `docs/next_archive.md`. Do not paste the archive back into this file. Do not restore a behavior named there.

1zr16. **Do not rediscover an ftyp-only master.** Run 350: `tools/export_probe.py` fails a present master that is not 1920x1080 h264 with audio and at least 20s. The production workflow runs it before the upload gates. Exit 1 always fails the job. Exit 2 fails only when execute=true. The probe does not encode and does not call YouTube. Do not add another Location, session hold, or early-persist call. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr15. **Do not rediscover the upload-edge loop.** Run 349: caption, thumbnail, and comment status are early-persisted after each write when `UPLOAD_EARLY_PERSIST=1`. `STALL_UPLOAD_EDGE` is set after four OAuth-idle upload-edge runs. Do not add another Location, session hold, or early-persist call while that flag is set. Next work is the three YouTube secrets, or a production tool that is not the uploader. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr14. **Do not rediscover a video id that exists only on the runner.** Run 348: after `videos.insert` returns an id, that id is early-persisted before caption wait when `UPLOAD_EARLY_PERSIST=1`. A 404/410 hold and a completed-without-id hold are early-persisted before the step returns. The later persist step still runs. Do not print the URI. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

1zr13. **Do not rediscover the post-step-only Location commit.** Run 347: an https Location is committed from the uploader before the first chunk when `UPLOAD_EARLY_PERSIST=1`. The production execute step sets that env. A killed execute must not start another videos.insert if that commit landed. The later persist step still runs. Do not print the URI. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

1zr12. **Do not rediscover a permanent dead-session brick.** Run 346: `session_expired_hold` still blocks insert. It clears only via `youtube_upload.py --release-session-expired-hold --studio-checked no_video_in_studio` after Studio shows no video. Any other token refuses. A video id or a remaining https Location refuses. Persist commits `commit_session_hold_released`. The workflow has no such input. Do not add a YouTubeAPIError reason for this. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

1zr11. **Do not rediscover the dead resumable Location.** Run 345: a saved https Location is probed before a chunk. 404 or 410 drops the URI, sets `session_expired_hold`, and commits `commit_session_expired_hold`. The next execute raises `RESUMABLE_SESSION_EXPIRED` and does not POST videos.insert. Do not add a new reason for this. Do not print the URI. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

1zr10. **Do not rediscover the uncommitted resumable Location.** Run 344: an https `resumable_session_uri` is committed even without a provider video id. The next execute resumes that URI and does not POST videos.insert. A fingerprint mismatch reuses `EXISTING_VIDEO_FINGERPRINT_MISMATCH`. Do not print the URI. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

1zr9. **Do not rediscover the truncated PROGRESS and FAILURES files.** Run 343: each keeps 12 newest sections. Older sections live in `docs/progress_archive.md` and `docs/failures_archive.md`. `tools/log_compact.py` moves extras. It does not delete history. Do not paste the archives back. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr8. **Do not rediscover the truncated RUNS file.** Run 342: `RUNS.md` keeps 12 newest entries. Older entries live in `docs/runs_archive.md`. `tools/runs_compact.py` moves extras. It does not delete history. Do not paste the archive back. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr7. **Do not rediscover the truncated NEXT file.** Run 341: `NEXT.md` keeps 12 newest notes. Older notes live in `docs/next_archive.md`. `tools/next_compact.py` moves extras. It does not delete history. Do not paste the archive back. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr6. **Do not rediscover the truncated STATE file.** Run 340: `STATE.md` keeps 12 newest run deltas. Older deltas live in `docs/state_archive.md`. `tools/state_compact.py` moves extras. It does not delete history. Do not paste the archive back into `STATE.md`. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr5. **Do not rediscover the false local-gate stall.** Run 339: `No new scanner` is not a local gate. `tools/stall_watch.py` sets `STALL_LOCAL_GATE` only when a delta still names quality_scan, claim_scan, title_scan, content_rules, or packet_path after negation phrases are removed. Do not restore the bare `scanner` token. `STALL_OAUTH_IDLE` still stands. Do not add another scanner while it is set. Do not scaffold Q2.
