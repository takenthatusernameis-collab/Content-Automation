## Run 298 — a shallow rebase would still drop the video id
- **Tried:** Run 297 retried a rejected push with fetch and rebase. The production workflow checks out with actions/checkout@v4, which defaults to fetch-depth 1.
- **Evidence:** A shallow clone does not contain the merge base once origin/main moves. `git rebase origin/main` then fails, `push_with_retry` raises STATE_PERSIST_REJECTED, and the provider video id stays only on the runner. The next execute can insert again.
- **Result:** A rejected push now checks `git rev-parse --is-shallow-repository`. A shallow clone is unshallowed before fetch and rebase. A failed rebase is aborted. No force-push. Selftest covers both a full clone and a shallow clone. Actions was not re-run.
- **Avoid:** Restoring a rebase that assumes a full history. Force-pushing provider state. Another HTTP status variant without a live execute status. Another run that only restates the OAuth secret hold.

## Run 297 — a rejected git push would drop the video id
- **Tried:** Runs 279-296 kept the provider video id in upload_state.json, then the workflow pushed once. A non-fast-forward rejection left that id only on the runner, so the next execute could insert again. The Q1 board also still told the operator to check boxes that are already checked.
- **Result:** Persist classifies state, retries a rejected push after fetch and rebase, and does not force-push. Board copy no longer re-opens Description edited or First comment approved.
- **Avoid:** Restoring a single `git push origin HEAD:main`. Force-pushing provider state. Re-opening the approved Q1 boxes. Another HTTP status variant without a live execute status. Another run that only restates the OAuth secret hold.

## Run 296 — unaligned resume looked like progress, and the status loop is suspicious
- **Tried:** Runs 281-295 each added a local snippet gate or an HTTP status variant on the resumable uploader. The publish gate stayed the missing OAuth secrets. A 308 Range of `bytes=0-99` would resume at byte 100 and send the next chunk.
- **Evidence:** YouTube requires every non-final chunk to be a multiple of 256 KiB and to start on that boundary. An unaligned PUT is a 400, not a stored chunk. The next execute would open another videos.insert. The same runs never saw a live status; they kept extending the client anyway.
- **Result:** `sendable_offset()` refuses that resume. The loop raises `RESUMABLE_STALLED` with `unaligned_offset` and does not send the next chunk. Selftest covers a 308 of `bytes=0-99` and asserts one POST and one PUT. Status-variant work is flagged. Do not add another unless a live execute returned that status.
- **Avoid:** Sending the next chunk from an unaligned Range. Treating Runs 281-295 as a reason to invent the next status code. Restating the OAuth hold as the only work.

## Run 295 — a finished upload with a gone session looked retryable
- **Tried:** Run 294 queried the session once when a 200/201 body had no id. A follow-up 404 or 410 still raised `RESUMABLE_MISSING_VIDEO_ID` or the raw status, and the workflow refused to commit state without a provider video id.
- **Evidence:** YouTube's resumable guide uses 404 for an expired session URI. The Google Data resumable protocol says a later PUT to a completed session returns 410 Gone. Either response after an accepted last byte means the video can exist and the id is no longer on that session. The next execute would open another videos.insert.
- **Result:** That follow-up is `RESUMABLE_COMPLETED_SESSION_GONE`. Execute writes `completed_without_id` without inventing an id. Inspect and execute refuse a matching fingerprint with `HOLD_COMPLETED_WITHOUT_ID`. The workflow commits that hold. Selftest covers a 410 after an empty 201 and asserts one POST.
- **Avoid:** Treating 404 or 410 after a completing 200/201 as a missing video. Starting a second videos.insert to recover an id the session can no longer return. Inventing a provider video id.

## Run 294 — empty 201 body looked like a missing video
- **Tried:** Runs 287-293 treated a 200/201 from the last chunk as the video resource and raised `RESUMABLE_MISSING_VIDEO_ID` when the body had no id.
- **Evidence:** The resumable protocol puts the resource in that response. A dropped body still means the server accepted the last byte. The next execute had no video id, so it would open another videos.insert.
- **Result:** `_video_from_complete()` queries the same session once and uses that id. A query that is not 200/201 stays `RESUMABLE_MISSING_VIDEO_ID`. Selftest covers an empty 201 followed by a status query that returns the id, and asserts one POST.
- **Avoid:** Treating an empty completion body as proof the video was not created. Starting a second videos.insert to recover an id the session can still return.

## Run 293 — post-upload 401 was still permanent

Run 292 refreshed a 401 only on the resumable master. Caption, thumbnail, and pin-comment calls still raised the raw 401. An access token can expire during a multi-minute upload, so the next execute would see a video id and then fail the artifacts. Fixed by refreshing and retrying the artifact call only. Do not treat that 401 as a second videos.insert.

## Run 289 — a 308 without Range was treated as a received chunk
- **Tried:** Run 287 resumed a chunk 308 from the Range header, and used `end+1` when Range was missing.
- **Evidence:** The YouTube resumable guide says a 308 with no Range means nothing has been uploaded. The fallback would send the next chunk past bytes the server does not have.
- **Result:** `received_offset()` returns None when Range is omitted. The loop restarts at byte 0 and stalls after three missing-Range responses. Retry-After is honored, capped at 30 seconds. Selftest covers a 308 with no Range followed by a Range that advances.
- **Avoid:** Restoring the `end+1` fallback for a missing Range. Treating that 308 as proof the chunk was stored.

## Run 283 — thumbnail and caption drafts could fail only after videos.insert

- **Tried:** Runs 279-282 made post-upload failure resumable and refused missing caption scope and invalid snippets before insert.
- **Evidence:** `execute_upload()` called `videos.insert` whenever the local gate was READY, then `thumbnails.set` and `captions.insert`. YouTube rejects thumbnails over 2MB, non-image bytes, and images under 640px wide, and rejects a caption file with no cue. Those checks were absent.
- **Result:** `artifact_block_reason()` is a hard local check. Execute raises `ARTIFACT_REJECTED` before the token refresh. Missing files stay missing. Selftest covers non-png, undersize, oversize, missing timestamp, valid cue, and a 10001-character pin comment.
- **Avoid:** Calling videos.insert with a present thumbnail.png that is not a PNG, is over 2MB, or is under 640x360. Calling videos.insert with a captions.srt that has no `-->` cue. Writing upload_state.json for an artifact refusal. Regenerating Q1 thumbnail.png or captions.srt while source checksums are unchanged.

## Run 282 — upload-only scope would create an uncaptioned video
- **Tried:** The upload contract treated `youtube.upload` as sufficient for the production path that also sends captions.
- **Evidence:** `captions.insert` accepts `youtube.force-ssl` or `youtube`, not `youtube.upload`. `docs/youtube_integration.md` told the operator to use the minimum upload scope. A 403 after `videos.insert` would persist the video id and then loop `POST_UPLOAD_INCOMPLETE`.
- **Result:** Execute reads tokeninfo scopes and raises `SCOPE_INSUFFICIENT` before insert. The refusal does not write `upload_state.json`. Selftest covers upload-only, upload+force-ssl, and full youtube.
- **Avoid:** Creating the refresh token with only `youtube.upload`. Treating a later caption 403 as a reason to upload a second video. Writing upload state for a scope refusal.

## Run 280 — idempotent gate blocked the post-upload retry and mtime could duplicate the video
- **Tried:** Run 279 saved the provider video id after a caption or thumbnail failure and told the next run to execute again.
- **Evidence:** `inspect_upload()` set `HOLD_IDEMPOTENT` whenever the fingerprint matched, and `main()` returned 2 before `execute_upload()`. `fingerprint()` included `st_mtime`. Actions materialize copies the same r253 bytes onto a new mtime.
- **Result:** Resume is `RESUME_POST_UPLOAD`. A finished match stays `HOLD_IDEMPOTENT`. A different content hash is `HOLD_FINGERPRINT_MISMATCH` and execute refuses a second insert. Fingerprint uses sha256 of the export.
- **Avoid:** Treating HOLD_IDEMPOTENT as the caption retry. Putting mtime back into the upload fingerprint. Uploading again because the persisted fingerprint does not match a rematerialized file.

# FAILURES

## Run 276 — feedback fetch stayed a manual CLI after upload
- **Tried:** Runs 219 and 271 made `youtube_feedback.py --execute` and collected metrics visible to the learning gates. The production workflow persisted upload state and stopped.
- **Evidence:** `youtube-production.yml` had no collect input. A later video would still need a human to run the feedback CLI after secrets exist.
- **Result:** `collect_feedback` defaults off. Collect-only skips media materialize, fetches only through `--execute`, and commits feedback only when gate is COLLECTED. Not dispatched.
- **Avoid:** Another manual-only feedback step. Dispatching collect_feedback before a provider video id exists. Inventing metrics, a baseline, or a decision because the input exists.


## Run 271 — collected feedback was invisible to the learning gates
- **Tried:** Runs 219-220 built dry-run feedback and experiment adapters. `inspect_feedback()` always left metrics None, and both `experiment_loop.py` and `complete.py` used that field.
- **Evidence:** Local inspection of those functions. A COLLECTED `feedback_state.json` was not an input. Selftest only covered the empty-metrics hold.
- **Result:** `collected_metrics()` is the only evidence path. Mismatched ids and dry-run files stay HOLD_NO_EVIDENCE. Matching collected rows are READY_TO_COMPARE and still pending.
- **Avoid:** Reading `inspect_feedback()["metrics"]` as observed evidence. Inventing a keep/discard because a fetch exists. Another run that only reprints the OAuth hold.


## Run 270 — materialize aborted because the banned master was present
- **Tried:** Run 269 added a workflow_dispatch production path and assumed `tools/materialize_q1_release.py` could fetch r249 wav/cards plus the r253 master.
- **Evidence:** GitHub Actions run 36982959831 (job 110761451601) failed at Materialize verified Q1 media with `RuntimeError: refuse known-truncated r249 q1-master.mp4`. The Actions token downloaded the release. The guard treated the expected banned asset as a fatal fetch error before copying wav, cards, or the r253 master.
- **Result:** The guard now ignores that known sha in the r249 download, refuses an unexpected r249 master sha, and still refuses installing the banned sha as `export/master.mp4`.
- **Avoid:** Restoring the presence-only abort. Copying r249 `q1-master.mp4` onto `export/master.mp4`. Treating this as an OAuth failure.

## Run 265 — thumbnail left as a brief only
- **Tried:** Runs 254-264 restated the publish hold after the description, captions, and chapters existed. thumbnail.md already had the on-image line. No PNG, and the uploader could not name one.
- **Result:** thumbnail_draft.py writes thumbnail.png and an unapproved review. Q1 card committed. thumbnails.set stays uncalled.
- **Avoid:** Another run that only reprints the publish hold. Checking the design or publish boxes from an agent run. Regenerating the PNG while the on-image text matches. Calling the card a design sign-off.

## Run 264 — chapter timestamps left unassigned
- **Tried:** Runs 254-263 kept restating the publish hold after the description, captions, and spot-check sheet already existed. No chapter list was drafted.
- **Result:** chapter_draft.py writes chapters.md. Q1 lines are in the description draft. Approval stays unchecked.
- **Avoid:** Another run that only reprints the publish hold. Checking the description box from an agent run. Regenerating chapters while the srt checksum matches. Calling the times ASR.

## Run 263 — caption page still assigned inventing the srt
- **Tried:** Run 261 wrote captions.srt and Run 262 wrapped lines, but captions.md still said invent the timed file and split long lines.
- **Result:** captions_review.md is the human path (five checkpoints). The invent-srt line is gone. Spot-check stays unchecked.
- **Avoid:** Another run that only reprints the publish hold. Checking the spot-check or publish boxes from an agent run. Regenerating the srt while the wav checksum matches.

## Run 261 — caption timing left as a blank task
- **Tried:** Runs 254-260 kept restating the publish hold. captions.md still said do not invent an SRT, so every future video would need a human to time 900+ words.
- **Result:** caption_align.py writes a labeled draft from the DROP wav. Q1 captions.srt exists. Approval stays unchecked.
- **Avoid:** Calling the draft Whisper or uploaded captions. Checking publish boxes from an agent run. Another run that only reprints the hold.

## Run 260 — compose instruction survived on the human pages
- **Tried:** Run 259 updated next_action and hint, then left gate_machine, human_session, agent_session, HANDOFF, and pipeline_status telling the operator to delete `No upload happened`.
- **Result:** Those surfaces now name the two open boxes and forbid restoring the stub. publish_brief refuses the Q1 packet.
- **Avoid:** Another printer-only pass that does not change the human action. Checking the boxes from an agent run. Restoring the stub. Flag if Runs 261+ only restate this hold.

## Run 259 — stub description treated as a compose task
- **Tried:** Runs 254–258 kept telling the operator to delete `No upload happened` and write the description. The script, title, tags, and pin draft already existed. That loop did not move the packet.
- **Result:** Description is now a drafted viewer paragraph. Open boxes stay unchecked so approval is still human. next_action must not tell the operator to delete a sentence that is gone.
- **Avoid:** Restoring the stub sentence. Checking Description edited or First comment approved from an agent run. Another printer-only run while those boxes are the remaining human edit.

## Run 257 — front door still said record
- **Tried:** Treating the truncated-master copy fix as enough. human_session and agent_session still said remaining labor is the DROP file, so the next agent would synthesize again.
- **Result:** Those pages and Q1 next_action now point at the publish.md review.
- **Avoid:** Restoring "remaining labor is a new recording" while q1-media-r249 and q1-media-r253 exist.

Earlier failures remain in force in prior commits.
