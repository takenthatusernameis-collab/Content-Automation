# RUNS

## Run 362 — 2026-10-06T11:20:00Z
- Objective: Make the first private execute a copy-paste dispatch instead of an unscripted workflow click.
- Action: `tools/oauth_setup.py` now prints `gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false`. Selftest requires that command. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Recipe check passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `check_oauth_setup_recipe` returned no failures. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Step 8 named execute=true but not the `gh` invocation. A first dispatch with collect_feedback=true would fetch before a video id exists.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-idle runs have not published a video. Do not add another exchange parser.
- Next: A human stores the three secrets and runs that dispatch. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 361 — 2026-10-06T10:12:00Z
- Objective: Stop lock sentences from keeping stall flags set, and stop a last chapter inside the final 10 seconds from being uploaded as if YouTube would show it.
- Action: `stall_watch.py` scrubs do-not-add sentences before the pre-upload and upload-edge token checks. `chapter_sync_reason` takes an optional duration and refuses `chapter_last_under_10s_before_end`. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser.
- Result: Stall contract passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Newest STATE deltas repeated the lock sentence, and that sentence contained the same tokens as a wired probe. The flag could not clear. YouTube also drops a chapter list whose last stamp is inside the final 10 seconds. That check was missing.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-idle runs have not published a video. Do not add another exchange parser.
- Next: A human stores the three secrets and dispatches execute=true. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 360 — 2026-10-06T09:11:00Z
- Objective: Stop a second Active locks block from hiding the one human step on a truncated NEXT.md fetch.
- Action: `next_compact.py` keeps one Active locks block and drops a lone `.` paragraph. NEXT.md now names the three secrets as the step. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload probe. Did not add another OAuth exchange parser.
- Result: Contract passed. Oldest NEXT note archived. Videos published stay 0. No live execute.
- Verification: `python3 tools/next_compact_contract.py` printed NEXT COMPACT CONTRACT PASS. Actions not re-run. No provider write.
- Discovery: NEXT.md had two Active locks blocks plus a `.` paragraph. A truncated fetch could land in the copy and miss the human step. Runs 358-359 added exchange parsers and published nothing.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-helper runs have not published a video. Do not add another exchange parser.
- Next: A human stores the three secrets and dispatches execute=true. Do not add another probe. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 359 — 2026-10-06T08:11:00Z
- Objective: Stop the first OAuth exchange from failing when the human pastes the localhost address bar.
- Action: `oauth_exchange.py` extracts the code from a redirect URL or a raw code. Denied redirects are refused. The token still writes only outside the repo. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload probe.
- Result: Contract passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/oauth_exchange_contract.py` printed OAUTH EXCHANGE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Desktop consent does not load localhost. The code is in the address bar. A raw-code-only stdin read would send that URL to the token endpoint.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-idle runs have not published a video. Do not add another probe.
- Next: A human runs the exchange once and stores the three secrets. Paste the full redirect URL. Do not add another probe. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 358 — 2026-10-06T07:15:00Z
- Objective: Cut the manual OAuth token exchange down to one local command that cannot commit the refresh token.
- Action: Added `tools/oauth_exchange.py` and a contract. The recipe now points at it. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload probe.
- Result: Contract passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/oauth_exchange_contract.py` printed OAUTH EXCHANGE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: The setup recipe named the scopes but still left the consent URL and token POST to an unscripted browser step. A wrong scope still creates a private video that cannot take captions.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human runs the exchange once and stores the three secrets. Do not add another probe. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 357 — 2026-10-06T06:20:00Z
- Objective: Stop stacked FAILURES and PROGRESS headers from hiding the newest lesson.
- Action: `log_compact.py` drops a later file header and a repeated archive pointer. Both live logs now have one header and 12 sections. Finished the cut Run 356 STATE bullet. Did not poll secrets. Did not add a scanner or a probe.
- Result: Contracts passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/log_compact_contract.py` printed LOG COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 356 collapsed STATE headers only. FAILURES and PROGRESS still had stacked headers.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not prepend a second file header. Do not add another probe. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 356 — 2026-10-06T05:11:00Z
- Objective: Stop stacked STATE headers from hiding or truncating the current gate.
- Action: `state_compact.py` now keeps one preamble and strips later `# STATE` headers before the size cap. Collapsed the live file from 13 headers to 1. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload probe.
- Result: Contract passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/state_compact_contract.py` printed STATE COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Each run prepended a full `# STATE` file. Compact counted `## Run` only, so the Run 343 body was already cut and a dangling header remained.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not prepend a second `# STATE` header. Do not add another export probe, media checker, or caption cue gate. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

Older runs live in `docs/runs_archive.md`. Do not paste the archive back. `tools/runs_compact.py` moves extras. It does not delete history.

## Run 355 — 2026-10-06T04:15:00Z
- Objective: Stop the first upload from publishing internal production notes in the description and pinned comment.
- Action: `parse_publish` drops a `Chapter draft (` label and the sentence `This comment is a draft pin, not posted.` Q1 `publish.md` and `publish_brief.py` no longer contain them. Chapter timestamp lines stay. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a probe, media checker, or caption cue gate. Did not add an upload-edge persist call.
- Result: Dry-run copy no longer contains those notes. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/youtube_upload.py` on Q1 printed chapters_in_description PASS and did not print the chapter label or draft-pin sentence. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Delegated approval had checked the description and first-comment boxes while the viewer-facing sections still said the chapter list was unapproved and the pin was not posted.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: pre-upload probe patches have not published a video. Do not add another one.
- Next: Do not install the r249 master. Do not add another Location, session hold, or early-persist call. Do not add another export probe, media checker, or caption cue gate. Do not add a scanner. Do not scaffold Q2. Do not poll secrets. Do not put the draft-pin sentence back into the pin.

## Run 354 — 2026-10-06T03:20:00Z
- Objective: Stop the next run from adding another pre-upload checker while videos published stay 0.
- Action: `tools/stall_watch.py` now prints `STALL_PREUPLOAD_PROBE` when the newest four OAuth-idle deltas each name `export_probe`, `media_qa`, or `caption_gate`. The flag does not fail the job. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add an upload-edge persist call. Did not add an export-probe lock. Did not add another media checker. Did not add another caption cue gate.
- Result: Contract passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. `python3 tools/stall_watch.py` printed `STALL_PREUPLOAD_PROBE`. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Runs 350-353 each wired a probe that already existed or a cue check, and none published a video. The same shape already stopped the upload-edge loop. The unpublished video is still the missing OAuth secrets.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: pre-upload probe patches have not published a video. Do not add another one.
- Next: Do not install the r249 master. Do not add another Location, session hold, or early-persist call. Do not add another export-probe lock. Do not add another media checker. Do not add another caption cue gate. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

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

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.
Earlier runs through Run 269 remain in git at `9416aae2c482ca08fd55642e0fff94568482ee51` (`RUNS.md` blob `243e47753b76bbd636a59dddb00e8c1c6f2e90c1`) and before that at `65cca063`.
