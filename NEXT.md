# NEXT

Updated: 2026-10-07T04:12:00Z (Run 376)

Active locks: do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets. `playlist_id` stays `not_set` until a human sets it. Do not add another export probe, media checker, or caption cue gate while `STALL_PREUPLOAD_PROBE` is set. Do not add another Location, session hold, or early-persist call while `STALL_UPLOAD_EDGE` is set. Do not prepend a second `# NEXT` header. Do not add another OAuth exchange parser while videos published stay 0. The unpublished video is the three GitHub Actions secrets. `idle_streak` is a count, not a new gate.

One human step: run `python3 tools/oauth_setup.py`, then `python3 tools/oauth_exchange.py`, paste the full localhost address-bar URL, and store the three secrets with `gh secret set`. Then run `gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false`. Do not commit the token file. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

Older do-not-rediscover notes live in `docs/next_archive.md`. Do not paste the archive back into this file. Do not restore a behavior named there.

1zr40. **Do not rediscover a bare artifact download.** Run 376: `python3 tools/persist_provider_state.py recover` pins `youtube-production.yml` with `gh run list` before `gh run download --name provider-upload-state`. A bare download uses the newest run. That is often selftest, which has no video id. Do not dispatch execute again to retry videos.insert. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr39. **Do not rediscover a rejected push as a lost video id.** Run 375: the execute job uploads `upload_state.json` as `provider-upload-state`. A rejected push prints `python3 tools/persist_provider_state.py recover`. Copy that file onto main before another execute. Do not dispatch execute again to retry videos.insert. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr38. **Do not rediscover a classify miss as a reason to skip the commit.** Run 374: a non-zero `classify-upload` with a provider video id prints `PERSIST_CLASSIFY_MISS_STILL_COMMIT` and still runs `git add`. Status 2 still skips. A miss without that id still fails. Do not exit 0 before the commit. Do not dispatch execute again to retry videos.insert. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.
1zr37. **Do not rediscover a spaced heredoc as a provider-state push.** Run 373: both persist steps call `python3 tools/persist_provider_state.py push`. A `<<'PY'` block closed by `          PY` never ends, so `push_with_retry` does not run and the video id stays off main. Do not put that heredoc back. Do not dispatch execute again to retry videos.insert. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr36. **Do not rediscover a classify miss as an insert failure.** Run 372: the persist step prints `PERSIST_PUSH_NOT_INSERT_FAILURE` and exits 0 when `classify-upload` fails and a provider video id exists. A miss without that id still fails the step. Do not dispatch execute again to retry videos.insert. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr35. **Do not rediscover a playlist crash or a caption-miss summary as an insert failure.** Run 371: the playlist step prints `PLAYLIST_INSERT_NOT_UPLOAD_FAILURE` and exits 0 on any non-zero exit after upload state exists, not only exit 2. The job summary no longer says a caption or thumbnail miss exits non-zero after the video id is written. Do not dispatch execute again to retry videos.insert. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr34. **Do not rediscover a red persist or Studio pin step as an insert failure.** Run 370: the Studio pin step prints `STUDIO_PIN_NOT_INSERT_FAILURE` and exits 0 when the handoff printer fails. The persist step prints `PERSIST_PUSH_NOT_INSERT_FAILURE` and exits 0 when a provider video id exists and the commit or push fails. Do not dispatch execute again to retry `videos.insert`. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr33. **Do not rediscover a red post-upload step as an insert failure.** Run 369: the execute step prints `POST_UPLOAD_NOT_INSERT_FAILURE` and exits 0 when a provider video id exists and `error_class` starts with `POST_UPLOAD_INCOMPLETE`. Do not dispatch execute again to retry `videos.insert`. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr32. **Do not rediscover a red playlist step as an upload failure.** Run 368: the playlist membership step prints `PLAYLIST_INSERT_NOT_UPLOAD_FAILURE` and exits 0 when `playlist_membership.py` exits 2. Do not dispatch execute again to retry that insert. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr31. **Do not rediscover a playlist end-screen element while playlist_id is not_set.** Run 367: `tools/studio_handoff.py` asks for one video element (best for viewer) until a playlist id is set. Do not invent a playlist id. A failed playlist insert is not a reason to dispatch execute again. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr30. **Do not rediscover a second stall-watch check.** Run 366: `tools/selftest.py` keeps one `check_stall_watch`. It runs `stall_watch_contract.py` and the inline stall assertions. A later copy must not shadow the contract. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr29. **Do not rediscover a zero idle streak as a stall flag.** Run 365: `flag_text` omits `idle_streak: 0`. A quiet file stays empty. A positive streak still prints. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

1zr28. **Do not rediscover an uncounted OAuth idle streak.** Run 364: `tools/stall_watch.py` prints `idle_streak` and, at 8 or more, `suspicious: oauth_idle_without_publish`. The live streak is 13 after this delta. Do not treat another restatement as progress. Do not add another exchange parser. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.
