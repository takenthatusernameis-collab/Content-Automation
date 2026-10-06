# STATE

Updated: 2026-10-06T13:22:00Z (Run 364)

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

## Run 361 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser. No new pre-upload checker.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. The unpublished video is still the three GitHub Actions secrets.
- `tools/stall_watch.py` now ignores a do-not-add lock sentence when deciding `STALL_PREUPLOAD_PROBE` and `STALL_UPLOAD_EDGE`. A wired tool still sets the flag. A lock sentence alone does not. This does not call YouTube.
- `chapter_sync_reason` refuses a last chapter that starts inside the final 10 seconds when duration is known. Unknown duration does not invent an end. Q1 lines still pass at 328.4s. This does not regenerate chapters and does not call YouTube.

## Run 360 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder. No new OAuth exchange parser.
- `STALL_OAUTH_IDLE` still stands. `STALL_PREUPLOAD_PROBE` still stands. `STALL_UPLOAD_EDGE` still stands. `playlist_id` remains `not_set`. Do not add another export probe, media checker, or caption cue gate. Do not add another exchange parser.
- `tools/next_compact.py` now keeps one `Active locks:` block and drops a lone `.` paragraph. NEXT.md names the three secrets as the human step. This does not call YouTube.

## Run 359 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `STALL_PREUPLOAD_PROBE` still stands. `playlist_id` remains `not_set`. Do not add another export probe, media checker, or caption cue gate.
- `tools/oauth_exchange.py` accepts a raw auth code or the full localhost redirect URL and still writes the refresh token only outside the repo. It does not print the code. This does not call YouTube.

## Run 358 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `STALL_PREUPLOAD_PROBE` still stands. `playlist_id` remains `not_set`. Do not add another export probe, media checker, or caption cue gate.
- `tools/oauth_exchange.py` prints a consent URL with upload, force-ssl, and analytics scopes, then exchanges one stdin code. The refresh token is written only to an absolute path outside the repo. It does not call GitHub and does not print the token. This does not call YouTube.

## Run 357 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `STALL_PREUPLOAD_PROBE` still stands. `playlist_id` remains `not_set`. Do not add another export probe, media checker, or caption cue gate.
- `tools/log_compact.py` now drops a later `# FAILURES`, `# PROGRESS`, or `# LOG` header and a repeated archive pointer before the size cap. Live FAILURES.md and PROGRESS.md each keep one header and 12 sections. The Run 356 STATE bullet that ended on a dangling backtick is finished. This does not call YouTube.

## Run 356 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `STALL_PREUPLOAD_PROBE` still stands. `playlist_id` remains `not_set`. Do not add another export probe, media checker, or caption cue gate.
- STATE.md had 13 stacked file headers. Compact collapsed them to one. The fetch cut this bullet mid-line. Do not treat a dangling backtick as a new gate.

## Run 355 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `STALL_PREUPLOAD_PROBE` still stands. `playlist_id` remains `not_set`. Do not add another export probe, media checker, or caption cue gate. Do not add another upload-edge persist call.
- The approved Q1 description still contained `Chapter draft (not ASR, not an approval...)` and the approved pin still ended with `This comment is a draft pin, not posted.` `videos.insert` and `commentThreads.insert` would have published those notes. `parse_publish` now drops that chapter label and that pin sentence. Chapter timestamp lines stay. `publish.md` and `publish_brief.py` no longer emit them. This does not call YouTube.
- Local dry-run still HOLD_LOCAL (missing master in this checkout, missing OAuth). Chapter label and draft-pin sentence were absent from the dry-run text. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

## Run 354 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. Do not add another upload-edge persist call. Do not add another export-probe lock. Do not add another media checker. Do not add another caption cue gate.
- Runs 350-353 each wired a pre-upload checker (`tools/export_probe.py`, `tools/media_qa.py`, `tools/caption_gate.py`) while videos published stayed 0. `tools/stall_watch.py` now prints `STALL_PREUPLOAD_PROBE` after four such deltas. The flag does not fail the job. It does not call YouTube. Do not wire another export probe, media checker, or caption cue gate while it is set.
- `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

## Run 353 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. `tools/stall_watch.py` was not given a new flag. Do not add another upload-edge persist call. Do not add another export-probe lock. Do not add another media checker.
- The production job ran media QA and the export probe, then still called captions.insert on any present srt. An overlapping cue, a line over 42 characters, or a cue past the selected wav could reach the provider. `tools/caption_gate.py` now runs after media QA. A present bad cue fails the job. A missing srt fails only when execute=true. It does not rewrite captions and does not call YouTube.
- Local Q1 captions printed caption_gate PASS (103 cues). `python3 tools/caption_gate_contract.py` printed CAPTION GATE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

## Run 352 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. No new scanner. Q1 was not rewritten. No new packet folder.
- `STALL_OAUTH_IDLE` still stands. `playlist_id` remains `not_set`. `tools/stall_watch.py` was not given a new flag. Do not add another upload-edge persist call. Do not add another export-probe lock.
- The production job materialized Q1 and then probed the master, but it never ran `tools/media_qa.py`. A bad take or a wrong-size card could still reach the upload gates. The workflow now runs media QA after materialize and before the export probe. It does not encode and does not call YouTube. Q1 must pass. A non-Q1 missing take fails the job only when execute=true.
- Local Q1 media from `q1-media-r253` and the r249 wav/cards printed media_qa gate PASS (308.4s wav, 7/7 cards, export ftyp). `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.
