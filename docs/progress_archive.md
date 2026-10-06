# PROGRESS ARCHIVE

Older sections. Do not delete. Do not paste back into PROGRESS.md.

## Run 322 (2026-10-04T21:12:00Z)
- Script anti-slop phrases are now a reusable report (`tools/quality_scan.py`) instead of a reread of docs/content_quality.md. Estimated human minutes saved on each later script review: about 4, if the report is clear. Q1 was already clear, so this video does not change. Automated steps: 139 plus this report. Videos published stay 0. No provider write.
- Instruction-only runs are now visible as STALL_INSTRUCTION_LOCK. That does not reduce minutes until the three YouTube secrets exist.

## Run 320 (2026-10-04T19:30:00Z)

## Run 321 — 2026-10-04T20:15:00Z
fill-idea no longer tells the operator to paste idea.md by hand. Estimated human minutes for a future blank idea.md: one dry-run plus one --write, not a field copy. Automated steps unchanged (the writer already existed). Videos published stay 0. No provider write. Do not restore the hand paste. Do not add a YouTubeAPIError reason without a live_status line.

- Blank idea.md after scaffold can be filled by `tools/apply_idea.py --write` from the locked queue paste. Reviewed idea.md is refused. Estimated human minutes saved at each later scaffold: about 3 (no hand paste). No video produced. Videos published stay 0. Automated steps stay 139 plus this fill command. Q2 was not scaffolded.


## Run 319 (2026-10-04T18:14:00Z)
- Locked problem lines for Q2-Q5 in the topic queue. Future idea briefs reprint them. Estimated human minutes saved at each later scaffold: about 5, once Q1 has shipped. No video produced. Videos published stay 0.
## Run 318
The topic queue no longer tells the next agent to scaffold `002-` after Q1 already occupies that id. `queue_contract.py` fails if that sentence returns. Estimated human minutes stay 0.5 until secrets exist. Automated steps stay 139. Videos published stay 0. No provider write. No Studio sentence added.

## Run 317
The Studio-handoff loop is now a printed flag, and the end-screen reserve in that handoff is the same `timeline.END_SCREEN` value the encode uses. Estimated human minutes stay 0.5 until secrets exist. Automated steps stay 139. Videos published stay 0. No provider write. Do not add another Studio sentence while `STALL_OAUTH_AND_STUDIO` is set.

## Run 316 — 2026-10-04T11:20:00Z
- Studio end-screen steps now sit in `studio_pin.md` with the pin URL. Estimated human search after upload drops by one Studio menu hunt per video. Still two Studio clicks (pin, end screen). Videos published stay 0. No new upload reason.

## Run 315 — 2026-10-04T10:12:00Z
- Studio pin URL now persists as `studio_pin.md` beside the video id. Estimated human search after upload drops from reading an Actions log to opening one packet file. Still one Studio click. Videos published stay 0.

## Run 313
videos.insert now takes category and license from docs/channel.md instead of a hardcoded Education id. A missing channel file cannot invent category 27 or creativeCommon. Estimated human minutes stay 0.5 until secrets exist. Automated steps unchanged. Videos published stay 0. No provider write. Do not add a YouTubeAPIError reason without a live_status line.

## Run 311
The production dispatch can opt out of the approved first comment with `skip_comment`. Skip wins over `post_comment`. A posted comment is recorded `pinned: false` because the Data API insert does not pin; Studio pin stays a one-time human step. Estimated human minutes stay 0.5 until secrets exist. Automated steps unchanged. Videos published stay 0. No provider write. Do not add another upload HTTP status variant without a live execute status.

## Run 309
Write-path locks now run on every push via the selftest workflow, so a future agent does not have to remember `prove_locks.py` after a tool edit. Estimated human minutes stay 0.5 until secrets exist. Automated steps 138 -> 139. Videos published stay 0. No provider write. Do not map prove_locks in needed.py. Do not add a YouTubeAPIError reason without a live_status line.

## Run 308
Production checkout is now full history (`fetch-depth: 0`). A rejected provider-state push can rebase without a mid-job unshallow after the upload. Estimated human minutes stay 0.5 until secrets exist. Automated steps stay 138. Videos published stay 0. No provider write. Do not restore a depth-1 production checkout. Do not add a YouTubeAPIError reason without a live_status line.

## Run 307
New upload error reasons now fail the selftest unless a live execute recorded them. That stops the Run 281-306 status loop from growing on prose alone. Estimated human minutes stay 0.5 until secrets exist. Automated steps 137 -> 138. Videos published stay 0. No provider write. Do not add a YouTubeAPIError reason without a live_status line.

## Run 306
The caption processing wait now covers about 10 minutes instead of 60 seconds, so a normal 1080p processing delay does not force a second execute for the same caption. Estimated human minutes stay 0.5 until secrets exist; the saved dispatch is one future execute, not a per-video edit. Automated steps stay 137. Videos published stay 0. No provider write. Do not add another upload HTTP status variant without a live execute status.

## Run 305
The first caption write now waits until YouTube processingDetails is succeeded or terminated. A still-processing video is VIDEO_PROCESSING_NOT_READY and does not start a second insert. Estimated human minutes stay 0.5. Automated steps 136 -> 137. Videos published stay 0. No provider write. Do not add another upload HTTP status variant without a live execute status.

## Run 304
The post-write lock now passes on a checkout that already has Q1. A false prove_locks fail no longer hides a real write-path regression. Estimated human minutes stay 0.5. Automated steps stay 136. Videos published stay 0. No provider write. Do not add another upload HTTP status variant without a live execute status.

## Run 303
The production job now outlasts a slow chunk PUT, so a finished upload can persist its video id instead of being killed at 20 minutes. Chunk PUT timeout is 180 seconds. Estimated human minutes stay 0.5. Automated steps 135 -> 136. Videos published stay 0. No provider write. Do not add another upload HTTP status variant without a live execute status.

# PROGRESS

## Run 310 — one less dispatch after the first upload
- Approved pin comment posts on the same execute as the video, captions, and thumbnail.
- Estimated human minutes saved: one workflow dispatch and one wait for a second job, on every future video whose first-comment box is already checked.
- Videos published stay 0. OAuth secrets remain the publish gate.



## Run 302
`videos.insert` now refuses to start when `status.selfDeclaredMadeForKids` is missing. Channel designation is `not_made_for_kids`, so the flag is false. Estimated human minutes stay 0.5. Automated steps 134 -> 135. Videos published stay 0. No provider write. Do not add another upload HTTP status variant without a live execute status.

## 2026-10-03T20:20:00Z — Run 301
- Chapter lines drafted in chapters.md are now a fail-closed description check. A dropped or invalid list cannot reach videos.insert. Q1 already matched, so no publish copy was rewritten.
- Automated steps 133 -> 134. Videos published stay 0. Human minutes per video stay 0.5. The OAuth secret stall is unchanged and was not polled.

## Run 300 — 2026-10-03T19:20:00Z
- One-time OAuth setup research is now `tools/oauth_setup.py` (names and scopes only). Per-video human minutes stay 0.5. Videos published stay 0. Upload-status loop not extended.

# PROGRESS

Updated: 2026-10-03T15:20:00Z (Run 299)

## Latest measurable delta
- Run 298 automated steps: 132. Run 299: 133.
- New automated behavior: videos.insert discloses generated narration via status.containsSyntheticMedia, so the operator does not set the altered-content box in Studio.
- Human minutes per video remain 0.5. The remaining recurring human step is entering the three YouTube OAuth secrets.
- Videos published: 0. No provider write.

## Run 299
Generated narration now sets status.containsSyntheticMedia on videos.insert. Human narration sets false. Unknown origin fails before the token refresh. Estimated human minutes stay 0.5. Automated steps 132 -> 133. Videos published stay 0. No provider write. Do not add another upload HTTP status variant without a live execute status.

## Run 298
A shallow rejected push now unshallows, fetches, and rebases instead of failing with no merge base. No force-push. Estimated human minutes stay 0.5. Automated steps 131 -> 132. Videos published stay 0. No provider write. Do not add another upload HTTP status variant without a live execute status.


## Run 295
A finishing PUT whose session then returns 404 or 410 is `RESUMABLE_COMPLETED_SESSION_GONE`. The workflow commits `completed_without_id` and the next execute must not insert again. No provider video id is invented. Estimated human minutes stay 0.5. Automated steps 128 -> 129. Videos published stay 0. No provider write.

## Run 294
A finishing chunk that returns 200 or 201 without a video id now queries that session once. An empty body is not treated as a missing video and does not start a second videos.insert. Estimated human minutes stay 0.5. Automated steps 127 -> 128. Videos published stay 0. No provider write.

## Run 291
Caption, thumbnail, and pin-comment calls retry a transient 408/429/5xx or network error instead of failing the workflow after the video id exists. A 400 stays permanent. Estimated human minutes stay 0.5 until secrets exist; one avoided re-dispatch after the first upload. Automated steps 125 -> 126. Videos published stay 0. No provider write.

## Run 290
A session POST that returns 503 without Location is retried. A 503 that already returned Location is that session and is not a second videos.insert. Chunk 408 and 429 resume the existing session. Estimated human minutes stay 0.5. Automated steps 124 -> 125. Videos published stay 0. No provider write.

## Run 289
A 308 with no Range header now restarts the resumable upload at byte 0 instead of skipping the unconfirmed chunk. Retry-After is honored, capped at 30 seconds. Estimated human minutes stay 0.5. Automated steps 123 -> 124. Videos published stay 0. No provider write.

## Run 288
videos.insert now resumes a 500/502/503/504 or network error by querying the session (`bytes */size`) instead of aborting. Estimated human minutes stay 0.5. Automated steps 122 -> 123. Videos published stay 0. No provider write.

## Run 287
videos.insert now uses resumable upload (8 MiB chunks, 308 resume) instead of one multipart POST of the master. Captions and thumbnails stay multipart. Estimated human minutes stay 0.5. Automated steps 121 -> 122. Videos published stay 0. No provider write.

## Run 286
Tag lists now fail closed on the videos.insert keyword budget, not a raw character sum. Spaced tags count two wrapping quotes, and commas between tags count. Q1 tags still pass at 152. Estimated human minutes stay 0.5. Automated steps 120 -> 121. Videos published stay 0.

## Run 285
Overlapping caption cues and a PNG without IEND now fail before videos.insert. The insert body sets default audio and caption language to en so the later caption track matches. Q1 captions.srt and thumbnail.png still pass. Estimated human minutes stay 0.5. Automated steps 119 -> 120. Videos published stay 0.

## Run 284
Caption cue order and title characters are now a pre-insert gate. A backward cue, a cue past the probed master, an empty title, or a title with angle brackets cannot create a private video that then stays POST_UPLOAD_INCOMPLETE. Q1 captions.srt still passes. Estimated human minutes stay 0.5. Automated steps 118 -> 119. Videos published stay 0.

## Run 283
Thumbnail and caption drafts are now a pre-insert gate. A file YouTube will reject cannot create a private video that then stays POST_UPLOAD_INCOMPLETE. Estimated human minutes stay 0.5. Automated steps 117 -> 118. Videos published stay 0.

## Run 282
Caption scope is now a pre-insert gate. An upload-only token cannot create a private video that the caption step can never finish. Estimated human minutes stay 0.5 because the secret entry itself is unchanged; the first secret entry is less likely to need a second consent screen. Automated steps 116 -> 117. Videos published stay 0.

# PROGRESS

Updated: 2026-10-03T05:20:00Z (Run 290)

## Latest measurable delta
- Run 280 automated steps: 115. Run 281: 116.
- New automated check: provider snippet limits fail closed before token refresh. Tags are not silently sliced.
- Human minutes per video remain 0.5. The remaining recurring human step is entering the three YouTube OAuth secrets.
- Videos published: 0. No provider write.

## Run 281 — 2026-10-02T20:12:00Z
- Invalid YouTube snippet fields now fail locally before the token refresh. Q1 publish copy passes. No upload ran. Videos published stay 0.

## Run 280 — 2026-10-02T19:15:00Z
- A later execute can finish captions and thumbnail on the existing video id. Rematerialize no longer changes upload identity. No upload ran. Videos published stay 0.

## Run 279 — 2026-10-02T17:20:00Z
- A caption, thumbnail, or requested comment failure after a provider video id is now a failed job, and the upload state is still persisted. The same dispatch no longer collects feedback. No upload ran. Videos published stay 0.

## Run 278 — 2026-10-02T16:20:00Z
- Upload resume now keeps an existing uploaded_at. A caption or thumbnail retry can no longer erase the 7-day observation clock. No upload ran. Videos published stay 0.

## Run 277 — 2026-10-02T15:20:00Z
- Feedback collect now fails closed until the documented 7-day window. An early or undated upload cannot be stored as COLLECTED. No fetch ran. Videos published stay 0.

## Run 276 — 2026-10-02T14:20:00Z
- Production workflow can collect read-only feedback after a provider video id exists. Default remains off. Collect-only does not download media or upload. No fetch ran. Videos published stay 0.

## Run 275 — 2026-10-02T13:30:00Z
- Experiment ledger now records an explicit keep/discard/retest from `experiment_decision.json` after a numeric comparison. A delta still cannot decide by itself. No Q1 decision was written. Videos published stay 0.

## Run 274 — 2026-10-02T12:25:00Z
- Experiment ledger now computes one primary-metric delta from a documented baseline and collected rows. Decision stays pending. A delta cannot mark a video complete. Videos published stay 0.

## Run 273 — 2026-10-02T11:17:00Z
- Experiment ledger now accepts a documented baseline file and refuses an invented one. Comparison can start after a real fetch without a human designing the schema. Decision stays pending. Videos published stay 0.

## Run 272 — 2026-10-02T10:15:00Z
- Execute dispatch now refuses missing OAuth secrets before ffmpeg and media materialize. Dry-run path unchanged. Videos published stay 0.

## Run 271 — 2026-10-02T09:15:00Z
- Experiment and completion gates now read collected feedback metrics instead of the always-empty dry-run field. A real fetch will no longer look like HOLD_NO_EVIDENCE forever.
- Local selftest passed. Videos published stay 0. OAuth secrets remain the publish boundary.

## Run 270 — 2026-10-02T08:22:00Z
- Production workflow dry-run is now externally verified after the truncated-master skip. Actions run 36983196381 succeeded. Videos published stay 0.
- Automated materialize is no longer blocked by the expected r249 asset. Remaining publish gate is OAuth secrets only.

Updated: 2026-10-02T07:50:00Z

## Run 268
Selftest runner dependency fixed: GitHub Actions now installs ffmpeg, and Selftest Run 8 passed. Repository-side validation is green. No video published; provider authorization and runtime media access remain external.

Updated: 2026-10-02T07:55:00Z

## Run 267
Repository-side bottlenecks removed: durable Q1 release materialization, authenticated YouTube upload execution, resumable post-upload artifacts, authenticated Analytics/comment feedback reads, delegated approval policy, and a minimal selftest workflow. No video published; provider credentials and runtime media access remain external.

Updated: 2026-10-02T07:45:00Z

## Run 266
Approval-only human gates delegated to the automation agent. Q1 description and first-comment approvals completed. Thumbnail/caption sensory review remains evidence-gated because private binary/audio artifacts are inaccessible here. YouTube OAuth remains the external publish bottleneck. No video published.

## Run 265
Q1 thumbnail.png drafted from the locked on-image line (1280x720). Review stays unapproved. Uploader names it and sets uploaded=false. Automated steps 104. Videos published 0.

## Run 264
Q1 chapter lines drafted from script + captions.srt (6 chapters) and copied into publish.md. Boxes stay open. Automated steps 103. Videos published 0.

## Run 263
Q1 caption spot-check sheet written (5 checkpoints, 0 flagged). captions.md no longer assigns inventing the srt. Spot-check and publish boxes stay open. OAuth unchanged. Automated steps 102. Videos published 0.

## Run 261
Q1 captions.srt drafted from wav speech gaps (103 cues). Human still spot-checks. Publish boxes and OAuth unchanged. Automated steps 101. Videos published 0.

## Run 260
Stale "delete No upload happened" instructions removed from pipeline_status, gate_machine, human_session, agent_session, and HANDOFF. publish_brief cannot overwrite the Q1 draft. Human minutes stay 1.5. Videos published 0.

# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-10-03 Run 293 | 0.5 | 127 | post-upload 401 refreshes and retries the artifact; OAuth remains |
| 2026-10-02 Run 278 | 0.5 | 113 | resume keeps uploaded_at; OAuth remains |
| 2026-10-02 Run 277 | ~0.5 estimate | 112 | early collect cannot become evidence; OAuth still blocks publish and fetch |
| 2026-10-02 Run 276 | ~0.5 estimate | 111 | collect_feedback dispatch exists; OAuth still blocks publish and fetch |
| 2026-10-02 Run 275 | ~0.5 estimate | 110 | explicit decision file is loaded fail-closed; OAuth still blocks publish |
| 2026-10-02 Run 274 | ~0.5 estimate | 109 | numeric delta is automatic; keep/discard still pending; OAuth still blocks publish |
| 2026-10-02 Run 273 | ~0.5 estimate | 108 | baseline file is loaded fail-closed; OAuth still blocks publish |
| 2026-10-02 Run 271 | ~0.5 estimate | 106 | collected feedback visible to experiment/complete; OAuth still blocks publish |
| 2026-10-02 Run 265 | ~1.0 estimate | 104 | thumbnail PNG drafted; two publish boxes, caption spot-check, and OAuth remain |
| 2026-10-02 Run 264 | ~1.1 estimate | 103 | chapter lines drafted into the description; two publish boxes and OAuth remain |
| 2026-10-02 Run 263 | ~1.2 estimate | 102 | caption review is five checkpoints; two publish boxes and OAuth remain |
| 2026-10-02 Run 261 | ~1.5 estimate | 101 | caption draft from Selected VO; two publish boxes and OAuth remain |
| 2026-10-02 Run 260 | ~1.5 estimate | 100 | operator pages match the drafted description; two boxes and OAuth remain |
| 2026-10-02 Run 259 | ~1.5 estimate | 100 | description drafted; human checks two boxes; OAuth remains |
| 2026-10-05 Run 335 | ~1.4 estimate | 140 | first analytics collect waits for 7 video days plus 3-day lag; videos published stay 0 |
| 2026-10-02 Run 258 | ~2.0 estimate | 99 | pipeline_status and gate_machine stop the record loop; publish edit and OAuth remain |
| 2026-10-01 Run 253 | ~2.5 estimate | 96 | Padded master 328.40s on q1-media-r253; r249 truncated master must not be uploaded; OAuth still blocks publish |

These numbers are **estimates**, not stopwatch data. Earlier rows remain in prior commits.

## Capability additions
- Run 265: thumbnail_draft.py writes a non-approving 1280x720 PNG from thumbnail.md. Q1 file committed. Dry-run never calls thumbnails.set.
- Run 264: chapter_draft.py writes a non-approving YouTube chapter list from script WORDS and captions.srt. Q1 lines committed into chapters.md and the description draft.
- Run 263: caption_review.py writes a non-approving spot-check sheet from an existing srt. Q1 sheet committed. Human listens to checkpoints instead of all cues.
- Run 261: caption_align.py drafts captions.srt from packet DROP wav speech gaps and script WORDS. Refuses a missing wav. Not ASR. Q1 draft committed; spot-check stays open.
- Run 260: remaining operator surfaces no longer assign a compose step that is already done. Q1 publish.md cannot be force-stubbed.
- Run 259: publish.md no longer needs a human to compose the description. The human still must check Description edited and First comment approved. Agent must not check those boxes.
- Run 253: Live Q1 padded master exists. Duration 328.40s, sha256 `4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546`, private release `q1-media-r253`. Videos published stay 0.

- Run 262 (2026-10-02): uploader dry-run names captions.srt and refuses to claim captions.insert. One overlong Q1 caption line wrapped. Human caption edit is wording spot-check only. Estimated human minutes 1.5 -> 1.4. Videos published stay 0.
- Run 325: production dispatch refuses a missing or illegal packet path before materialize. Local selftest PASS. No upload.

## Run 331 (2026-10-05T08:20:00Z)
Playlist membership is now a skip-until-set step. After one human playlist id is written to `docs/channel.md`, later uploads can call playlistItems.insert instead of a per-video Studio add. Estimated human minutes saved after that id exists: about 2 per video. Until then the tool prints not_set and does not invent an id. Videos published stay 0. Automated steps stay 139 plus this skip command.
## Run 323 — 2026-10-04T21:20:00Z
ready_for_vo now fails closed on quality_scan hits. Estimated human review of those phrases on later packets drops from a remembered read to a status refusal. Q1 unchanged. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 324 — 2026-10-04T22:13:00Z
The production workflow packet is now a dispatch input defaulting to Q1. A later video can reuse the same job instead of a copied workflow. Q1 materialize stays path-locked. Estimated human minutes to add video 2's upload job later: about 20 avoided. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 326 — 2026-10-05T00:20:00Z
Unsourced spoken digits and survey hedges now refuse ready_for_vo. Estimated human minutes saved on each later script: about 5, because the status step catches the number instead of a remembered research read. Q1 was already clear, so this video does not change. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 327 — 2026-10-05T01:17:00Z
Shouted titles and an explicit thumbnail mismatch now refuse ready_for_vo. Estimated human minutes saved on each later title review: about 3, if the report is clear. Q1 was already clear, so this video does not change. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 328 (2026-10-05T05:13:00Z)
- Upload inspect now fails closed on the same quality, claim, and title hits that already block `ready_for_vo`.
- Estimated effect: one less class of bad packet that can reach videos.insert after a later script or title edit. No change to human minutes on Q1. Videos published stay 0.

## Run 329 (2026-10-05T06:15:00Z)
- Local-gate inflation is now a visible stall flag instead of a silent series of new scanners. Estimated agent minutes saved on the next runs: the rediscovery pass over Runs 326-328, about 10, if the flag is read first. No change to human minutes on Q1. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 336 — 2026-10-05T10:20:00Z
- Dry-run feedback plan now matches the first-7-calendar-day query. Removes a future wrong collect after secrets exist. Human minutes per video unchanged. Videos published stay 0.
- Run 334: a failed playlist insert now fails the production step and leaves a plan file, instead of exiting 0 with no record. Estimated human minutes saved after the first real upload: about 10, because Studio is not the only way to learn the video missed the series playlist. `not_set` still does not fail the upload. Videos published stay 0.

- Run 333: dry-run `scope` now matches the consent set, so copying that field no longer mints an upload-only token. The production job prints the existing idle flag before preflight. Estimated human minutes saved on the first token mint: about 20, if the operator copies `scope`. Videos published stay 0. No new refusal.

- Run 332: OAuth-idle is visible across eight subject changes, not only three matching topics. A mistyped playlist id now fails the production step (exit 2) without blocking `not_set`. Estimated agent minutes saved on the next rediscovery pass: about 15. Human minutes on Q1 unchanged. Videos published stay 0.

# PROGRESS

- Run 330: dry-run consent scope now includes force-ssl and analytics, not upload alone. Estimated human minutes saved on the first token mint: about 20, if the operator follows the dry-run line instead of the old scope field. Videos published stay 0. No new refusal.


## Run 338 — 2026-10-05T12:30:00Z
Persist no longer commits a COLLECTED analytics file that lacks the first-calendar-days stamp. Estimated effect: one less way a sliding or unstamped window becomes the comparison evidence after a later collect. Videos published stay 0. Human minutes on Q1 unchanged.

# PROGRESS

Updated: 2026-10-05T11:20:00Z

- Run 337: a collected analytics file no longer counts unless its window is the video's first 7 calendar days. Estimated agent minutes saved on the first comparison: about 15, by not treating a sliding or unstamped file as the observation. Human minutes per video unchanged. Videos published stay 0.

## Run 339 — 2026-10-05T14:20:00Z
The production stall printer no longer treats `No new scanner` as a local-gate run. Estimated agent minutes saved on the next runs: about 10, by not following a false `STALL_LOCAL_GATE` that Runs 336-338 kept rewriting. Human minutes per video unchanged. Videos published stay 0.

## Run 340 (2026-10-05T15:20:00Z)
- STATE.md dropped from 52418 bytes and 67 run sections to 12 sections. Older deltas are in docs/state_archive.md. Estimated agent minutes saved on the next truncated-fetch rediscovery: about 10, if the newest gate is read first. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 341 (2026-10-05T16:20:00Z)
- NEXT.md dropped from 28596 bytes to 12 notes. Older notes are in docs/next_archive.md. Estimated agent minutes saved on the next truncated-fetch rediscovery: about 10, if the newest locks are read first. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 342 — 2026-10-05T17:15:00Z
RUNS.md no longer truncates before the newest run log. Newest 12 entries stay in the live file. Older entries are in docs/runs_archive.md. Estimated agent minutes saved on the next runs: about 10, by not reconstructing the latest action from a cut fetch. Human minutes per video unchanged. Videos published stay 0.

## Run 343 — 2026-10-05T17:25:00Z
PROGRESS.md and FAILURES.md no longer sit past the known fetch cut. Newest 12 sections stay live. Older notes are in docs/progress_archive.md and docs/failures_archive.md. Estimated agent minutes saved on the next runs: about 10, by not reconstructing a cut lesson. Human minutes per video unchanged. Videos published stay 0.

## Run 344 — 2026-10-05T18:20:00Z
A killed upload no longer has to start a second videos.insert after Location exists. The session URI is written before the first chunk and committed. Estimated effect: one less duplicate private video on the first real execute if the runner dies mid-upload. Human minutes per video unchanged. Videos published stay 0.


Updated: 2026-10-05T17:25:00Z
## Run 345 — 2026-10-05T19:20:00Z
A dead resumable Location is no longer reused as an open session. 404 or 410 commits a hold and the next execute does not start another videos.insert. Estimated effect: one less duplicate private video if the first session expires before the runner can finish. Human minutes per video unchanged. Videos published stay 0.

## Run 346 — dead-session hold can be cleared after Studio shows no video
- Estimated human minutes per video: unchanged. Publish still blocked on OAuth.
- Automated step added: local hold release plus commit decision `commit_session_hold_released`. No provider write.
- Remaining manual steps: YouTube OAuth secrets, playlist id, Studio check before any hold release, pin after comment insert.
- Reliability: an expired Location no longer bricks later executes once a human confirms no video. The workflow cannot clear the hold by itself.


Updated: 2026-10-05T19:20:00Z


## Run 347 — 2026-10-05T21:15:00Z
- Early persist of an open resumable Location before the first chunk. Estimated save: one duplicate videos.insert if the runner dies after the session POST. Human minutes per video unchanged. Videos published stay 0.
- Automated step added: production execute sets UPLOAD_EARLY_PERSIST=1. Remaining manual gate: YouTube OAuth secrets and Studio check before any session-hold release.



## Run 348 — 2026-10-05T22:15:00Z
- Early persist of the provider video id before caption wait, and of dead-session holds before the step returns. Estimated save: one Studio check and one blocked re-execute if the job dies after videos.insert returns an id. Human minutes per video unchanged. Videos published stay 0.
- Automated step added: same UPLOAD_EARLY_PERSIST=1 path now covers the id and the holds. Remaining manual gate: YouTube OAuth secrets and Studio check before any session-hold release.



## Run 349 — 2026-10-05T22:35:00Z
- Caption, thumbnail, and comment status now early-persist before the next post-upload call. Estimated save: one duplicate captions.insert if the runner dies after the caption write. Human minutes per video unchanged. Videos published stay 0.
- Automated step added: `STALL_UPLOAD_EDGE` after four OAuth-idle upload-edge runs. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call while that flag is set.




## Run 351 — 2026-10-06T00:20:00Z
- The production export probe now refuses the known truncated r249 master and a present master that is not 30fps yuv420p h264 with stereo AAC at 48000 Hz. Estimated save: one private upload of the truncated file if execute starts before a human checks duration. Human minutes per video unchanged until secrets exist. Videos published stay 0.
- Automated step changed: existing `tools/export_probe.py` on the production job. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call while `STALL_UPLOAD_EDGE` is set.

## Run 350 — 2026-10-05T23:20:00Z
- A present master is now rejected before videos.insert unless it is 1920x1080 h264 with audio and at least 20s. Estimated save: one bad private upload and one Studio cleanup if the first execute used a wrong-size file. Human minutes per video unchanged until secrets exist. Videos published stay 0.
- Automated step added: `tools/export_probe.py` in the production workflow before upload gates. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call while `STALL_UPLOAD_EDGE` is set.
## Run 353 — 2026-10-06T02:20:00Z
- A present captions.srt is now rejected before captions.insert when a cue is empty, overlapping, reversed, longer than 42 characters, or past the selected wav. Estimated save: one private video with unreadable or late captions if execute starts before a human opens the srt. Human minutes per video unchanged until secrets exist. Videos published stay 0.
- Automated step added: `tools/caption_gate.py` on the production job after media QA. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call. Do not add another export-probe lock. Do not add another media checker.
## Run 354 — 2026-10-06T03:20:00Z
- Improvement: a repeated pre-upload probe is now machine-visible. `STALL_PREUPLOAD_PROBE` stops the next run from wiring another export, media, or caption checker while videos published stay 0.
- Efficiency: avoids another probe-only run. Estimated human minutes per video unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: stall watch contract PASS. Selftest PASS. No provider write.

