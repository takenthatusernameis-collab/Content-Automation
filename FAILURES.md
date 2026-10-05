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

## Run 340 — truncated STATE hid the current gate

- **Tried:** Reading STATE.md as the current system state. The file was 52418 bytes. The fetch truncated before the publish-gate section.
- **Evidence:** 67 `## Run ` sections. Stall watch only needs the newest 8. After the move, STATE.md has 12 sections and stall_watch still prints STALL_OAUTH_IDLE.
- **Result:** Older deltas are in docs/state_archive.md. tools/state_compact.py keeps the cap. No provider write.
- **Avoid:** Pasting the archive back into STATE.md. Adding another scanner while STALL_OAUTH_IDLE is set. Polling OAuth secrets as the only work.

## Run 339 — boilerplate kept the local-gate flag set

- **Tried:** Treating `STALL_LOCAL_GATE` as still true because the printer said so after Runs 336-338.
- **Evidence:** Those deltas said `No new scanner`. `LOCAL_GATE_TOKENS` included `scanner`, so the negation matched. After the token was removed, `tools/stall_watch.py` printed `STALL_OAUTH_IDLE` only.
- **Result:** Contract locks the negated case. A real scan token still sets the flag. No provider write.
- **Avoid:** Restoring the bare `scanner` token. Adding another scanner while `STALL_OAUTH_IDLE` is set. Polling OAuth secrets as the only work.

## Run 335 — day-7 collect was not a 7-day observation

- **Tried:** The feedback gate treated upload plus 7 days as due, while the Analytics query ended 3 days before now.
- **Evidence:** At the earliest allowed collect, the fetched end date was about 4 days after upload, and the start date was a sliding now window rather than the video's first day.
- **Result:** Due time is upload plus 10 days. Query dates are the first 7 calendar days of that video. Day 8 stays not due. No metrics were invented.
- **Avoid:** Restoring a 7-day due gate while the query still holds back 3 days. Treating a sliding now window as the first-video comparison.

## Run 333 — dry-run scope field still said upload-only
Run 330 added `required_scopes` and a warning line, but `auth_status` and the request body still set `scope` to `youtube.upload` alone. An operator copying that field would mint a token that can insert a video and then fail captions.insert. Fixed by joining the consent set into `scope`. Do not restore the single-scope field. Do not treat this as a new YouTubeAPIError.

## Run 332 — 3-run stall window reset
The Studio, instruction, and local-gate flags only look at the last three deltas and require the same topic tokens. Runs 330-331 changed subject, so `stall_watch.py` printed clear while publish was still the missing secrets. Do not treat `status: clear` as evidence the idle loop ended. The 8-run `STALL_OAUTH_IDLE` flag is the counter for that reset.

## Run 329 — local scanners did not move the publish gate
- **Tried:** Runs 326-328 each added a scan or content-rule refusal (claim, title, upload content_rules). Q1 was already clear. Videos published stayed 0.
- **Evidence:** Each STATE delta says OAuth secrets were not polled and no provider write. `stall_watch.py` stayed clear because the edits were not Studio copy and not paste/hint sentences.
- **Result:** `STALL_LOCAL_GATE` now prints for that window. Selftest still passes. No provider write.
- **Avoid:** Another scanner, packet path gate, or content-rule refusal while that flag is set. Polling OAuth secrets as the only work. Scaffolding Q2 to try the flag.

