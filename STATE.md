# STATE

Updated: 2026-10-07T09:13:00Z (Run 381)

## Run 381 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call. No new recovery edge.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- Four consecutive provider-state recovery deltas now set `STALL_RECOVERY_EDGE` and `suspicious: recovery_edge_without_publish`. A lock sentence such as "no new recovery edge" does not set the flag. The newest deltas are log-cap work, so the flag is clear on this commit. This does not call YouTube.


Updated: 2026-10-07T08:11:00Z (Run 380)

## Run 380 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call. No new recovery edge.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- Live-log overflow is now one command. `python3 tools/compact_all.py` runs the four compact tools and exits non-zero if STATE, NEXT, RUNS, PROGRESS, or FAILURES is still over cap. Selftest calls `compact_all.py --check` and does not write. A local selftest before a prepend is not a green push.

Updated: 2026-10-07T07:16:00Z (Run 379)

## Run 379 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- Run 378 claimed a local selftest pass and left STATE.md and NEXT.md at 13 sections. Actions run 37580716646 failed: `STATE.md has 13 run sections, max 12` and `NEXT.md has 13 notes, max 12`. This run only ran the existing compact tools. A red selftest is not a reason to add another recovery edge.

## Run 378 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- A rejected-push recovery no longer keeps the newest `provider-upload-state` artifact. `persist_provider_state.py recover` skips a downloaded `upload_state.json` that has no `provider_video_id` and continues through the last 20 production runs. A later failed execute must not hide an older insert. This does not call YouTube or GitHub.

Updated: 2026-10-07T05:11:00Z (Run 377)

## Run 377 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- A rejected-push recovery no longer uses only the newest `youtube-production.yml` run. That run can be a later execute=false dispatch with no artifact. `persist_provider_state.py recover` walks the last 20 production runs, skips an empty run id, and downloads `provider-upload-state` from the first run that has it. This does not call YouTube or GitHub.

## Run 376 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- A rejected push recovery no longer uses a bare `gh run download --name provider-upload-state`. That command follows the newest run. Agent commits trigger `selftest.yml`, which has no video id. `persist_provider_state.py recover` now pins `youtube-production.yml` via `gh run list`. This does not call YouTube or GitHub.

## Run 375 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- A rejected provider-state push no longer leaves the video id only on the runner. The execute job uploads `upload_state.json` as the `provider-upload-state` artifact (`actions: write`, `continue-on-error`). A rejected push prints `gh run download --repo takenthatusernameis-collab/Content-Automation --name provider-upload-state`. This does not call YouTube.

## Run 374 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- A classify miss with a provider video id no longer exits 0 before `git add`. The persist step prints `PERSIST_CLASSIFY_MISS_STILL_COMMIT` and still commits that id. Status 2 remains a skip. A miss without a video id still fails the step. This does not call YouTube.

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

