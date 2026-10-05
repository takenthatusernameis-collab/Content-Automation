# NEXT

Updated: 2026-10-05T17:15:00Z (Run 342)

Active locks: do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets. `playlist_id` stays `not_set` until a human sets it. Materialize installs `q1-media-r253` only. Do not restore multipart for the master. Do not start a second `videos.insert` when Location exists.

Older do-not-rediscover notes live in `docs/next_archive.md`. Do not paste the archive back into this file. Do not restore a behavior named there.

1zr8. **Do not rediscover the truncated RUNS file.** Run 342: `RUNS.md` keeps 12 newest entries. Older entries live in `docs/runs_archive.md`. `tools/runs_compact.py` moves extras. It does not delete history. Do not paste the archive back. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr7. **Do not rediscover the truncated NEXT file.** Run 341: `NEXT.md` keeps 12 newest notes. Older notes live in `docs/next_archive.md`. `tools/next_compact.py` moves extras. It does not delete history. Do not paste the archive back. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr6. **Do not rediscover the truncated STATE file.** Run 340: `STATE.md` keeps 12 newest run deltas. Older deltas live in `docs/state_archive.md`. `tools/state_compact.py` moves extras. It does not delete history. Do not paste the archive back into `STATE.md`. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr5. **Do not rediscover the false local-gate stall.** Run 339: `No new scanner` is not a local gate. `tools/stall_watch.py` sets `STALL_LOCAL_GATE` only when a delta still names quality_scan, claim_scan, title_scan, content_rules, or packet_path after negation phrases are removed. Do not restore the bare `scanner` token. `STALL_OAUTH_IDLE` still stands. Do not add another scanner while it is set. Do not scaffold Q2.

1zr4. **Do not rediscover the unstamped feedback commit.** Run 338: `feedback_commit_decision` returns `skip_unstamped_window` unless `window.kind` is `first_calendar_days`, `days` is 7, and start/end dates are present. A missing kind or `sliding_now` stays uncommitted. A stamped file still commits. Date match against `uploaded_at` stays in `collected_metrics`. Do not restore commit-on-gate-only. Do not add a YouTubeAPIError reason for this. Do not add another scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr3. **Do not rediscover the unstamped collected window.** Run 337: `collected_metrics` returns no rows unless `window.kind` is `first_calendar_days` and the dates match `uploaded_at` through upload plus 6 days. Execute stamps that kind and ignores a report days field. A sliding or missing kind is not evidence. Do not restore a collected file with no kind as a comparison. Do not add a YouTubeAPIError reason for this. Do not add another scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr2. **Do not rediscover the sliding dry-run window.** Run 336: `inspect_feedback` `window` and `request_plan` start/end are the video's first 7 calendar days when `uploaded_at` exists. A missing upload time does not advertise a sliding now window. Collect is still due at upload plus 7 days plus 3 days of Analytics lag. Do not restore `observation_window(now)` as the query range. Do not add a YouTubeAPIError reason for this. Do not add another scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zr. **Do not rediscover the short analytics window.** Run 335: collect is due at upload plus 7 days plus 3 days of Analytics lag. The query is that video's first 7 calendar days, not a sliding now window. Day 8 stays `OBSERVATION_WINDOW_NOT_DUE`. Do not restore due-at-upload-plus-7 while the query still drops 3 days. Do not add a YouTubeAPIError reason for this. Do not add another scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zq. **Do not rediscover the silent playlist insert failure.** Run 334: `auth_required` and `not_added` with a detail exit 2 and write `playlist_plan.md`. `already_present` exits 0 and writes the plan. `playlist_id: not_set` and a missing video id still exit 0, write nothing, and do not call videos.insert. Do not add a YouTubeAPIError reason for this. Do not add another scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zp. **Do not rediscover the upload-only scope field.** Run 333: dry-run `scope` is the consent set (`youtube.upload youtube.force-ssl yt-analytics.readonly`), matching `required_scopes`. Do not restore `scope: youtube.upload` alone. The production job prints `tools/stall_watch.py` after checkout. The flag does not fail the job. Do not add another scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2.

1zo. **Do not rediscover the OAuth-idle window.** Run 332: a 3-run topic flag clears when the subject changes. `tools/stall_watch.py` prints `STALL_OAUTH_IDLE` when the last eight STATE deltas left OAuth unpolled and videos published at 0. The flag does not fail CI. Do not add another scanner, Studio sentence, or playlist variant while it is set. Do not spend the run only restating the missing secrets. `invalid_playlist_id` exits 2. `playlist_id: not_set` still exits 0 and does not invent a PL id. Do not scaffold Q2.

1zn. **Do not rediscover the playlist insert.** Run 331: `docs/channel.md` `playlist_id` is `not_set`. `tools/playlist_membership.py` skips and does not invent a PL id. A missing provider video id does not call playlistItems.insert and does not start videos.insert. The production job runs the tool after execute. Upload does not wait on this field. Do not scaffold Q2 to try it. Do not add a YouTubeAPIError reason for a missing playlist.
