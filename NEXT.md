# NEXT

Updated: 2026-10-05T20:15:00Z (Run 346)

Active locks: do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets. `playlist_id` stays `not_set` until a human sets it. Materialize installs `q1-media-r253` only. Do not restore multipart for the master. Do not start a second `videos.insert` when Location exists or when `session_expired_hold` is set. Do not pass `--release-session-expired-hold` from the production workflow.

Older do-not-rediscover notes live in `docs/next_archive.md`. Do not paste the archive back into this file. Do not restore a behavior named there.

1zr12. **Do not rediscover a permanent dead-session brick.** Run 346: `session_expired_hold` still blocks insert. It clears only via `youtube_upload.py --release-session-expired-hold --studio-checked no_video_in_studio` after Studio shows no video. Any other token refuses. A video id or a remaining https Location refuses. Persist commits `commit_session_hold_released`. The workflow has no such input. Do not add a YouTubeAPIError reason for this. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

1zr11. **Do not rediscover the dead resumable Location.** Run 345: a saved https Location is probed before a chunk. 404 or 410 drops the URI, sets `session_expired_hold`, and commits `commit_session_expired_hold`. The next execute raises `RESUMABLE_SESSION_EXPIRED` and does not POST videos.insert. Do not add a new reason for this. Do not print the URI. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

1zr10. **Do not rediscover the uncommitted resumable Location.** Run 344: an https `resumable_session_uri` is committed even without a provider video id. The next execute resumes that URI and does not POST videos.insert. A fingerprint mismatch reuses `EXISTING_VIDEO_FINGERPRINT_MISMATCH`. Do not print the URI. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

1zr9. **Do not rediscover the truncated PROGRESS and FAILURES files.** Run 343: each keeps 12 newest sections. Older sections live in `docs/progress_archive.md` and `docs/failures_archive.md`. `tools/log_compact.py` moves extras. It does not delete history. Do not paste the archives back. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr8. **Do not rediscover the truncated RUNS file.** Run 342: `RUNS.md` keeps 12 newest entries. Older entries live in `docs/runs_archive.md`. `tools/runs_compact.py` moves extras. It does not delete history. Do not paste the archive back. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr7. **Do not rediscover the truncated NEXT file.** Run 341: `NEXT.md` keeps 12 newest notes. Older notes live in `docs/next_archive.md`. `tools/next_compact.py` moves extras. It does not delete history. Do not paste the archive back. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr6. **Do not rediscover the truncated STATE file.** Run 340: `STATE.md` keeps 12 newest run deltas. Older deltas live in `docs/state_archive.md`. `tools/state_compact.py` moves extras. It does not delete history. Do not paste the archive back into `STATE.md`. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr5. **Do not rediscover the false local-gate stall.** Run 339: `No new scanner` is not a local gate. `tools/stall_watch.py` sets `STALL_LOCAL_GATE` only when a delta still names quality_scan, claim_scan, title_scan, content_rules, or packet_path after negation phrases are removed. Do not restore the bare `scanner` token. `STALL_OAUTH_IDLE` still stands. Do not add another scanner while it is set. Do not scaffold Q2.

1zr4. **Do not rediscover the unstamped feedback commit.** Run 338: `feedback_commit_decision` returns `skip_unstamped_window` unless `window.kind` is `first_calendar_days`, `days` is 7, and start/end dates are present. A missing kind or `sliding_now` stays uncommitted. A stamped file still commits. Date match against `uploaded_at` stays in `collected_metrics`. Do not restore commit-on-gate-only. Do not add a YouTubeAPIError reason for this. Do not add another scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr3. **Do not rediscover the unstamped collected window.** Run 337: `collected_metrics` returns no rows unless `window.kind` is `first_calendar_days` and the dates match `uploaded_at` through upload plus 6 days. Execute stamps that kind and ignores a report days field. A sliding or missing kind is not evidence. Do not restore a collected file with no kind as a comparison. Do not add a YouTubeAPIError reason for this. Do not add another scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr2. **Do not rediscover the sliding dry-run window.** Run 336: `inspect_feedback` `window` and `request_plan` start/end are the video's first 7 calendar days when `uploaded_at` exists. A missing upload time does not advertise a sliding now window. Collect is still due at upload plus 7 days plus 3 days of Analytics lag. Do not restore `observation_window(now)` as the query range. Do not add a YouTubeAPIError reason for this. Do not add another scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr. **Do not rediscover the short analytics window.** Run 335: collect is due at upload plus 7 days plus 3 days of Analytics lag. The query is that video's first 7 calendar days, not a sliding now window. Day 8 stays `OBSERVATION_WINDOW_NOT_DUE`. Do not restore due-at-upload-plus-7 while the query still drops 3 days. Do not add a YouTubeAPIError reason for this. Do not add another scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.
