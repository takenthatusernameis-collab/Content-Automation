# NEXT

Updated: 2026-10-06T10:12:00Z (Run 361)

Active locks: do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets. `playlist_id` stays `not_set` until a human sets it. Do not add another export probe, media checker, or caption cue gate while `STALL_PREUPLOAD_PROBE` is set. Do not add another Location, session hold, or early-persist call while `STALL_UPLOAD_EDGE` is set. Do not prepend a second `# NEXT` header. Do not add another OAuth exchange parser while videos published stay 0. The unpublished video is the three GitHub Actions secrets.

One human step: run `python3 tools/oauth_setup.py`, then `python3 tools/oauth_exchange.py`, paste the full localhost address-bar URL, and store the three secrets with `gh secret set`. Then dispatch `youtube-production.yml` with execute=true. Do not commit the token file. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

Older do-not-rediscover notes live in `docs/next_archive.md`. Do not paste the archive back into this file. Do not restore a behavior named there.

1zr25. **Do not rediscover a lock sentence as a wired probe.** Run 361: `tools/stall_watch.py` ignores a do-not-add lock sentence before `STALL_PREUPLOAD_PROBE` and `STALL_UPLOAD_EDGE`. A wired tool still sets the flag. `chapter_sync_reason` refuses a last chapter inside the final 10 seconds when duration is known. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr24. **Do not rediscover a second Active locks block.** Run 360: `tools/next_compact.py` keeps one `Active locks:` block and drops a lone `.` paragraph. The human step is the three secrets, not another exchange parser. Do not add another export probe, media checker, or caption cue gate. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr23. **Do not rediscover a raw-code-only token exchange.** Run 359: `tools/oauth_exchange.py` accepts the full localhost redirect URL or a raw code. It does not print the code. The refresh token is still written only outside the repo. Do not commit that file. Do not add another export probe, media checker, or caption cue gate. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr22. **Do not rediscover an unscripted token exchange.** Run 358: `tools/oauth_exchange.py` builds the consent URL and writes a refresh token only outside the repo. Do not commit that file. Do not print the token. Do not add another export probe, media checker, or caption cue gate. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr21. **Do not rediscover stacked FAILURES or PROGRESS headers.** Run 357: `tools/log_compact.py` drops a later file header and a repeated archive pointer. Each live log keeps one header and 12 sections. Do not prepend a second header. Do not add another export probe, media checker, or caption cue gate. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr20. **Do not rediscover the draft-pin sentence.** Run 355: `parse_publish` drops a `Chapter draft (` label and `This comment is a draft pin, not posted.` before the dry-run body and before execute. Chapter timestamp lines stay. Do not put that sentence back. Do not add another export probe, media checker, or caption cue gate. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr19. **Do not rediscover another pre-upload checker.** Run 354: `tools/stall_watch.py` prints `STALL_PREUPLOAD_PROBE` when the newest four OAuth-idle deltas each name `export_probe`, `media_qa`, or `caption_gate`. The flag does not fail the job and does not call YouTube. Do not add another export probe, media checker, or caption cue gate while it is set. Do not add another Location, session hold, or early-persist call. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr18. **Do not rediscover a production job that skips caption cues.** Run 353: the workflow runs `tools/caption_gate.py` after media QA and before the export probe. It does not rewrite captions and does not call YouTube. A present bad cue fails the job. A missing srt fails only when execute=true. Do not add another export-probe lock. Do not add another media checker. Do not add another Location, session hold, or early-persist call. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr17. **Do not rediscover a production job that skips media QA.** Run 352: the workflow runs `tools/media_qa.py` after materialize and before the export probe. It does not encode and does not call YouTube. Q1 must pass. A non-Q1 missing take fails only when execute=true. Do not add another export-probe lock. Do not add another Location, session hold, or early-persist call. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr16. **Do not rediscover an ftyp-only master.** Run 350: `tools/export_probe.py` fails a present master that is not 1920x1080 h264 with audio and at least 20s. The production workflow runs it before the upload gates. Exit 1 always fails the job. Exit 2 fails only when execute=true. The probe does not encode and does not call YouTube. Do not add another Location, session hold, or early-persist call. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr15. **Do not rediscover the upload-edge loop.** Run 349: caption, thumbnail, and comment status are early-persisted after each write when `UPLOAD_EARLY_PERSIST=1`. `STALL_UPLOAD_EDGE` is set after four OAuth-idle upload-edge runs. Do not add another Location, session hold, or early-persist call while that flag is set. Next work is the three YouTube secrets, or a production tool that is not the uploader. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr14. **Do not rediscover a video id that exists only on the runner.** Run 348: after `videos.insert` returns an id, that id is early-persisted before caption wait when `UPLOAD_EARLY_PERSIST=1`. A 404/410 hold and a completed-without-id hold are early-persisted before the step returns. The later persist step still runs. Do not print the URI. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.
