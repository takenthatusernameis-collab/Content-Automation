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
