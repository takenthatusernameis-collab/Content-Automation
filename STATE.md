# STATE

Updated: 2026-10-05T00:20:00Z (Run 326)

## Run 326 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. Q1 WORDS and research.md were not rewritten. No new packet folder.
- Spoken digit tokens and survey hedges in script WORDS now fail `ready_for_vo` unless a non-placeholder Sources bullet cites that same token or phrase. `tools/claim_scan.py` does not rewrite. A missing script is not a hit.
- Q1, the template, and the sample printed clear. `python3 tools/claim_scan_contract.py` printed CLAIM SCAN CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-04T23:20:00Z (Run 325)

## Run 325 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. Q1 WORDS were not rewritten. No new packet folder.
- `youtube-production.yml` now refuses a dispatch packet with `tools/packet_path.py` before materialize. The Q1 path still passes. A missing folder, `_template`, or a path outside `videos/<slug>` exits 2. The tool does not create a folder and does not write upload state.
- `python3 tools/packet_path_contract.py` printed PACKET PATH CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-04T22:13:00Z (Run 324)

## Run 324 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. Q1 WORDS were not rewritten. No new packet folder.
- `youtube-production.yml` now takes a `packet` dispatch input. The default is still `videos/002-stop-deciding-what-to-work-on-every-morning`. `PACKET` comes from that input. Q1 release materialize runs only for that path. Other `videos/<slug>` values are not filled from the Q1 releases. `_template` and `..` are refused.
- `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.

# STATE

Updated: 2026-10-04T21:20:00Z (Run 323)

## Run 323 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write. Q1 WORDS were not rewritten. No new packet folder.
- `tools/set_status.py` now refuses `ready_for_vo` when `quality_scan.scan_path` finds an anti-slop phrase. A missing script is not a hit. The scanner still does not rewrite script.md.
- `python3 tools/quality_scan_contract.py` printed QUALITY SCAN CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.
- Q1 quality_scan still printed clear. Promoting Q1 again still stops on already ready_for_vo.

# STATE

Updated: 2026-10-04T21:12:00Z (Run 322)

## Run 322 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No provider write.
- Pre-change stall printer named STALL_INSTRUCTION_LOCK on Runs 319-321. Those three deltas were credential-idle copy edits. The flag is a printer, not a CI failure.
- `tools/quality_scan.py` reports anti-slop phrases in script WORDS and does not rewrite. Q1, the template, and the sample were clear. Contracts lock the scanner and the stall printer. Selftest runs both.
- Q1 WORDS were not rewritten. `videos/003-put-the-start-cue-on-the-work-itself` was not created.

# STATE

Updated: 2026-10-04T20:15:00Z (Run 321)

## Run 321 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No Studio URL or end-screen sentence added. `STALL_OAUTH_AND_STUDIO` still stands.
- fill-idea still told the operator to paste idea.md by hand after Run 320 added `tools/apply_idea.py`. `tools/hint.py` now prints `doctor.py` then `apply_idea.py` dry-run. `--write` is a comment, not the first command. `next_action.py`, `idea_brief.py`, `expand_prompt.py`, `next_topic.py`, and `queue_status.py` name that command. A reviewed idea.md is still refused.
- `python3 tools/idea_gate_contract.py` printed IDEA GATE CONTRACT PASS. `python3 tools/selftest.py` now runs that contract and printed SELFTEST PASS. Actions was not re-run.
- Q1 idea.md was not rewritten. `videos/003-put-the-start-cue-on-the-work-itself` was not created.

# STATE

Updated: 2026-10-04T19:30:00Z (Run 320)

## Run 320 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No Studio URL or end-screen sentence added. `STALL_OAUTH_AND_STUDIO` still stands.
- Blank `idea.md` after scaffold was still a hand paste even though the queue paste is locked. `tools/apply_idea.py` fills that file from `paste_block` only when it is still the blank template or already equal. A reviewed idea.md is refused. It does not scaffold, does not write spoken WORDS, and does not mark the queue used.
- `python3 tools/apply_idea_contract.py` printed APPLY IDEA CONTRACT PASS on a tempfile packet. `videos/003-put-the-start-cue-on-the-work-itself` was not created. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.
- Q1 idea.md was not rewritten.

# STATE

Updated: 2026-10-04T18:14:00Z (Run 319)

## Run 319 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No handoff URL sentence added.
- Queued topics Q2-Q5 had no locked problem line, so idea_brief asked for a handwritten problem before expand. `docs/topic_queue.md` now has a problem column. `idea_followup` reads that cell. Q1 still reprints the existing pin sentence. No packet folder was created.
- `queue_contract.py` fails if those four problem cells disappear. `python3 tools/queue_contract.py` printed QUEUE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions was not re-run.
- `python3 tools/idea_brief.py --queue Q2` reprints the locked problem and writes nothing.


Updated: 2026-10-04T14:16:00Z (Run 318)

## Run 318 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. No Studio URL or end-screen sentence added. `STALL_OAUTH_AND_STUDIO` still stands.
- `docs/topic_queue.md` no longer says the next scaffold is `002-`. Q1 already occupies `videos/002-stop-deciding-what-to-work-on-every-morning`. `tools/next_topic.py` still prints `videos/003-put-the-start-cue-on-the-work-itself`. `queue_contract.py` fails if the stale 002 sentence returns.
- Release listing still shows `q1-media-r253` `q1-master-r253.mp4` digest `sha256:4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546` and the r249 wav digest `sha256:758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`. Not re-downloaded. Not re-encoded.
- `queue_contract.py` and `selftest.py` passed locally. Actions was not re-run.


Updated: 2026-10-04T12:20:00Z (Run 317)

## Run 317 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. Upload-variant freeze, fetch-depth 0, and prove_locks stay in place.
- Flag: Runs 314-316 each added a Studio handoff sentence while the publish gate stayed the missing secrets. `tools/stall_watch.py` now prints `STALL_OAUTH_AND_STUDIO` when the last three STATE deltas match that pattern. The flag does not fail CI. Do not add another Studio URL or end-screen sentence while it is set.
- The remaining handoff text now takes the reserve from `timeline.END_SCREEN` (`end_screen_reserve_s`). It does not hardcode 20. `pinned` stays false. `end_screen` stays `not_set`. No YouTube call.
- Selftest, prove_locks, and upload_variant_freeze passed locally. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. Do not spend a run only restating the OAuth hold.

Updated: 2026-10-04T11:20:00Z (Run 316)

## Run 316 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. Upload-variant freeze, fetch-depth 0, and prove_locks stay in place.
- `studio_pin.md` now also records the end screen the Data API cannot set. `end_screen: not_set`. The editor URL is written only when a provider video id exists. A missing id still does not invent a URL. `pinned` stays false. Do not re-encode for the end screen; the master already reserves the last 20 seconds.
- Selftest, prove_locks, and upload_variant_freeze passed locally. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. Do not spend a run only restating the OAuth hold.


Updated: 2026-10-04T10:12:00Z (Run 315)

## Run 315 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. Upload-variant freeze, fetch-depth 0, and prove_locks stay in place.
- `tools/studio_handoff.py --write` stores `studio_pin.md` only when upload_state.json has a provider video id. A missing id prints `not_written` and does not invent a URL file. `pinned` stays false. The production persist step commits that file with the video id.
- Selftest, prove_locks, and upload_variant_freeze passed locally. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. Do not spend a run only restating the OAuth hold.


Updated: 2026-10-04T09:20:00Z (Run 314)

## Run 314 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. Upload-variant freeze, fetch-depth 0, and prove_locks stay in place.
- Q1 materialize installed the r253 master and ignored the truncated r249 master. media_qa PASS. Dry-run gate YOUTUBE_AUTH_REQUIRED.
- `tools/studio_handoff.py` prints the Studio comments URL after execute when a provider video id exists. `pinned` stays false. A missing id does not invent a URL. The Data API still cannot pin.
- Selftest, prove_locks, and upload_variant_freeze passed locally. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. Do not spend a run only restating the OAuth hold.

Updated: 2026-10-04T08:20:00Z (Run 313)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + narration adapter + labeled generated fallback + local card generator + WORDS timeline planner + fail-closed media QA + authenticated YouTube uploader (dry-run default, execute path) + authenticated feedback ingestion (dry-run default, execute path) + fail-closed ffmpeg assemble planner + fail-closed feedback/experiment/complete gates + documented experiment baseline contract + gate-machine drop recipe + Actions materialize/dry-run verified -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning` status `ready_for_vo`
- Durable fetch: private release `q1-media-r253` (padded master) plus r249 wav/cards
- r249 master is truncated (308.40s). Finished local export is `q1-media-r253` `q1-master-r253.mp4` (328.40s).
- Actions dry-run 36983196381 materialized that set and reached `YOUTUBE_AUTH_REQUIRED`. Execute was not dispatched.
- Category and license now come from docs/channel.md (27 / youtube). Executive: SHIP after the three YouTube OAuth secrets exist and `youtube-production.yml` is dispatched with execute=true. That execute now posts the already-approved first comment. skip_comment opts out. The Data API does not pin it. Do not re-encode. Do not upload r249. Do not expand architecture. Do not spend a run only restating the secret hold.

## Run 313 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. The upload-variant freeze stays in place. Production checkout stays `fetch-depth: 0`. prove_locks stays in selftest.yml.
- Run 312 locked `category_id: 27` and `license: youtube` in `docs/channel.md` but the adapter still hardcoded `categoryId` 27. `youtube_upload.py` now reads both fields. Unknown or missing values are HOLD_LOCAL and `METADATA_REJECTED:category_unknown` or `METADATA_REJECTED:license_unknown` before the token refresh. A missing file does not invent 27 or creativeCommon. The insert body uses the channel values.
- Selftest, prove_locks, and upload_variant_freeze passed locally. Actions run 37188429455 concluded success on `56b782f7222dcd44ccc3bed405124a4296c9420b`.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. Do not spend a run only restating the OAuth hold.

## Run 311 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. The upload-variant freeze stays in place. Production checkout stays `fetch-depth: 0`. prove_locks stays in selftest.yml.
- Dispatch input `skip_comment` passes `--skip-comment` and wins over `post_comment`. An approved first comment still posts when skip is false. `comment_post.pinned` stays false because `commentThreads.insert` does not pin. Studio pin remains a one-time human step after the private upload.
- Selftest, prove_locks, and upload_variant_freeze passed locally. Actions run 37182446814 concluded success on `c95a5438abda65ff99f8d38049e0be7a4efed98c`.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. Do not spend a run only restating the OAuth hold.

## Run 310 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. The upload-variant freeze stays in place. Production checkout stays `fetch-depth: 0`. prove_locks stays in selftest.yml.
- Local materialize installed the r253 master and ignored the truncated r249 master. Dry-run gate was `YOUTUBE_AUTH_REQUIRED`. media_qa PASS. Q1 first-comment box is checked (199 characters).
- Execute now posts that pin comment on the same dispatch when the box is checked. `--skip-comment` opts out. A second execute only to post the comment is no longer required. Selftest, prove_locks, and upload_variant_freeze passed locally. Actions run 37179477808 concluded success on `ec9d111de2f64fe697f76c59e1d7727c8a559341`.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. Do not spend a run only restating the OAuth hold.

## Run 309 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. The upload-variant freeze stays in place. Production checkout stays `fetch-depth: 0`.
- `prove_locks.py` was only a remembered command. `.github/workflows/selftest.yml` now runs it on every push. `selftest.py` fails if that step is removed. The tool stays unmapped in `needed.py`. Local selftest and prove_locks passed. Actions run 37176474403 concluded success on `20f05c8a20cec81271e06f75441aef4d659b505e`.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. Do not spend a run only restating the OAuth hold.

## Run 308 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- No new YouTubeAPIError reason. The upload-variant freeze stays in place.
- Production checkout was still the Actions default (depth 1). A rejected provider-state push then depended on `git fetch --unshallow` after the upload. That fetch can fail or eat the rest of the job, and the video id stays only on the runner. Checkout is now `fetch-depth: 0`. The unshallow retry remains for any other shallow caller. Selftest refuses `fetch-depth: 1`. prove_locks and the variant freeze passed. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. Do not restore a shallow production checkout.

## Run 307 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- Runs 281-306 kept adding upload gates while the publish gate stayed the missing secrets. That loop is now a selftest freeze. `tools/upload_variant_freeze.py` rejects a new `YouTubeAPIError` reason in `youtube_api.py` or `youtube_upload.py` unless `docs/live_execute_evidence.md` has `live_status: REASON_CODE` from a real execute. Existing reasons stay allowed. No new HTTP status was added. Selftest and prove_locks passed locally. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. The freeze is the lock. Do not add a reason to the allowlist to bypass the evidence file.

## Run 306 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- Run 305 waited only 60 seconds for processingDetails. A 1080p master often stays processing longer, so the first execute would exit VIDEO_PROCESSING_NOT_READY and need another dispatch for the same caption. The wait is now 30 polls of 20 seconds, about 10 minutes, still inside the 60-minute job. Selftest locks a budget of at least 8 minutes and at most 15. prove_locks passed. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status.

## Run 305 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- captions.insert before processing finishes is a 400, and this client treats 400 as permanent. Execute now polls processingDetails and waits until succeeded or terminated before the caption call. failed is VIDEO_PROCESSING_FAILED. Still processing after the caption wait budget is VIDEO_PROCESSING_NOT_READY. Run 306 raised that budget from 60 seconds to about 10 minutes. Neither starts another videos.insert. The video id stays persisted so the next execute resumes the caption. Selftest and prove_locks passed locally. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status.

## Run 304 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `python3 tools/prove_locks.py` now passes on this checkout. The placeholder needle in words_contract.py is split, and the write-path leak check hashes the live Q1 packet instead of requiring it to be absent. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status.

## Run 303 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- The production job timeout was 20 minutes while a chunk PUT waited up to 600 seconds and retried three times. A killed runner never persists the video id, so the next execute can insert again. The job is now 60 minutes and the chunk PUT timeout is 180 seconds. Selftest locks both. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status.

## Run 302 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `videos.insert` must send `status.selfDeclaredMadeForKids` from `docs/channel.md` `audience_designation`. This channel is `not_made_for_kids`, so the flag is false. An unknown designation is `AUDIENCE_UNKNOWN` before the token refresh and does not insert. The API layer no longer defaults a missing flag to false. Omitting the field uploads a video that stays blocked until Studio sets the audience. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status.

## Run 301 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- Drafted chapter lines must be in the description before videos.insert. Fewer than 3, a first stamp other than 0:00, a gap under 10 seconds, or a missing or reordered line is HOLD_LOCAL / METADATA_REJECTED. A missing chapters.md stays missing. Q1 already matches. Selftest passed locally. Actions was not re-run.
- The production workflow already queues on `concurrency: youtube-production`. Do not rediscover that.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. Description angle brackets remain ungated and deferred on purpose.

## Run 300 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- The upload-status loop stays frozen. No new HTTP status variant. Description angle brackets stay ungated on purpose.
- `tools/oauth_setup.py` prints the non-secret secret-entry recipe: console steps, required scopes, and `gh secret set` commands that read from the prompt. It reports missing secret names only. `docs/human_session.md` no longer tells the operator to re-open Description edited or First comment approved. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status.

## Run 299 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- videos.insert now sets status.containsSyntheticMedia from vo_origin.md. Q1 kind is generated, so the flag is true. A human kind is false. An unknown kind is SYNTHETIC_DISCLOSURE_UNKNOWN before the token refresh and does not insert. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. Description angle brackets remain ungated and deferred on purpose.

## Run 298 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- A rejected provider-state push on the Actions runner could still drop the video id. checkout@v4 is shallow, and `git rebase origin/main` has no merge base until the clone is unshallowed. `push_with_retry` now unshallows when `git rev-parse --is-shallow-repository` is true, then fetches and rebases. It does not force-push. A failed rebase aborts. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. Description angle brackets remain ungated and deferred on purpose.

## Run 297 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- Provider state persist no longer uses a single `git push origin HEAD:main`. A non-fast-forward rejection fetches and rebases, then retries. It does not force-push. A provider video id and a completed-without-id hold still commit. Transient failures and dry-run feedback still do not. Selftest passed locally. Actions was not re-run.
- Q1 board copy no longer tells the operator to check Description edited or First comment approved. Those boxes are already checked. Do not re-open them.
- Flag still stands: do not add another upload HTTP status variant unless a live execute returned that status. Description angle brackets remain ungated and deferred on purpose.

## Run 296 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- Flag: Runs 281-295 kept adding upload status and snippet gates while the publish gate stayed the missing OAuth secrets. That loop is now suspicious. Do not add another HTTP status variant unless a live execute returned that status.
- A 308 Range that is not on a 256 KiB boundary is `RESUMABLE_STALLED` (`unaligned_offset`). The next chunk is not sent. That is a protocol reject, not a new status class. Selftest passed locally. Actions was not re-run.
- Description angle brackets remain ungated and deferred on purpose.

## Run 295 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- A 200/201 whose follow-up session query returns 404 or 410 is now `RESUMABLE_COMPLETED_SESSION_GONE`. The last byte was accepted and the session can no longer return the id. Execute writes `completed_without_id` and does not invent a video id. A matching fingerprint is `HOLD_COMPLETED_WITHOUT_ID` and must not start another videos.insert. The workflow commits that hold. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose. The OAuth secret stall is still the publish gate. This run closed a documented duplicate-insert hole; it did not restate the secret hold as the only work.

## Run 294 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- A finishing chunk PUT that returns 200 or 201 with an empty or id-less body now queries that same session once and uses the video resource. It does not open another videos.insert. A query that is not 200/201 still raises `RESUMABLE_MISSING_VIDEO_ID`. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. The upload-transport loop is now covering lost completion bodies; do not keep adding status variants without a documented hole. Description angle brackets remain ungated and are deferred on purpose.

## Run 293 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- A 401 on caption, thumbnail, pin-comment, or channel-id lookup refreshes the access token and retries that same call. It does not open another videos.insert. Three refreshes or an empty/unchanged token raise `POST_UPLOAD_TOKEN_REFRESH_EXHAUSTED`. A 400 stays permanent. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose.

## Run 292 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- A 401 on a chunk PUT, or on session start with no Location, refreshes the access token and resumes the same upload. A Location already returned is not followed by another videos.insert. Three refreshes or an empty/unchanged token raise `RESUMABLE_TOKEN_REFRESH_EXHAUSTED`. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose.

## Run 291 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- Caption, thumbnail, and pin-comment calls now retry 408/429/5xx and network errors up to three times. A 400 stays permanent. This does not start another videos.insert. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose.

## Run 290 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- Session start now retries a 408/429/5xx or network error only when the POST returns no Location. A Location on that response is the session and is not followed by a second videos.insert. Chunk 408 and 429 resume the existing session. A status query that advances the offset clears the retry count. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose.

## Run 289 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- A 308 with no Range header now restarts at byte 0. The YouTube resumable guide says that response means nothing is stored. The previous fallback treated the chunk just sent as accepted. Three missing-Range responses at the same stage raise `RESUMABLE_STALLED`. Retry-After is honored, capped at 30 seconds. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose.

## Run 288 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `upload_video` now treats HTTP 500, 502, 503, and 504, and a network error on a chunk PUT, as resumeable. It queries the session with `Content-Range: bytes */size` and continues from the returned Range. Three failures at the same stage raise `RESUMABLE_RETRY_EXHAUSTED`. A 404 on that query is `RESUMABLE_SESSION_EXPIRED`. Captions and thumbnails stay multipart. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose.

## Run 287 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `videos.insert` no longer uses one multipart POST of the master. `youtube_api.upload_video` starts a resumable session and sends 8 MiB chunks, resuming on HTTP 308. Captions and thumbnails stay multipart. A missing Location is `RESUMABLE_SESSION_MISSING`. A 308 that does not advance is `RESUMABLE_STALLED`. Selftest passed locally with a fake transport. Actions was not re-run.
- Flag: runs 281-286 added successive snippet/artifact gates. That loop is diminishing. Do not add another local metadata check unless a documented provider reject is still ungated.

## Run 286 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now counts the `videos.insert` tag budget: a space in a tag adds the two wrapping quotes, and each comma between tags counts. A raw sum under 500 can still be `invalidTags`. Inspect stays HOLD_LOCAL. Execute raises METADATA_REJECTED before the token refresh. Q1 tags budget to 152 and still pass. Selftest passed locally. Actions was not re-run.

## Run 285 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now refuses overlapping caption cues and a PNG that has an IHDR but no IEND chunk. Inspect stays HOLD_LOCAL. Execute raises ARTIFACT_REJECTED before the token refresh. `videos.insert` now sets `defaultLanguage` and `defaultAudioLanguage` to `en`, matching `captions.insert`. Q1 captions.srt (103 cues) and thumbnail.png pass. Selftest passed locally. Actions was not re-run.

## Run 284 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now refuses an empty title, a title containing `<` or `>`, a caption cue that is unparseable or not forward, cues out of order, and a last cue more than one second past a probed master. Inspect stays HOLD_LOCAL. Execute raises ARTIFACT_REJECTED or METADATA_REJECTED before the token refresh. Q1 captions.srt (103 cues) passes without a local master. Selftest passed locally. Actions was not re-run.

## Run 283 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now refuses a present thumbnail that is not a PNG, is over 2MB, or is under 640x360, a present captions.srt that is not UTF-8 or has no cue timestamp, and a pin comment over 10000 characters. Inspect gate is HOLD_LOCAL. Execute raises ARTIFACT_REJECTED before the token refresh. A missing thumbnail or caption stays missing. An artifact refusal does not write upload_state.json.
- Q1 captions.srt (103 cues) passes when thumbnail.png is absent. Selftest passed locally. Actions was not re-run.

## Run 282 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now reads granted scopes after refresh and raises `SCOPE_INSUFFICIENT` before `videos.insert` when caption or thumbnail scope is missing. An upload-only token cannot create a private video that then loops on caption failure. A scope refusal does not write `upload_state.json`.
- Required consent scopes are documented as `youtube.upload` plus `youtube.force-ssl`, or the full `youtube` scope. Analytics scope remains collect-only. Selftest passed locally. Actions was not re-run.

## Run 281 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now refuses a title over 100 characters, a description over 5000, more than 12 tags, tags whose characters sum over 500, or a tag with a comma or angle bracket. Inspect gate is HOLD_LOCAL. Execute raises METADATA_REJECTED before the token refresh and refuses a non-private privacy status.
- Tags are no longer silently sliced to 12. Q1 publish copy passes the new limit. Selftest passed locally. Actions was not re-run.

## Run 280 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- Upload identity no longer includes export mtime. The same bytes keep the same fingerprint after rematerialize.
- A persisted video id with a matching fingerprint and incomplete caption, thumbnail, or failed comment is gate RESUME. Execute retries those artifacts and does not upload a second video.
- A matching finished upload stays HOLD_IDEMPOTENT. A different fingerprint stays HOLD_FINGERPRINT_MISMATCH and execute refuses EXISTING_VIDEO_FINGERPRINT_MISMATCH.
- Selftest passed locally. Actions was not re-run.

## Run 279 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now exits non-zero with `POST_UPLOAD_INCOMPLETE` when caption, thumbnail, or requested comment upload fails after a provider video id exists. The video id and any existing `uploaded_at` stay in `upload_state.json`.
- `youtube-production.yml` persists that state even when the execute step fails. A same-dispatch `collect_feedback` is skipped because the 7-day window cannot be due. Selftest passed locally. Actions was not re-run.

## Run 278 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now copies an existing `uploaded_at` onto a resumed upload. A missing stamp stays missing. A fresh upload writes the same stamp on `video_upload.uploaded_at` and `uploaded_at`. Selftest passed locally. Actions was not re-run.

## Run 277 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_feedback.py` now refuses a collect until `upload_state.json` has `video_upload.uploaded_at` or `uploaded_at` at least 7 days old. Missing time is `OBSERVATION_WINDOW_UNKNOWN`. An earlier time is `OBSERVATION_WINDOW_NOT_DUE`. Neither path writes COLLECTED. Selftest passed locally. Actions was not re-run.

## Run 276 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube-production.yml` now accepts `collect_feedback` (default false). Collect-only skips media materialize, runs `youtube_feedback.py --execute`, then writes experiment state. It commits feedback only when gate is COLLECTED. It does not invent a baseline or decision.
- Authenticated dispatches still fail closed in `oauth_preflight.py` before media or provider calls. Selftest passed locally. Actions was not re-run.

## Run 275 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `experiment_loop.py` now loads `experiment_decision.json` only after a numeric comparison. Valid keep/discard/retest with a reason and a non-invented source sets action `DECISION_RECORDED` and fills `result`. A missing, invented, or pre-comparison file stays pending.
- No Q1 decision file was written. Selftest passed locally.

## Run 274 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `experiment_loop.py` now computes one numeric primary-metric delta when a documented baseline and one collected value exist. Action is `COMPARED`. Decision stays `pending`. `result` stays null.
- A missing, non-numeric, or conflicting primary metric is `COMPARE_BLOCKED_METRIC`. `complete.py` requires a keep/discard/retest decision, so a delta cannot mark COMPLETE.
- No Q1 baseline file was written. Selftest passed locally.

## Run 273 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `experiment_loop.py` now loads `experiment_baseline.json` when present. Invalid or invented sources stay `COMPARE_BLOCKED_NO_BASELINE`. A valid file becomes `COMPARE_READY` and still does not choose keep/discard.
- No Q1 baseline file was written. There is no prior observation to cite.
- Selftest passed locally.

## Run 272 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `tools/oauth_preflight.py` now runs before ffmpeg and materialize when `youtube-production.yml` is dispatched with execute=true. Missing or blank secrets exit 3 and print names only.
- Dry-run path is unchanged. Selftest passed locally.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 0.5 | 0.5 | Audience omission is now a local hold; secret setup still one-time |
| Automated steps | 135 | 136 | job timeout covers chunk retry; no upload ran |
| Videos produced | 0 | 0 | no provider write |

## Active constraints
- Do not upload q1-media-r249 q1-master.mp4 as the finished export
- Do not upload a description that drops drafted chapter lines. A missing chapters.md stays missing.
- Do not omit status.containsSyntheticMedia. Q1 vo_origin kind is generated, so the flag is true. Do not invent a kind.
- Do not omit status.selfDeclaredMadeForKids. This channel is not_made_for_kids, so the flag is false. Do not default a missing flag to false. Do not invent made_for_kids.
- Do not rebase a shallow provider-state commit without unshallow. Do not force-push that state.
- Do not abort materialize merely because that banned asset is present in the r249 release
- Finished local export is q1-media-r253 q1-master-r253.mp4 (328.40s, sha256 4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546)
- Do not re-encode while q1-media-r253 exists
- Do not scaffold Q2
- Do not restore the stub sentence `No upload happened`
- Do not dispatch youtube-production.yml with execute=true until the three OAuth secrets exist
- Do not remove the oauth_preflight step or move it after materialize
- Do not regenerate thumbnail.png, chapters.md, or captions.srt while source checksums are unchanged
- Do not invent experiment_baseline.json for Q1
- Do not treat COMPARED or a numeric delta as a keep/discard
- Do not invent experiment_baseline.json for Q1
- Do not invent experiment_decision.json for Q1
- Do not treat a decision file written before COMPARED as a result
- Do not treat a collect before uploaded_at plus 7 days as COLLECTED
- Do not invent uploaded_at
- Do not drop an existing uploaded_at when an upload resumes
- Do not treat a failed caption or thumbnail as a finished upload
- Do not skip persisting upload_state.json after a post-upload failure
- Do not collect feedback in the same dispatch as execute
- Do not treat HOLD_IDEMPOTENT as the retry path for a failed caption or thumbnail
- Do not put export mtime back into the upload fingerprint
- Do not upload a second video when a provider video id already exists
- Do not silently slice tags to 12
- Do not call videos.insert with a title over 100 characters, a description over 5000, or tags over the provider limit
- Do not upload with privacy other than private
- Do not call videos.insert with only youtube.upload when captions.srt still needs force-ssl
- Do not write upload_state.json for a SCOPE_INSUFFICIENT refusal
- Do not call videos.insert with an empty title or a title containing < or >
- Do not call videos.insert when caption cues overlap or a thumbnail PNG has no IEND chunk
- Do not drop defaultLanguage or defaultAudioLanguage from videos.insert
- Do not treat a raw tag character sum as the videos.insert 500 limit when a tag contains a space
- Do not put videos.insert back on multipart
- Do not treat HTTP 500/502/503/504 on a chunk PUT as a permanent failure
- Do not start a second videos.insert because a 503 hid the session
- Do not treat a session POST 503 with no Location as a permanent failure
- Do not POST videos.insert again when that 503 already returned Location
- Do not treat HTTP 408 or 429 on a chunk PUT as a permanent failure
- Do not add another snippet micro-gate unless a documented provider reject is still ungated
- Do not treat a 401 on a chunk PUT as a reason to start a second videos.insert
- Do not refresh into a second videos.insert when Location is already present
- Do not treat a 401 on captions, thumbnail, or pin comment as a reason to start a second videos.insert
- Do not treat an empty or unchanged post-upload refresh as success
- Do not treat a 200/201 with an empty body as a missing video if the session can still return the id
- Do not start a second videos.insert because the completion body was dropped
- Do not start a second videos.insert when a 200/201 follow-up returns 404 or 410
- Do not invent a provider video id for RESUMABLE_COMPLETED_SESSION_GONE
- Do not treat HOLD_COMPLETED_WITHOUT_ID as a retry of videos.insert
- Do not send a non-final resumable chunk from an offset that is not a multiple of 256 KiB
- Do not add another upload HTTP status variant unless a live execute returned that status
- Do not bare-push provider state; retry a non-fast-forward rejection and do not force-push
- Do not re-open Q1 Description edited or First comment approved; those boxes are already checked
- Do not restore the 20-minute production job timeout or a 600-second chunk PUT. A killed runner drops the video id.
