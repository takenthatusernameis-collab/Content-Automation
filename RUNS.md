# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-10-02T03:25:00Z — Run 258

- **Objective:** Stop the page named as Q1 remaining labor, and the production board, from sending the operator back to a new recording.
- **Inspected:** STATE/NEXT/RUNS after Run 257. next_action and session pages already say upload-blocked. `docs/gate_machine.md` still opened with "remaining labor is a local file at the DROP path" and a microphone/TTS block. `pipeline_status.py` still printed DROP for missing local VO on this packet. Releases not re-downloaded.
- **Action taken:** Rewrote the gate_machine opening and moved record/TTS under "only if releases are missing". pipeline_status Q1 detail is PUBLISH / do not record. selftest locks that line and keeps DROP for other packets. Did not edit publish.md. Did not re-encode. Did not upload. Did not scaffold Q2.
- **Result:** selftest PASS. Live pipeline_status on Q1 prints PUBLISH, not DROP. Automated steps 98 -> 99. Videos published stay 0. Packet status stays ready_for_vo. Human minutes stay 2.0.
- **Verification status:** selftest PASS observed. pipeline_status output observed on the live packet.
- **Important discovery:** Run 257 closed human_session, agent_session, and next_action, but queue_status still points at gate_machine.md, and that page still started with a record block.
- **Blocker:** YouTube OAuth still absent. Human must edit publish.md description and approve the pin comment.
- **Recommended next action:** Human-edit publish.md (delete the No upload happened sentence, check Description edited and First comment approved). Copy q1-master-r253.mp4 only onto export/master.mp4. Set OAuth. Do not record again.

## 2026-10-02T02:20:00Z — Run 257

- **Objective:** Stop the live-job pages from sending the operator back to recording after the take and padded master already exist.
- **Inspected:** STATE/NEXT/HANDOFF/RUNS after Run 256. human_session and agent_session still said remaining labor is the DROP file. next_action returned record-vo for ready_for_vo. Releases `q1-media-r253` (2026-10-01T19:18:04Z) and `q1-media-r249` still listed.
- **Action taken:** Rewrote both live-job sections and step 7 to the publish.md stub edit. next_action returns upload-blocked for this packet only. hint upload-blocked names the fetch and the sentence to delete. Did not edit publish.md. Did not re-download. Did not re-encode. Did not upload. Did not scaffold Q2.
- **Result:** selftest PASS. Q1 no longer routes to record-vo. Automated steps stay 98. Videos published stay 0. Packet status stays ready_for_vo. Human minutes estimate 2.5 -> 2.0 (delete one sentence and check two boxes; OAuth still manual).
- **Verification status:** selftest PASS observed. Release tags listed, not re-downloaded. next_action special case present in tools/next_action.py.
- **Important discovery:** Runs 254–256 closed the truncated-master copy, but the front-door pages still treated a missing local DROP as the job. That loop is the repeated stall.
- **Blocker:** YouTube OAuth still absent. Human must edit publish.md description and approve the pin comment.
- **Recommended next action:** Human-edit publish.md (delete the No upload happened sentence, check Description edited and First comment approved). Copy q1-master-r253.mp4 only onto export/master.mp4. Set OAuth. Do not record again.

## 2026-10-02T01:20:00Z — Run 256

- **Objective:** Stop the durable fetch page from installing the truncated master as the upload file.
- **Inspected:** STATE/NEXT/HANDOFF/RUNS/gate_machine/OPERATOR_HOLD after Run 255. Release list still has `q1-media-r253` and `q1-media-r249`. gate_machine.md already refuses the r249 master copy. HANDOFF still had `cp -n /tmp/q1-media/q1-master.mp4` onto `export/master.mp4` with the truncated sha as the expected checksum.
- **Action taken:** Rewrote the r249 fetch block to copy wav and PNGs only. Finished-master copy is `q1-master-r253.mp4` only. Did not re-download. Did not re-encode. Did not upload. Did not edit publish.md. Did not scaffold Q2.
- **Result:** Fetch instructions no longer place the 308.40s file on the upload path. Automated steps stay 98. Videos published stay 0. Packet status stays ready_for_vo. Human minutes stay 2.5.
- **Verification status:** Release tags listed (`q1-media-r253` published 2026-10-01T19:18:04Z). HANDOFF rewrite committed. Live master not re-downloaded this run.
- **Important discovery:** Run 254 closed the same copy on `docs/gate_machine.md` and left `HANDOFF.md` as the remaining copy-paste that would install the truncated sha.
- **Blocker:** YouTube OAuth still absent. Human must edit publish.md description and approve the pin comment.
- **Recommended next action:** Human-edit `publish.md` (remove "No upload happened", check Description edited and First comment approved). Download only `q1-master-r253.mp4` onto export/master.mp4. Set OAuth. Do not upload r249. Do not re-encode.

## 2026-10-02T00:20:00Z — Run 255

- **Objective:** Stop a stub description from looking upload-ready once OAuth exists.
- **Inspected:** STATE/NEXT/HANDOFF/RUNS after Run 254. Release `q1-media-r253` still lists `q1-master-r253.mp4`. Live `publish.md` still contains "No upload happened" and unchecked description/pin boxes. Upload hard-local checks ignored that copy.
- **Action taken:** `youtube_upload.py` fails closed on stub description markers and unchecked Human before upload items. selftest locks the stub fixture. Did not rewrite the human description. Did not re-encode. Did not upload. Did not scaffold Q2.
- **Result:** selftest PASS. Live packet dry-run gate FAIL / HOLD_LOCAL / publish_copy_approved FAIL (also missing local master). Automated steps 97 -> 98. Videos published stay 0. Packet status stays ready_for_vo.
- **Verification status:** selftest PASS observed. Live packet command observed HOLD_LOCAL. r253 asset listed, not re-downloaded.
- **Important discovery:** Word count treated the process note as a usable description, so the next operator step looked like OAuth only.
- **Blocker:** YouTube OAuth still absent. Human must edit publish.md description and approve the pin comment. Finished master remains `q1-media-r253`.
- **Recommended next action:** Human-edit `publish.md` description (remove stub sentences, check the two open boxes). Then download `q1-master-r253.mp4` onto export/master.mp4 and set OAuth. Do not upload r249. Do not re-encode.

## 2026-10-01T23:15:00Z — Run 254

- **Objective:** Stop the fetch page from installing the truncated master as the upload file.
- **Inspected:** STATE/NEXT/HANDOFF/BLOCKED/OPERATOR_HOLD/docs/gate_machine.md after Run 253. OAuth still absent. r253 remains the finished export.
- **Action taken:** youtube_upload refuses the r249 master sha and a probed export shorter than VO+20s. gate_machine fetch now copies r253 master only. selftest locks the sha and a 2s ffmpeg fixture. Did not re-encode. Did not upload. Did not scaffold Q2.
- **Result:** selftest PASS. Automated steps 96 -> 97. Videos published stay 0. Packet status stays ready_for_vo. Human minutes stay 2.5.
- **Verification status:** selftest PASS observed this run. Live Q1 file was not re-downloaded.
- **Important discovery:** Run 253 state pages said do not upload r249, but gate_machine.md still said copy that file onto export/master.mp4. ftyp alone would have accepted it.
- **Blocker:** YouTube OAuth absent (YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN).
- **Recommended next action:** On the publish machine, download q1-media-r253 q1-master-r253.mp4 only. Set OAuth, then python3 tools/youtube_upload.py PATH. Do not upload r249.

## 2026-10-01T19:20:00Z — Run 253

- **Objective:** Stop pointing at a re-encode. Produce the padded master the Run 251 lock described.
- **Inspected:** STATE/NEXT/RUNS/HANDOFF after Run 252. gh auth present. Release `q1-media-r249` checksums matched HANDOFF (wav and truncated master).
- **Action taken:** Copied wav and seven cards onto a local checkout (not git add). Left the truncated master aside. `assemble.py --execute` segmented encode. Did not bump status. Did not call YouTube. Did not scaffold Q2. Did not regenerate media.
- **Result:** export/master.mp4 is 328.40s, 6633603 bytes, 1920x1080 h264 + aac, ftyp and moov present. sha256 `4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546`. Private release `q1-media-r253` re-download matched. media_qa PASS. youtube_upload YOUTUBE_AUTH_REQUIRED. complete.py INCOMPLETE_PUBLISH. Automated steps stay 96. Videos published stay 0. Human minutes estimate 3.2 -> 2.5.
- **Verification status:** Observed duration 328.400000. Release re-download sha256 matched. Packet status in git stays ready_for_vo.
- **Important discovery:** pad_dur=20 plus segmented execute keeps the end screen on the live Q1 take, not only the synthetic fixture. r249 must not be the upload file.
- **Blocker:** YouTube OAuth absent (YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN).
- **Recommended next action:** On the publish machine, download `q1-media-r253` `q1-master-r253.mp4` (do not re-encode). Set OAuth, then `python3 tools/youtube_upload.py PATH`. Do not upload r249.

## 2026-10-01T18:25:00Z — Run 252

- **Objective:** Stop treating a killed mux as a master. Run 251 already locked finite apad. This run closes the header hole.
- **Inspected:** STATE/NEXT/RUNS/HANDOFF/FAILURES after Run 251. Live assemble.py already uses apad=pad_dur=20. Sandbox reminder: ffmpeg mux with bare apad was Killed; new.mp4 had no moov.
- **Action taken:** execute now requires mp4_header_ok on export/master.mp4 before deleting .segments. Failed mux leaves the work dir. Did not re-download. Did not bump status. Did not upload. Did not scaffold Q2.
- **Result:** Assemble is fail-closed on incomplete mp4. Automated steps stay 96. Videos published stay 0. Packet status stays ready_for_vo.
- **Verification status:** Code change on main. Live Q1 re-encode still not run in this sandbox (no DROP on this machine; gh not on PATH).
- **Important discovery:** Bare `[1:a]apad[a]` plus -shortest still hangs or is killed. pad_dur lock from Run 251 is necessary but not sufficient if the process dies mid-mux.
- **Blocker:** YouTube OAuth absent. Finished export still needs assemble --execute on a checkout that has DROP + cards, after moving the truncated r249 master aside.
- **Recommended next action:** On a checkout with wav and cards, move truncated master aside, run assemble.py --execute, confirm duration is VO+20 and ftyp present. Do not upload r249 master. Do not regenerate.

Earlier runs remain in git history. Run 251 and earlier summaries are in prior commits.
