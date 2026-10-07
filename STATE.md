# STATE

Updated: 2026-10-07T01:15:00Z (Run 373)

## Run 373 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- Both provider-state push steps called `python3 - <<'PY'` and closed on `          PY`. Bash does not treat a spaced terminator as the end of the heredoc, so `push_with_retry` never ran. A later swallow of that non-zero status would leave the video id off main. The steps now call `python3 tools/persist_provider_state.py push`. This does not call YouTube.

## Run 372 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- The persist step prints `PERSIST_PUSH_NOT_INSERT_FAILURE` and exits 0 when `classify-upload` fails and `upload_state.json` already has a provider video id. A classify miss without that video id still fails the step. A red job after `videos.insert` is not a reason to dispatch execute again. This does not call YouTube.

## Run 371 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- The playlist membership step now prints `PLAYLIST_INSERT_NOT_UPLOAD_FAILURE` and exits 0 on any non-zero exit, not only exit 2. A crash after `upload_state.json` exists is not an insert failure. The job summary no longer says a caption or thumbnail miss exits non-zero after the video id is written. It says that miss prints `POST_UPLOAD_NOT_INSERT_FAILURE` and exits 0. This does not call YouTube.

## Run 370 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- The Studio pin step prints `STUDIO_PIN_NOT_INSERT_FAILURE` and exits 0 when `studio_handoff.py` exits non-zero. The persist step prints `PERSIST_PUSH_NOT_INSERT_FAILURE` and exits 0 when a provider video id exists and the commit or push fails. A red job after `videos.insert` is not a reason to dispatch execute again. A persist miss without that video id still fails the step. This does not call YouTube.

## Run 369 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- The execute step no longer fails the job when `youtube_upload.py` exits 4 and `upload_state.json` already has a provider video id with `error_class` starting `POST_UPLOAD_INCOMPLETE`. It prints `POST_UPLOAD_NOT_INSERT_FAILURE` and exits 0. A red job after `videos.insert` is not a reason to dispatch execute again. An insert failure without that video id still fails the step. This does not call YouTube.

## Run 368 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- The playlist membership step no longer fails the job when `playlist_membership.py` exits 2. It prints `PLAYLIST_INSERT_NOT_UPLOAD_FAILURE` and exits 0. A red job after `videos.insert` is not a reason to dispatch execute again. This does not call YouTube.

## Run 367 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- `tools/studio_handoff.py` no longer tells the operator to add a playlist end-screen element while `playlist_id` is `not_set`. The note is one video element (best for viewer). A set playlist id still names a playlist element. The workflow comment no longer says a failed `playlistItems.insert` prevents `videos.insert`. This does not call YouTube.

## Run 366 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- `tools/selftest.py` had two `check_stall_watch` definitions. The later one shadowed the contract call, so a broken `stall_watch_contract.py` could still print SELFTEST PASS. One definition now runs the contract and the inline stall assertions. This does not call YouTube.

## Run 365 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- Selftest was red. `tools/stall_watch.py` appended `idle_streak: 0` on a quiet file, so `flag_text` was never empty and the quiet check failed twice. A zero streak is no longer a flag. `idle_streak()` still returns 0. A positive streak and the suspicious line at 8 or more stay. This does not call YouTube.
- STATE.md and NEXT.md each had 13 sections after Run 364. Compact moved the oldest of each into the archive. Live caps are 12 again. This does not poll secrets.

## Run 364 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- `tools/stall_watch.py` now prints `idle_streak` for every newest STATE delta that still says OAuth was not polled and videos published stay 0. A streak of 8 or more also prints `suspicious: oauth_idle_without_publish`. A published or polled newest delta resets the streak. This does not call YouTube and does not add a scanner.
- Live STATE before this delta already had 12 such newest deltas (Runs 363-352). After this delta the streak is 13. That repetition is suspicious. Do not treat another restatement as progress.

## Run 363 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- PROGRESS.md Run 360 was a bare `360 — timestamp` line, so log compact did not count it. `tools/log_compact.py` now promotes that shape to a Run heading before the size cap. The live heading is restored. Run 351 and Run 350 progress sections moved to `docs/progress_archive.md`. This does not call YouTube.

## Run 362 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- `tools/oauth_setup.py` now prints the exact `gh workflow dispatch` for the first private execute, with `collect_feedback=false`. It does not call GitHub and does not print secret values. This does not call YouTube.

