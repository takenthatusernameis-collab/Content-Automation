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

## Run 343 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- PROGRESS.md was 27269 bytes. FAILURES.md was 30708 bytes. Both were past the NEXT truncation size. Newest 12 sections stay live. Older sections moved to `docs/progress_archive.md` and `docs/failures_archive.md`. `tools/log_compact.py` moves extras. It does not delete history.
- `python3 tools/log_compact_contract.py` printed LOG COMPACT CONTRACT PASS. Selftest includes the contract. Actions was not re-run.

# STATE

Updated: 2026-10-05T17:15:00Z (Run 342)

## Run 342 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- RUNS.md was 108696 bytes and 71 entries. A fetch truncated it before the newest recommended next action. Newest 12 entries stay in RUNS.md. Older entries moved to `docs/runs_archive.md`. `tools/runs_compact.py` moves extras. It does not delete history.
- `python3 tools/runs_compact_contract.py` printed RUNS COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T16:20:00Z (Run 341)

## Run 341 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- NEXT.md was 28596 bytes. A fetch truncated it before the older upload locks. Newest 12 notes stay in NEXT.md. Older notes moved to `docs/next_archive.md`. `tools/next_compact.py` moves extras. It does not delete history.
- `python3 tools/next_compact_contract.py` printed NEXT COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T15:20:00Z (Run 340)

## Run 340 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- STATE.md had 67 run deltas and 52418 bytes. A fetch of this file truncated before the publish-gate section. Newest 12 deltas stay here. Older deltas moved to `docs/state_archive.md`. `tools/state_compact.py` moves extras there and keeps 12. It does not refuse the file.
- `python3 tools/state_compact_contract.py` printed STATE COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

## Run 339 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new packet folder. Q1 was not rewritten.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- `STALL_LOCAL_GATE` was a false positive. The token `scanner` matched the boilerplate `No new scanner` in Runs 336-338, so the flag stayed set after the subject had already left local gates. `tools/stall_watch.py` no longer treats that phrase as a local gate. A real quality_scan, claim_scan, title_scan, content_rules, or packet_path delta still sets the flag.
- `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. `python3 tools/stall_watch.py` printed STALL_OAUTH_IDLE and did not print STALL_LOCAL_GATE. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T12:30:00Z (Run 338)

## Run 338 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- Run 337 refused an unstamped COLLECTED file as a comparison, but `feedback_commit_decision` still returned `commit_collected` for that file. Persist now returns `skip_unstamped_window` unless `window.kind` is `first_calendar_days`, `days` is 7, and start/end dates are present. A stamped file still commits. No fetch was run.
- `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T11:20:00Z (Run 337)

## Run 337 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- A COLLECTED feedback file with no window kind, or kind sliding_now, used to count as the 7-day observation. `collected_metrics` now refuses those files. Execute stamps `kind: first_calendar_days` and queries `DEFAULT_WINDOW_DAYS` from `uploaded_at`, not a report days field. No fetch was run.
- `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T10:20:00Z (Run 336)

## Run 336 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- Run 335 due-gate was correct, but dry-run `window` and `request_plan` still used a sliding now window. `inspect_feedback` now sets `window` from the video's first 7 calendar days when `uploaded_at` exists. A missing upload time leaves start and end empty (`kind: unavailable`). `request_plan` uses those dates. The live fetch still uses `analytics_range`. No fetch was run.
- `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T09:11:00Z (Run 335)

## Run 335 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- A collect at upload+7 days used to query a sliding window ending 3 days ago, so the first comparison was short and not the video's first 7 days. `tools/youtube_feedback.py` now marks the window due at upload plus 7 days plus 3 days of Analytics lag, and the query dates are that video's first 7 calendar days. Day 8 stays `OBSERVATION_WINDOW_NOT_DUE`. No fetch was run.
- `check_feedback_fail_closed` passed. Full selftest was not re-run.

# STATE

Updated: 2026-10-05T08:17:14Z (Run 334)

## Run 334 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`.
- A failed `playlistItems.insert` used to exit 0 and write no plan, so a later run could treat membership as done. `tools/playlist_membership.py` now exits 2 on `auth_required` and on `not_added` with a detail, and writes `playlist_plan.md` for that failure and for `already_present`. `not_set` and a missing video id still exit 0, write no plan, and do not call videos.insert.
- `python3 tools/playlist_membership_contract.py` printed PLAYLIST MEMBERSHIP CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-05T10:30:00Z (Run 333)

