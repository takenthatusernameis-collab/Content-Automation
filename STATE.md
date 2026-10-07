# STATE

Updated: 2026-10-07T13:23:00Z (Run 385)

## Run 385 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new scanner. Q1 was not rewritten. No new packet folder. No new exchange parser. No new pre-upload checker. No new early-persist call. No new recovery edge. Did not extend operator_card. No new operator card.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- `tools/operator_card_freeze.py` fails if `operator_card.py` grows a function, a second card module appears, or the card imports a network client. Runs 383-384 extended the card and still published nothing. This does not call YouTube or GitHub.


Updated: 2026-10-07T12:20:00Z (Run 384)

## Run 384 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new scanner. Q1 was not rewritten. No new packet folder. No new exchange parser. No new pre-upload checker. No new early-persist call. No new recovery edge.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- `python3 tools/operator_card.py` now reprints the numbered Google Cloud steps from `oauth_setup.py`, including the Desktop-app client, the three scopes, `oauth_exchange.py`, and the secret-set lines. It fails if those steps drift. This does not call YouTube or GitHub.

## Run 383 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new scanner. Q1 was not rewritten. No new packet folder. No new exchange parser. No new pre-upload checker. No new early-persist call. No new recovery edge.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- The one human step is now `python3 tools/operator_card.py`. It prints the same dispatch line as `oauth_setup.py` and fails if HANDOFF loses the documented master sha. This does not call YouTube or GitHub.

- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker. No new early-persist call. No new recovery edge.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- The provider-state recovery surface is frozen. `tools/recovery_freeze.py` fails if `youtube-production.yml` grows another `provider-upload-state` artifact or another `persist_provider_state.py recover` call. This does not call YouTube or GitHub. Release `q1-media-r253` master still matches sha256 `4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546` and ffprobe 1920x1080 h264 30fps yuv420p stereo AAC 48000 Hz, duration 328.40s. That check did not encode and did not upload.

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

