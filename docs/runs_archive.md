# RUNS ARCHIVE

Older run log entries. Newest first inside each move. Do not paste these back into RUNS.md. Do not delete this file.


## 2026-10-05T06:15:00Z — Run 329

- **Objective:** Stop the local-scanner loop from looking like progress while publish is still blocked.
- **Inspected:** STATE, NEXT, RUNS, stall_watch.py, Runs 326-328.
- **Action taken:** `stall_watch.py` now prints `STALL_LOCAL_GATE` when the last three deltas are OAuth-unpolled, videos published 0, and each mentions a scanner or content-rule gate. Contract covers that window and still requires a mixed window to stay clear. No new scanner. No dispatch. No Q2 scaffold.
- **Result:** Contract printed STALL WATCH CONTRACT PASS. Current STATE printed STALL_LOCAL_GATE. `python3 tools/selftest.py` printed SELFTEST PASS. Videos published stay 0.
- **Verification status:** completed for the flag and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Runs 326-328 repeated the same shape as the earlier upload-variant loop: a new local refusal, Q1 already clear, secrets still unset. The stall printer did not see it because it only matched Studio copy and instruction paste.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not add another scanner while STALL_LOCAL_GATE is set. Do not scaffold Q2. Do not re-encode.

## 2026-10-05T05:13:00Z — Run 328

- **Objective:** Fail closed on pre-VO content hits at upload time, not only at status promotion.
- **Inspected:** STATE, NEXT, RUNS, `youtube_upload.py` inspect gates, `title_scan.py`, `claim_scan.py`, `quality_scan.py`.
- **Action taken:** Added `content_rule_reason` and hard-local check `content_rules_clear`. Selftest fixture with `Primary: GRIND harder today` must not look upload-ready. Did not dispatch. Did not scaffold a packet. Did not rewrite Q1.
- **Result:** Q1 and sample `content_rule_reason` returned None. `python3 tools/selftest.py` printed SELFTEST PASS. Videos published stay 0.
- **Verification status:** completed for the upload content gate and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** ready_for_vo already refused these hits, but inspect_upload did not. A packet promoted before the scanners, or edited after promotion, could still reach DRY_RUN or execute.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring stall since before Run 270.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not scaffold Q2. Do not rewrite Q1. Do not re-encode.

## 2026-10-05T01:17:00Z — Run 327

- **Objective:** Fail closed on shouted titles and an explicit thumbnail mismatch before VO, without rewriting Q1 or retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, production title rules, `validate_packet.py`, `set_status.py`, Q1 titles.md and thumbnail.md.
- **Action taken:** Added `tools/title_scan.py` and `tools/title_scan_contract.py`. `set_status.py` refuses `ready_for_vo` on those hits. Selftest runs the contract. Did not dispatch. Did not scaffold a packet. Did not rewrite Q1 titles.
- **Result:** Contract printed TITLE SCAN CONTRACT PASS. Title scan printed clear for Q1. `python3 tools/selftest.py` printed SELFTEST PASS. Videos published stay 0.
- **Verification status:** completed for the title gate and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The production rule already banned all-caps title words except one acronym, but promotion only counted options and the 50-character option. A later packet could reach ready_for_vo with GRIND in the primary title, or with Matches title: No.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not scaffold Q2. Do not rewrite Q1 titles. Do not re-encode.

## 2026-10-05T00:20:00Z — Run 326

- **Objective:** Fail closed on unsourced spoken numbers and survey hedges before VO, without rewriting Q1 or retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, production_capabilities factual-claim gap, research_brief, set_status, Q1 script/research.
- **Action taken:** Added `tools/claim_scan.py` and `tools/claim_scan_contract.py`. `set_status.py` refuses `ready_for_vo` on those hits. Selftest runs the contract. Did not dispatch. Did not scaffold a packet. Did not invent a source.
- **Result:** Contract printed CLAIM SCAN CONTRACT PASS. Claim scan printed clear for Q1, the template, and the sample. `python3 tools/selftest.py` printed SELFTEST PASS. Videos published stay 0.
- **Verification status:** completed for the claim gate and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The production rule already said spoken numbers need a Sources line, but promotion only checked anti-slop phrases. A later script could reach ready_for_vo with an unsourced percentage.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not scaffold Q2. Do not invent a Q1 source line. Do not re-encode.

## 2026-10-04T23:20:00Z — Run 325

- **Objective:** Stop a bad production dispatch from reaching materialize or upload inspect.
- **Inspected:** STATE, NEXT, BLOCKED, `youtube-production.yml`, stall pattern on Runs 322-324.
- **Action taken:** Added `tools/packet_path.py` and `tools/packet_path_contract.py`. The workflow refuse step calls that tool. Selftest runs the contract and requires the workflow call. Did not dispatch. Did not scaffold a packet.
- **Result:** `python3 tools/packet_path_contract.py` printed PACKET PATH CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the path gate and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The previous refuse step accepted any `videos/<slug>` string, including a folder that had not been scaffolded.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not scaffold Q2. Do not re-encode.

## 2026-10-04T22:13:00Z — Run 324

- **Objective:** Stop the next video from needing a copied production workflow, without dispatching upload or scaffolding Q2.
- **Inspected:** STATE, NEXT, RUNS, stall_watch (clear), youtube-production.yml. OAuth secrets were not polled. Execute was not dispatched.
- **Action taken:** Added workflow input `packet` defaulting to the Q1 path. Job `PACKET` reads that input. Materialize stays on the Q1 path only. A path outside `videos/<slug>` is refused. Selftest locks the default and the materialize guard.
- **Result:** `python3 tools/selftest.py` printed SELFTEST PASS. Videos published stay 0.
- **Verification status:** completed for the workflow contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The upload job was still a Q1 constant, so video 2 would have required a workflow copy even after secrets exist.
- **Blocker:** GitHub Actions secrets YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, and YOUTUBE_REFRESH_TOKEN remain the publish gate. Not polled.
- **Recommended next action:** Store those three secrets, then dispatch youtube-production.yml with execute=true and skip_comment false. Leave packet at the default. Do not scaffold Q2. Do not point materialize at another packet.

## 2026-10-04T21:20:00Z — Run 323

- **Objective:** Bind the Run 322 anti-slop report to the status promotion so a later packet cannot reach ready_for_vo with those phrases.
- **Inspected:** STATE, NEXT, RUNS, quality_scan.py, set_status.py, content_quality.md. OAuth secrets were not polled. Execute was not dispatched.
- **Action taken:** set_status refuses ready_for_vo when scan_path finds a phrase. quality_scan_contract covers a slop refusal and a clear script. content_quality.md names that gate. Did not rewrite Q1 WORDS. Did not scaffold. Did not download or re-encode.
- **Result:** quality_scan printed clear for Q1 and hits 0. quality_scan_contract printed QUALITY SCAN CONTRACT PASS. selftest printed SELFTEST PASS. Videos published stay 0.
- **Verification status:** completed for the promotion gate and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The scanner existed but promotion did not call it, so the recommended next action was still a remembered command.
- **Blocker:** GitHub Actions secrets YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, and YOUTUBE_REFRESH_TOKEN remain the publish gate. Not polled. Recurring external stall.
- **Recommended next action:** Store those three secrets, then dispatch youtube-production.yml with execute=true and skip_comment false. Do not rewrite Q1 WORDS. Do not scaffold Q2. Do not add another instruction-only sentence while STALL_INSTRUCTION_LOCK is set.

## 2026-10-04T21:12:00Z — Run 322

- **Objective:** Stop the instruction-lock loop and add a reusable script quality signal that does not rewrite Q1.
- **Inspected:** STATE, NEXT, RUNS, stall_watch.py, content_quality.md, Q1 packet. OAuth secrets were not polled. Execute was not dispatched.
- **Action taken:** stall_watch now prints STALL_INSTRUCTION_LOCK when the last three deltas are credential-idle instruction edits. quality_scan.py reports the content_quality phrases in script WORDS and writes nothing. Contracts lock both. Selftest runs them. Did not scaffold. Did not rewrite Q1 WORDS. Did not download or re-encode.
- **Result:** Before the STATE delta, stall_watch printed STALL_INSTRUCTION_LOCK. quality_scan printed clear for Q1, the template, and the sample, hits 0. quality_scan_contract and stall_watch_contract passed. selftest printed SELFTEST PASS. Videos published stay 0.
- **Verification status:** completed for the scanner and the stall printer. Actions was not re-run. No provider write.
- **Important discovery:** Runs 319-321 each avoided OAuth and only locked operator copy. The Studio stall flag had gone clear because those deltas no longer said Studio, so the same no-progress pattern was invisible.
- **Blocker:** GitHub Actions secrets YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, and YOUTUBE_REFRESH_TOKEN remain the publish gate. Not polled. Recurring external stall.
- **Recommended next action:** Store those three secrets, then dispatch youtube-production.yml with execute=true and skip_comment false. On a new packet, run quality_scan.py before ready_for_vo. Do not rewrite Q1 WORDS. Do not add another instruction-only sentence while STALL_INSTRUCTION_LOCK is set.

## 2026-10-04T20:15:00Z — Run 321

- **Objective:** Stop the fill-idea path from telling the operator to paste idea.md by hand after apply_idea.py already exists.
- **Inspected:** STATE, NEXT, RUNS, hint.py, next_action.py, idea_brief.py, idea_gate_contract.py, apply_idea.py. OAuth secrets were not polled. Execute was not dispatched.
- **Action taken:** fill-idea now prints doctor.py then apply_idea.py dry-run. The --write line is a comment. idea_brief, expand_prompt, next_topic, queue_status, production_rules, and human_session name apply_idea instead of a hand paste. idea_gate_contract locks that. selftest runs the contract. Did not scaffold. Did not rewrite Q1 idea.md. Did not download or re-encode.
- **Result:** `python3 tools/idea_gate_contract.py` printed IDEA GATE CONTRACT PASS. `python3 tools/apply_idea_contract.py` printed APPLY IDEA CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. `videos/003-put-the-start-cue-on-the-work-itself` was not created. Videos published stay 0.
- **Verification status:** completed for the hint lock and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 320 added the writer, but the operator printers still said paste by hand. idea_gate_contract was already failing on HEAD because fill-idea did not start with doctor.py, and selftest did not run it.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall.
- **Recommended next action:** Store those three secrets, then dispatch `youtube-production.yml` with execute=true and skip_comment false. Do not scaffold Q2. Do not overwrite a reviewed idea.md with apply_idea.py. Do not restore a hand-paste instruction for idea.md.

## 2026-10-04T19:30:00Z — Run 320

- **Objective:** Remove the hand paste of a blank idea.md after scaffold without creating Q2 or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, topic_queue.md, idea_brief.py, new_packet.py, scaffold_contract.py. OAuth secrets were not polled. Execute was not dispatched.
- **Action taken:** Added `tools/apply_idea.py` and `tools/apply_idea_contract.py`. Selftest runs the contract. `idea_followup` now names the command and still reprints the locked fields. Did not scaffold. Did not rewrite Q1 idea.md. Did not download or re-encode.
- **Result:** `python3 tools/apply_idea_contract.py` printed APPLY IDEA CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. `videos/003-put-the-start-cue-on-the-work-itself` was not created. Videos published stay 0.
- **Verification status:** completed for the idea fill lock and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The queue paste was already complete. The remaining step was copying it into a blank idea.md by hand.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall.
- **Recommended next action:** Store those three secrets, then dispatch `youtube-production.yml` with execute=true and skip_comment false. Do not scaffold Q2. Do not overwrite a reviewed idea.md with apply_idea.py.

## 2026-10-04T18:14:00Z — Run 319

- **Objective:** Remove the handwritten problem step for the next four queued topics without scaffolding a packet or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, topic_queue.md, new_packet.py, idea_brief.py, queue_lib.py, queue_contract.py. OAuth secrets were not polled. Execute was not dispatched.
- **Action taken:** Added a problem column. Q2-Q5 now have locked problem lines. idea_followup reprints a non-empty problem cell. Q1 still reprints the existing pin sentence. queue_contract locks the four cells. Did not scaffold. Did not download or re-encode.
- **Result:** `python3 tools/idea_brief.py --queue Q2` printed the locked problem and writes nothing. `python3 tools/queue_contract.py` printed QUEUE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Videos published stay 0.
- **Verification status:** completed for the queue problem lock and local contracts. Actions was not re-run. No provider write.
- **Important discovery:** Only Q1 had a locked problem. The next scaffold reprint asked a human to write one before expand.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall.
- **Recommended next action:** Store those three secrets, then dispatch `youtube-production.yml` with execute=true and skip_comment false. Do not scaffold Q2. Do not blank the problem column.

## 2026-10-04T14:16:00Z — Run 318

- **Objective:** Remove the stale next-scaffold id so a later run cannot create a second `002-` packet, without another Studio sentence or an OAuth poll.
- **Inspected:** STATE, NEXT, RUNS, OPERATOR_HOLD, topic_queue.md, next_topic.py, queue_status.py, queue_contract.py. OAuth secrets were not polled. Execute was not dispatched.
- **Action taken:** Replaced the `topic_queue.md` claim that the next scaffold is `002-` with the current `next_topic.py` path `videos/003-put-the-start-cue-on-the-work-itself`. `queue_contract.py` now fails if that stale sentence returns. Listed `q1-media-r253` and `q1-media-r249` assets; digests still match the recorded master and wav. Did not download, re-encode, or scaffold.
- **Result:** `python3 tools/queue_contract.py` printed QUEUE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. `next_topic.py` still predicts `videos/003-put-the-start-cue-on-the-work-itself`. Videos published stay 0.
- **Verification status:** completed for the doc lock and local contracts. Release listing verified. Actions was not re-run. No provider write.
- **Important discovery:** The board tools already printed 003. The queue doc still told agents the next scaffold was 002, which would collide with Q1.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall.
- **Recommended next action:** Store those three secrets, then dispatch `youtube-production.yml` with execute=true and skip_comment false. Do not add another Studio sentence while `STALL_OAUTH_AND_STUDIO` is set. Do not scaffold Q2. Do not restore the next-scaffold-is-002 sentence.

## 2026-10-04T12:20:00Z — Run 317

- **Objective:** Stop the Studio-handoff loop and bind the end-screen reserve to the encode constant.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, studio_handoff.py, timeline.py, selftest. OAuth secrets were not polled. Execute was not dispatched.
- **Action taken:** `tools/stall_watch.py` flags three consecutive OAuth-unpolled Studio deltas as `STALL_OAUTH_AND_STUDIO`. Selftest locks that detector. `studio_handoff.py` prints `end_screen_reserve_s` from `timeline.END_SCREEN` instead of a second hardcoded 20. No YouTube call. No new YouTubeAPIError reason.
- **Result:** selftest, prove_locks, and upload_variant_freeze passed locally. Stall watch printed the flag on current STATE. Videos published stay 0.
- **Verification status:** completed for the detector and the reserve binding. Actions was not re-run. No provider write.
- **Important discovery:** Runs 314-316 were the same no-progress pattern as the earlier upload-status loop: prose additions while the secret hold did not move.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall.
- **Recommended next action:** Store those three secrets, then dispatch `youtube-production.yml` with execute=true and skip_comment false. Do not add another Studio sentence while `STALL_OAUTH_AND_STUDIO` is set. Do not add a YouTubeAPIError reason without a live_status line. Do not scaffold Q2.

## 2026-10-04T11:20:00Z — Run 316

- **Objective:** Put the Studio end-screen step in the same committed handoff as the pin URL, without a new upload reason or an OAuth poll.
- **Inspected:** STATE, NEXT, RUNS, studio_handoff.py, youtube-production.yml, format.md. OAuth secrets were not polled. Execute was not dispatched.
- **Action taken:** `studio_pin.md` and the Studio pin print now include `end_screen: not_set` and the editor URL only when upload_state.json has a provider video id. Lower-left video or playlist, lower-right subscribe, last 20 seconds already reserved. A missing id still writes nothing and prints no URL. No YouTube call. No new YouTubeAPIError reason.
- **Result:** selftest, prove_locks, and upload_variant_freeze passed locally. A fixture id printed the editor URL and `end_screen: not_set`. An empty state wrote nothing. Videos published stay 0.
- **Verification status:** completed for the handoff text and local locks. Actions was not re-run. No provider write.
- **Important discovery:** Run 315 persisted the pin URL. The other Studio step the Data API cannot do, the end screen, was still only in format.md, so the operator would still search Studio after the first private upload.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall.
- **Recommended next action:** Store those three secrets, then dispatch `youtube-production.yml` with execute=true and skip_comment false. Pin and add the end screen from `studio_pin.md` after that commit. Do not add a YouTubeAPIError reason without a live_status line. Do not scaffold Q2.

## 2026-10-04T10:12:00Z — Run 315

- **Objective:** Persist the Studio pin URL with the video id so the operator does not depend on the Actions log, without a new upload reason or an OAuth poll.
- **Inspected:** STATE, NEXT, RUNS, youtube-production.yml, studio_handoff.py, selftest. OAuth secrets were not polled. Execute was not dispatched.
- **Action taken:** `studio_handoff.py --write` writes `videos/.../studio_pin.md` only when upload_state.json has a provider video id. The comments URL and pin-candidate text are in that file. `pinned` stays false. A missing id does not create the file. The production persist step commits `studio_pin.md` with the upload state. No YouTube call. No new YouTubeAPIError reason.
- **Result:** selftest, prove_locks, and upload_variant_freeze passed locally. A fixture id wrote the Studio URL and `pinned: false`. An empty state wrote nothing. Videos published stay 0.
- **Verification status:** completed for the writer, workflow commit line, and local locks. Actions was not re-run. No provider write.
- **Important discovery:** Run 314 printed the URL only in the job log. A lost log still forced a Studio search even after the video id was committed.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall.
- **Recommended next action:** Store those three secrets, then dispatch `youtube-production.yml` with execute=true and skip_comment false. Pin from `studio_pin.md` after that commit. Do not add a YouTubeAPIError reason without a live_status line. Do not scaffold Q2.

## 2026-10-04T09:20:00Z — Run 314

- **Objective:** Make the remaining Studio pin a printed handoff after execute, without a new upload reason or an OAuth poll.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, youtube-production.yml, youtube_upload.py. Materialized Q1 from r253. media_qa PASS. Upload dry-run gate YOUTUBE_AUTH_REQUIRED. OAuth secrets were not polled.
- **Action taken:** Added `tools/studio_handoff.py`. After execute, the workflow prints the Studio comments URL, the pin-candidate text, and `pinned: false` when upload_state.json has a provider video id. No video id prints `no_video_id` and no URL. No YouTube call. No new YouTubeAPIError reason.
- **Result:** selftest, prove_locks, and upload_variant_freeze passed locally. A fixture state printed `https://studio.youtube.com/video/vid42/comments` and `pinned: false`. Videos published stay 0.
- **Verification status:** completed for the printer and local locks. Actions was not re-run. No provider write.
- **Important discovery:** The Data API comment insert was already on the execute path. The remaining human step had no stable URL in the job log, so every future upload still needed a Studio search.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall.
- **Recommended next action:** Store those three secrets, then dispatch `youtube-production.yml` with execute=true and skip_comment false. Pin from the STUDIO_PIN url in that job log. Do not add a YouTubeAPIError reason without a live_status line. Do not scaffold Q2.

## 2026-10-04T08:20:00Z — Run 313

- **Objective:** Land the Run 312 category/license adapter so videos.insert cannot keep a hardcoded Education category after the channel file changes or goes missing.
- **Inspected:** STATE, NEXT, RUNS, docs/run312.md, docs/channel.md, youtube_upload.py, selftest.py, upload_variant_freeze.py. OAuth secrets were not polled.
- **Action taken:** `category_id()` and `channel_license()` read docs/channel.md. Inspect adds `category_known` and `license_known`. Execute raises METADATA_REJECTED for unknown values before the token refresh. request_body and the insert body send the channel values. Removed the `categoryId` 27 literal. Selftest locks the channel values, the missing-file refusal, and the absent literal. Did not add a YouTubeAPIError reason. Did not dispatch. Did not scaffold Q2.
- **Result:** `python3 tools/selftest.py` printed SELFTEST PASS. prove_locks and upload_variant_freeze passed. Videos published stay 0. No provider write.
- **Verification status:** completed. Local selftest, prove_locks, and upload_variant_freeze passed. Actions run 37188429455 concluded success on `56b782f7222dcd44ccc3bed405124a4296c9420b`. No provider write.
- **Important discovery:** Run 312 recorded the design as partial because the 47k/101k file push did not land. The channel lines were already on main and the adapter still hardcoded 27.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Secret list API was not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Leave `skip_comment` false. Pin the comment in Studio after upload. Do not add a YouTubeAPIError reason without a live_status line. Do not scaffold Q2.

## 2026-10-04T09:15:00Z — Run 311

- **Objective:** Give the production dispatch a real opt-out for the approved first comment, and stop treating a Data API comment insert as a Studio pin, without adding an upload HTTP status variant or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, OPERATOR_HOLD, youtube-production.yml, youtube_upload.py, youtube_api.py. OAuth secrets were not polled.
- **Action taken:** Added workflow input `skip_comment` (default false). Execute passes `--skip-comment` when that input is true. Skip wins over `post_comment`. `comment_post.pinned` stays false with a Studio-pin note. Selftest locks both. Did not add a YouTubeAPIError reason. Did not dispatch. Did not scaffold Q2.
- **Result:** `python3 tools/selftest.py` printed SELFTEST PASS. prove_locks and upload_variant_freeze passed. Videos published stay 0. No provider write.
- **Verification status:** completed. Local selftest, prove_locks, and upload_variant_freeze passed. Actions run 37182446814 on `c95a5438abda65ff99f8d38049e0be7a4efed98c` concluded success. No provider write.
- **Important discovery:** Run 310 made the approved comment post on execute, but the dispatch form had no opt-out. `commentThreads.insert` does not pin. A human still pins in Studio after the first private upload.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Secret list API was not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Leave `skip_comment` false to post the approved comment. Pin that comment in Studio after upload; the API does not pin it. Do not add a YouTubeAPIError reason without a live_status line. Do not scaffold Q2.

## 2026-10-04T05:20:00Z — Run 310

- **Objective:** Remove the extra dispatch that would have been needed only to post the already-approved pin comment, without adding an upload HTTP status variant or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, OPERATOR_HOLD, youtube_upload.py, youtube-production.yml. Materialized Q1 from the private releases. OAuth secrets were not polled.
- **Action taken:** `should_post_comment` posts the pin comment on execute when `First comment approved` is checked and the text is non-empty. `--post-comment` stays an extra request. `--skip-comment` is the opt-out. Selftest covers the four cases. Did not add a YouTubeAPIError reason. Did not dispatch. Did not scaffold Q2.
- **Result:** Local materialize ignored the truncated r249 master and installed the r253 master. Dry-run gate `YOUTUBE_AUTH_REQUIRED`. media_qa PASS. Q1 comment box checked, 199 characters. `python3 tools/selftest.py` printed SELFTEST PASS. prove_locks and upload_variant_freeze passed. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed. Local selftest, prove_locks, and upload_variant_freeze passed. Actions run 37179477808 on `ec9d111de2f64fe697f76c59e1d7727c8a559341` concluded success. No provider write.
- **Important discovery:** The publish gate already refuses an unchecked first-comment box, but the workflow default left `post_comment` false. The first successful execute would have uploaded the video and still needed a second dispatch for the pin.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Secret list API returned 403. Not polled again. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. That execute posts the approved pin comment. Do not add a YouTubeAPIError reason without a live_status line. Do not scaffold Q2.

## 2026-10-04T04:11:00Z — Run 309

- **Objective:** Make the existing write-path lock run on every push, without adding an upload HTTP status variant or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, OPERATOR_HOLD, selftest.yml, prove_locks.py. OAuth secrets were not polled.
- **Action taken:** Added a selftest workflow step that runs `python3 tools/prove_locks.py`. `selftest.py` now fails if that step is removed. Did not map prove_locks in needed.py. Did not dispatch. Did not scaffold Q2. Did not add a YouTubeAPIError reason.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Local `python3 tools/prove_locks.py` printed PROVE LOCKS PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed. Local selftest and prove_locks passed. Actions run 37176474403 on `20f05c8a20cec81271e06f75441aef4d659b505e` concluded success, including the new Prove write-path locks step. No provider write.
- **Important discovery:** Runs 304 and later treated prove_locks as a remembered post-write command. A push could land a write-path regression without CI running those three locks.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not drop the prove_locks CI step. Do not add a YouTubeAPIError reason without a live_status line. Do not scaffold Q2.

## 2026-10-04T03:15:00Z — Run 308

- **Objective:** Stop a rejected provider-state push from depending on a mid-job unshallow after the upload, without adding an upload HTTP status variant or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, youtube-production.yml, persist_provider_state.py. OAuth secrets were not polled.
- **Action taken:** Production checkout is now `fetch-depth: 0`. Selftest refuses `fetch-depth: 1`. The existing unshallow-before-rebase path stays. Did not add a YouTubeAPIError reason. Did not dispatch. Did not scaffold Q2.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. `python3 tools/prove_locks.py` printed PROVE LOCKS PASS. `python3 tools/upload_variant_freeze.py` printed UPLOAD VARIANT FREEZE PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the checkout pin and local commands. Actions was not re-run. No provider write.
- **Important discovery:** Run 298 unshallows only after a rejected push. The production job still checked out depth 1, so the video id commit still depended on a full fetch at the end of a long upload.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not restore a shallow production checkout. Do not add a YouTubeAPIError reason without a live_status line. Do not scaffold Q2.

## 2026-10-04T02:15:00Z — Run 307

- **Objective:** Stop future runs from adding another upload error reason while the publish gate is still the missing OAuth secrets.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, youtube_api.py, youtube_upload.py. OAuth secrets were not polled.
- **Action taken:** Added `tools/upload_variant_freeze.py` and `docs/live_execute_evidence.md`. Selftest rejects a new `YouTubeAPIError` reason unless the evidence file has a `live_status` line. A synthetic new reason fails; the same reason with a live_status line passes. Existing reasons stay allowed. Did not dispatch. Did not scaffold Q2. Did not add an HTTP status variant.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. `python3 tools/prove_locks.py` printed PROVE LOCKS PASS. `python3 tools/upload_variant_freeze.py` printed UPLOAD VARIANT FREEZE PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the freeze and local commands. Actions was not re-run. No provider write.
- **Important discovery:** The status loop was documented as suspicious since Run 296 and still grew through Run 306. A prose flag did not stop it. A selftest lock can.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not add a YouTubeAPIError reason without a live_status line. Do not scaffold Q2.

## 2026-10-04T01:20:00Z — Run 306

- **Objective:** Stop a normal HD processing delay from forcing a second execute for the same caption, without adding an upload HTTP status variant or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, FAILURES, youtube_api.py, youtube_upload.py, youtube-production.yml. OAuth secrets were not polled.
- **Action taken:** Raised `wait_for_caption_ready` from six 10-second polls to 30 polls of 20 seconds (about 10 minutes). The 60-minute job still covers it. Selftest refuses a budget under 8 minutes or over 15. Did not dispatch. Did not scaffold Q2.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. `python3 tools/prove_locks.py` printed PROVE LOCKS PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the wait budget and local commands. Actions was not re-run. No provider write.
- **Important discovery:** Run 305 closed the permanent caption 400, but a 60-second budget would still exit VIDEO_PROCESSING_NOT_READY on a typical 1080p master and require another dispatch.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not shrink the caption wait to 60 seconds. Do not add another HTTP status variant unless a live execute returned that status. Do not scaffold Q2.

## 2026-10-04T00:25:00Z — Run 305

- **Objective:** Stop the first caption write from dying on a processing 400, without adding an upload HTTP status variant or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, FAILURES, youtube_api.py, youtube_upload.py, youtube_integration.md. OAuth secrets were not polled.
- **Action taken:** Added `wait_for_caption_ready`. Execute polls `videos.list` `processingDetails` up to six times before `captions.insert`. succeeded and terminated continue. failed is `VIDEO_PROCESSING_FAILED`. Still processing is `VIDEO_PROCESSING_NOT_READY`. The provider video id stays persisted. The next execute resumes the caption and must not insert again. Extended the selftest. Did not dispatch. Did not scaffold Q2.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. `python3 tools/prove_locks.py` printed PROVE LOCKS PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the processing wait and local commands. Actions was not re-run. No provider write.
- **Important discovery:** A caption 400 is permanent in this client. Sending captions before YouTube finishes processing would burn the first execute and look like a caption defect.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not drop the caption processing wait. Do not add another HTTP status variant unless a live execute returned that status. Do not scaffold Q2.

## 2026-10-03T23:20:00Z — Run 304

- **Objective:** Make the advertised post-write lock pass on this checkout, without adding an upload HTTP status variant or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, BLOCKED, prove_locks.py, placeholder_guard.py, words_contract.py, write_path_contract.py. OAuth secrets were not polled.
- **Action taken:** Split the placeholder needle in words_contract.py so the scanner is not itself a placeholder body. The write-path leak check now hashes the live Q1 packet and fails only if those bytes change. Absence stays an empty map. Did not dispatch. Did not scaffold Q2.
- **Result:** `python3 tools/prove_locks.py` printed PROVE LOCKS PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the lock contract and local commands. Actions was not re-run. No provider write.
- **Important discovery:** prove_locks could not pass on the real repo. The contract file contained the needle it scans for, and the leak check required the live Q1 packet to be absent. Run 299 recorded that fail and left it.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not restore the prove_locks false fail. Do not add another HTTP status variant unless a live execute returned that status. Do not scaffold Q2.

## 2026-10-03T22:20:00Z — Run 303

- **Objective:** Stop a slow upload from being killed before the video id is persisted, without adding an HTTP status variant or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, BLOCKED, youtube-production.yml, youtube_api.py. OAuth secrets were not polled (Actions secret list returned 403).
- **Action taken:** Raised the production job timeout from 20 to 60 minutes. Chunk PUT timeout is now 180 seconds via `CHUNK_PUT_TIMEOUT`. Selftest refuses a 20-minute job and a retry budget that does not fit. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the timeout contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The job budget was shorter than one 600-second PUT plus retries. A timeout kill is not an HTTP status; it just never writes `upload_state.json`.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not restore the 20-minute job timeout. Do not add another HTTP status variant unless a live execute returned that status. Do not scaffold Q2.

## 2026-10-03T21:15:00Z — Run 302

- **Objective:** Stop an omitted made-for-kids flag from uploading a video that Studio then blocks, without adding an upload HTTP status variant or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, BLOCKED, youtube_upload.py, youtube_api.py, channel.md. OAuth secrets were not polled (Actions secret list returned 403).
- **Action taken:** `docs/channel.md` records `audience_designation: not_made_for_kids`. Inspect holds when that line is missing or other. Execute raises `AUDIENCE_UNKNOWN` before the token refresh. `upload_video` no longer defaults a missing flag to false. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the audience gate and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The field was already hardcoded false on the execute path, but a missing flag was still treated as false in the transport. YouTube treats absence as unset, not as false.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not add another HTTP status variant unless a live execute returned that status. Do not change `audience_designation` unless the channel decision changes. Do not scaffold Q2.

## 2026-10-03T20:20:00Z — Run 301

- **Objective:** Stop a drafted chapter list from being dropped at videos.insert, without adding an upload HTTP status variant or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, BLOCKED, youtube-production.yml, youtube_upload.py. OAuth secrets were not polled. Concurrency group already exists.
- **Action taken:** `chapter_sync_reason()` refuses a chapters.md list that is under 3 lines, does not start at 0:00, has a gap under 10 seconds, or is missing or reordered in the publish description. Inspect is HOLD_LOCAL. Execute raises METADATA_REJECTED before the token refresh. A missing chapters.md stays missing. Q1 lines already match. Extended the selftest. Did not dispatch. Did not regenerate chapters.md or publish.md.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the chapter-sync gate and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The workflow already has `concurrency: youtube-production` with cancel-in-progress false. The publish gate is still the missing OAuth secrets. Chapter drop was a silent viewer miss, not an HTTP status.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not add another HTTP status variant unless a live execute returned that status. Do not regenerate chapters.md while captions.srt is unchanged. Do not scaffold Q2.

## 2026-10-03T19:20:00Z — Run 300

- **Objective:** Turn the recurring OAuth secret stall into a non-secret setup recipe, without adding another upload HTTP status variant or re-opening closed publish boxes.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, `docs/human_session.md`, `docs/youtube_integration.md`, `tools/youtube_upload.py`. OAuth secrets were not polled.
- **Action taken:** Added `tools/oauth_setup.py`. It prints console steps, the required scopes, and `gh secret set` commands that read from the prompt. It reports missing secret names only and does not call Google. `docs/human_session.md` no longer asks to check Description edited or First comment approved. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the recipe and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The live human page still told the operator to re-check boxes Run 297 already closed. That was recurring labor, not the credential gate. The upload-status loop remains frozen.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not add another HTTP status variant unless a live execute returned that status. Do not re-open Description edited or First comment approved. Do not scaffold Q2.

## 2026-10-03T15:20:00Z — Run 299

- **Objective:** Disclose generated narration on the first videos.insert, without adding another upload HTTP status variant.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, youtube_upload.py, youtube_api.py, Q1 vo_origin.md. OAuth secrets were not polled.
- **Action taken:** videos.insert now sets status.containsSyntheticMedia from vo_origin.md. kind generated is true. kind human is false. An unknown kind is SYNTHETIC_DISCLOSURE_UNKNOWN before the token refresh and does not insert. Q1 is generated. Extended the selftest. Did not dispatch.
- **Result:** Local python3 tools/selftest.py printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the disclosure flag and local selftest. Actions was not re-run. No provider write. prove_locks.py still fails on the pre-existing words_contract.py placeholder check; not caused by this change.
- **Important discovery:** The upload path set selfDeclaredMadeForKids but omitted containsSyntheticMedia. Q1 narration is edge-tts, so the first private upload would have left the altered-content disclosure for a Studio click.
- **Blocker:** GitHub Actions secrets YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, and YOUTUBE_REFRESH_TOKEN remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Add those three secrets from a token granted youtube.upload and youtube.force-ssl (or full youtube), then dispatch youtube-production.yml with execute=true. Do not drop containsSyntheticMedia. Do not invent a vo origin. Do not add another HTTP status variant unless a live execute returned that status. Do not scaffold Q2.

## 2026-10-03T14:20:00Z — Run 298

- **Objective:** Stop a rejected provider-state push from dropping the video id on the shallow Actions checkout, without adding another upload status variant.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, `youtube-production.yml`, `tools/persist_provider_state.py`. OAuth secrets were not polled.
- **Action taken:** `push_with_retry` unshallows when the clone is shallow, then fetches and rebases. A failed rebase aborts. No force-push. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the shallow retry order and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 297's retry still fails on the default checkout depth. The publish gate is still the missing OAuth secrets.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not force-push provider state. Do not rebase a shallow checkout without unshallow. Do not add another HTTP status variant unless a live execute returned that status. Do not scaffold Q2.

## 2026-10-03T12:20:00Z — Run 297

- **Objective:** Stop a successful upload from being lost when the provider-state push is rejected, without adding another upload status variant.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, `youtube-production.yml`, `next_action.py`, `hint.py`, `pipeline_status.py`. OAuth secrets were not polled.
- **Action taken:** Added `tools/persist_provider_state.py`. Upload and feedback persist now classify before commit and retry a non-fast-forward push after fetch and rebase. No force-push. Q1 board copy no longer asks to check already approved publish boxes. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the persist classifier, retry order, and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The video-id hold was only durable if `git push origin HEAD:main` succeeded on the first try. The publish gate is still the missing OAuth secrets.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not force-push provider state. Do not re-open the approved Q1 boxes. Do not add another HTTP status variant unless a live execute returned that status. Do not scaffold Q2.

## 2026-10-03T11:20:00Z — Run 296

- **Objective:** Stop the upload status-variant loop and close the unaligned resume hole that would send a chunk YouTube rejects.
- **Inspected:** STATE, NEXT, ROADMAP, HANDOFF, FAILURES, BLOCKED, `youtube_api.py`, `youtube-production.yml`. OAuth secrets were not polled.
- **Action taken:** A 308 Range that is not a multiple of 256 KiB is `RESUMABLE_STALLED` (`unaligned_offset`). The next chunk is not sent. Tiny-chunk tests stay exempt. Extended the selftest. Did not dispatch. Flagged Runs 281-295 as a suspicious loop.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the alignment guard and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The client resumed any advancing Range. Byte 100 is not a legal non-final chunk start. More status classes would not fix that, and the publish gate is still the missing secrets.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not send an unaligned resumable chunk. Do not add another HTTP status variant unless a live execute returned that status. Do not scaffold Q2.

## 2026-10-03T10:20:00Z — Run 295

- **Objective:** Stop a finished resumable upload whose session then returns 404 or 410 from inviting a second videos.insert.
- **Inspected:** STATE, NEXT, FAILURES, `tools/youtube_api.py`, `tools/youtube_upload.py`, `youtube-production.yml`. OAuth secrets were not polled (Actions secret list is 403 for this token).
- **Action taken:** A 200/201 with no id still queries the same session once. A 404 or 410 on that query is `RESUMABLE_COMPLETED_SESSION_GONE`. Execute persists `completed_without_id` and does not invent a video id. A matching fingerprint is `HOLD_COMPLETED_WITHOUT_ID`. The workflow commits that hold. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the completed-session-gone contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 294 recovered an id only when the follow-up query returned 200/201. The documented expired-session responses after an accepted last byte were still a duplicate-insert path, and the workflow would not have committed the failure.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall since the execute path existed. Flagged, not re-worked this run.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not start a second videos.insert after `RESUMABLE_COMPLETED_SESSION_GONE`. Do not invent a provider video id. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T09:15:00Z — Run 294

- **Objective:** Stop a finished resumable upload whose 200/201 body was dropped from looking like a missing video and inviting a second videos.insert.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/selftest.py`. OAuth secrets were not polled.
- **Action taken:** A completing PUT that returns 200 or 201 with an empty or id-less body queries the same session once and returns that video id. It does not open another videos.insert. A non-200/201 query stays `RESUMABLE_MISSING_VIDEO_ID`. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the empty-completion-body contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Runs 287-293 resume 308, 5xx, 401, and post-upload artifact failures, but a 201 with an empty body still raised `RESUMABLE_MISSING_VIDEO_ID` without asking the session. That is the case where the server already has the video and the next execute would spend another insert.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not start a second videos.insert when a completion body is empty. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T08:20:00Z — Run 293

- **Objective:** Stop a 401 on caption, thumbnail, or pin-comment upload from looking permanent after the video id already exists, without a second videos.insert.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/selftest.py`. OAuth secrets were not polled.
- **Action taken:** Post-upload calls refresh the access token on 401 and retry the same artifact request. An empty or unchanged token, or three refreshes, raise `POST_UPLOAD_TOKEN_REFRESH_EXHAUSTED`. A 400 stays permanent. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the post-upload 401 contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 292 refreshed a 401 only on the resumable master. Access tokens expire in about an hour, so a long upload could finish and then fail captions with the stale token. That is not a snippet gate.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not start a second videos.insert on a post-upload 401. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T07:20:00Z — Run 292

- **Objective:** Stop a 401 on the resumable master upload from aborting the session and inviting a second videos.insert.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/selftest.py`. OAuth secrets were not polled.
- **Action taken:** A chunk PUT 401, or a session-start 401 with no Location, refreshes the access token and continues the same upload. A Location already returned is not followed by another videos.insert. Three refreshes or an empty/unchanged token raise `RESUMABLE_TOKEN_REFRESH_EXHAUSTED`. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the 401 resume contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Runs 287-291 covered 308, 5xx, missing Range, session-start 503, and post-upload artifact retries. A 401 still raised `RESUMABLE_UNEXPECTED_STATUS` and dropped the Location.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not start a second videos.insert on 401. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T06:16:00Z — Run 291

- **Objective:** Stop a transient 503 on caption, thumbnail, or pin-comment upload from forcing another workflow dispatch after the video id already exists, without another snippet gate or a second videos.insert.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `tools/youtube_api.py`, `tools/selftest.py`.
- **Action taken:** Post-upload calls retry 408/429/5xx and network errors up to three times, then raise `POST_UPLOAD_RETRY_EXHAUSTED`. A 400 stays permanent. Extended the selftest. Did not dispatch. Did not poll secrets.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the artifact-retry contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Runs 287-290 made the master resumable, but captions and thumbnails still used one multipart POST. A 503 there is POST_UPLOAD_INCOMPLETE even though the video id exists. Snippet micro-gates remain deferred.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T05:20:00Z — Run 290

- **Objective:** Stop a session-start 503 with no Location from aborting the first upload, without starting a second videos.insert when Location is already present, and without restating the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/selftest.py`, `youtube-production.yml`.
- **Action taken:** Session POST now retries 408/429/5xx and network errors only when Location is missing. A Location on a non-200 is used and not followed by another POST. Chunk 408 and 429 join the existing resume set. A status query that advances the offset clears the retry count. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the session-start contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 288 resumed a chunk PUT 503, but the session POST itself still treated 503 as `RESUMABLE_SESSION_MISSING`. That is the call that spends the insert quota unit. A 503 with no Location has nothing to resume. A 503 with Location must not be retried as a new insert.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not scaffold Q2. Do not add another snippet micro-gate. Do not invent a baseline or decision.

## 2026-10-03T04:11:00Z — Run 289

- **Objective:** Stop a 308 with no Range header from skipping bytes the server did not store.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/selftest.py`, YouTube resumable upload guide (a 308 without Range means nothing has been uploaded).
- **Action taken:** `received_offset()` returns None when Range is omitted. The upload loop restarts at byte 0, honors Retry-After up to 30 seconds, and raises `RESUMABLE_STALLED` after three missing-Range responses. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the missing-Range contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 288 queried the session after a 5xx, but a chunk 308 without Range still used `end+1` as the resume point. That would send the next chunk past bytes YouTube says it does not have.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not treat a missing Range as received. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T03:12:00Z — Run 288

- **Objective:** Stop a transient 5xx on the resumable master upload from looking like a permanent failure and inviting a second `videos.insert`.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/selftest.py`, official resumable upload guide (500/502/503/504 are resumeable).
- **Action taken:** A chunk PUT that returns 500, 502, 503, or 504, or a network error, now queries the session with `Content-Range: bytes */size` and resumes from the Range. Three failures at the same stage raise `RESUMABLE_RETRY_EXHAUSTED`. A 404 on that query is `RESUMABLE_SESSION_EXPIRED`. Captions and thumbnails stay multipart. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the 5xx resume contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 287 resumed only on HTTP 308. A 503, which the official guide says to resume, still raised `RESUMABLE_UNEXPECTED_STATUS` and left no video id, so the next execute could open a second session.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not restore multipart for the master. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T02:11:00Z — Run 287

- **Objective:** Stop the first authenticated `videos.insert` from depending on one multipart POST of the multi-minute master.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/youtube_upload.py`, workflow timeout, selftest.
- **Action taken:** `upload_video` now starts a resumable session and PUTs 8 MiB chunks, continuing after HTTP 308. Captions and thumbnails stay multipart. Selftest covers Range parsing, chunk alignment, and a fake 308 resume. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the resumable contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Runs 281-286 kept adding pre-insert snippet gates while the master still used multipart. That gate loop is diminishing and should stop unless a documented provider reject is still ungated. The transport hole was the remaining first-upload failure mode that local gates cannot catch.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not restore multipart for the master. Do not scaffold Q2.

## 2026-10-03T01:20:00Z — Run 286

- **Objective:** Stop a tag list that is under a raw 500-character sum from reaching `videos.insert` when quotes and commas push it over the provider limit.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, `tools/youtube_upload.py`, `tools/selftest.py`, Q1 `publish.md` tags.
- **Action taken:** `metadata_block_reason` now uses `tag_budget()`. A space adds two quote characters. Each comma between tags counts. Selftest covers a 12-tag fixture whose raw sum is under 500 and whose budget is over 500, plus the short Q1-style spaced tags. Q1 tags were checked and still pass (budget 152).
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the local gate and selftest. Actions was not re-run. No provider write.
- **Important discovery:** The previous total counted tag characters only. Official `videos.insert` accounting wraps spaced tags in quotes and counts separators, so the old gate could pass a list the API rejects as `invalidTags`.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not scaffold Q2. Do not regenerate Q1 tags.

## 2026-10-03T00:35:00Z — Run 285

- **Objective:** Stop overlapping captions or a truncated PNG from creating a private video that then loops on post-upload failure, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, `youtube_upload.py`, `youtube_api.py`, Q1 `captions.srt`, Q1 `thumbnail.png`, selftest.
- **Action taken:** `caption_timing_reason()` now refuses a cue that starts before the previous cue ends. `png_has_iend()` refuses a PNG whose last chunk is not IEND. Inspect stays HOLD_LOCAL. Execute raises ARTIFACT_REJECTED before the token refresh. `videos.insert` sets `defaultLanguage` and `defaultAudioLanguage` to `en`, and `captions.insert` uses the same language. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Q1 captions.srt (103 cues, no overlap) and thumbnail.png (IEND present) pass. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the overlap and IEND contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 284 checked cue start order only. A later cue could start inside the previous cue and still pass READY, then fail after `videos.insert`. A PNG with a valid IHDR and no IEND had the same hole for `thumbnails.set`.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it. The refresh token must include caption scope, not only upload scope.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), plus `yt-analytics.readonly` for later collect. Then dispatch `youtube-production.yml` with execute=true. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T23:20:00Z — Run 284

- **Objective:** Stop a caption draft with bad timing, or an empty or illegal title, from creating a private video that then loops on post-upload failure, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, `youtube_upload.py`, `youtube_api.py`, Q1 `captions.srt`, selftest.
- **Action taken:** Added `caption_timing_reason()`. Present captions must have parseable forward cues in order. If the master can be probed, the last cue cannot end more than one second past it. Empty titles and titles with angle brackets fail in `metadata_block_reason()`. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Q1 captions.srt (103 cues) passes with no local master. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the timing contract and local selftest. Actions was not re-run. No provider write. Q1 master was not in the checkout, so the past-video check was verified only by the unit case.
- **Important discovery:** Run 283 accepted any file containing `-->`. A backward cue or a cue past the master would still pass READY and fail only after `videos.insert`.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it. The refresh token must include caption scope, not only upload scope.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), plus `yt-analytics.readonly` for later collect. Then dispatch `youtube-production.yml` with execute=true. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T22:13:00Z — Run 283

- **Objective:** Stop a bad thumbnail or caption draft from creating a private video that then loops on post-upload failure, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, `youtube_upload.py`, `youtube_api.py`, Q1 `captions.srt`, selftest.
- **Action taken:** Added `artifact_block_reason()` and `png_dimensions()`. Inspect treats it as a hard local check. Execute raises `ARTIFACT_REJECTED` before the token refresh. Missing thumbnail or captions stay missing. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Q1 captions.srt passes with thumbnail absent. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the artifact contract and local selftest. Actions was not re-run. No provider write. Q1 thumbnail.png was not in the checkout, so its dimensions were not remeasured this run.
- **Important discovery:** Scope and snippet checks ran before insert, but a present thumbnail over 2MB, not a PNG, or under 640px, or a caption file with no cue, would still pass READY and fail only after `videos.insert`.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it. The refresh token must include caption scope, not only upload scope.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), plus `yt-analytics.readonly` for later collect. Then dispatch `youtube-production.yml` with execute=true. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T21:13:00Z — Run 282

- **Objective:** Stop an upload-only OAuth token from creating a private video that then loops on caption failure, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, `youtube_upload.py`, `youtube_api.py`, `youtube-production.yml`, `docs/youtube_integration.md`, selftest.
- **Action taken:** Added `missing_provider_scopes()` and a tokeninfo scope read after refresh. Execute raises `SCOPE_INSUFFICIENT` before `videos.insert` when captions need `youtube.force-ssl` or the full `youtube` scope and the grant lacks both. A scope refusal does not write `upload_state.json`. Documented the consent scopes. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the scope contract and local selftest. Actions was not re-run. No provider write. Tokeninfo was not called.
- **Important discovery:** The documented minimum scope was `youtube.upload`. That scope can insert the video and set a thumbnail, but `captions.insert` requires `youtube.force-ssl` or `youtube`. The first authenticated dispatch would have created a video and then stayed `POST_UPLOAD_INCOMPLETE`.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it. The refresh token must include caption scope, not only upload scope.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), plus `yt-analytics.readonly` for later collect. Then dispatch `youtube-production.yml` with execute=true. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T20:12:00Z — Run 281

- **Objective:** Fail closed on YouTube snippet limits before the first authenticated write, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, `youtube_upload.py`, selftest, Q1 `publish.md`.
- **Action taken:** Added `metadata_block_reason()`. Inspect treats it as a hard local check. Execute refuses `METADATA_REJECTED` and `PRIVACY_NOT_PRIVATE` before the token refresh. Stopped silent `tags[:12]` truncation. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Q1 title 42 chars, 9 tags, description under 5000, block reason None. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the metadata limit contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** `request_body` and `upload_video` sliced tags to 12, so a later packet could drop tags and still look READY.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Invalid snippet fields must fail before the token refresh. A post-upload failure can be retried with the same execute input; it must not create a second video. Dispatch collect_feedback=true only after uploaded_at is at least 7 days old and not in the same dispatch as execute. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T19:15:00Z — Run 280

- **Objective:** Stop a rematerialized master from uploading a second video, and let a failed caption or thumbnail resume on the existing video id, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, `youtube_upload.py`, `youtube-production.yml`, selftest.
- **Action taken:** Fingerprint now hashes export bytes instead of mtime. `existing_upload_action()` returns resume, finished, mismatch, or none. Inspect exposes `RESUME` / `RESUME_POST_UPLOAD` for an incomplete post-upload. Execute refuses `EXISTING_VIDEO_FINGERPRINT_MISMATCH` instead of inserting another video. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the resume/idempotency contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 279 persisted the video id, then the next execute hit `HOLD_IDEMPOTENT` and returned before resume. The fingerprint also included mtime, so a later materialize of the same r253 bytes would miss that id and upload a second copy.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. A post-upload failure can be retried with the same execute input; it must not create a second video. Dispatch collect_feedback=true only after uploaded_at is at least 7 days old and not in the same dispatch as execute. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T17:20:00Z — Run 279

- **Objective:** Stop a caption or thumbnail failure from looking like a finished upload, and stop that failure from dropping the provider video id, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `youtube_upload.py`, `youtube-production.yml`, selftest.
- **Action taken:** Added `incomplete_post_uploads()`. Execute writes state, then raises `POST_UPLOAD_INCOMPLETE` if caption, thumbnail, or requested comment status is failed. Persist step now runs with `always()` when execute was requested. Collect is skipped when execute is also true. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the incomplete-upload contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** A failed caption previously left the execute step green, and a raised execute step skipped the persist step. Either path could lose the video id or hide a missing caption.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Dispatch collect_feedback=true only after uploaded_at is at least 7 days old and not in the same dispatch as execute. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T16:20:00Z — Run 278

- **Objective:** Stop a resumed upload from erasing the observation clock, without retrying the OAuth stall or inventing a timestamp.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `youtube_upload.py`, `youtube_feedback.py`, selftest.
- **Action taken:** Added `preserved_upload_stamp()`. Resume copies `video_upload.uploaded_at` or top-level `uploaded_at` onto the new state. A fresh upload writes the same stamp in both places. Missing prior stamp stays missing. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the stamp contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 277's window reads `uploaded_at`, but a caption or thumbnail retry rebuilt `video_upload` as `already_uploaded` and dropped the stamp. The next collect would stay `OBSERVATION_WINDOW_UNKNOWN` forever.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Dispatch collect_feedback=true only after uploaded_at is at least 7 days old. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T15:20:00Z — Run 277

- **Objective:** Stop an early feedback collect from becoming COLLECTED evidence, without retrying the OAuth stall or inventing metrics.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `youtube_feedback.py`, `youtube-production.yml`, selftest.
- **Action taken:** Collect now requires `video_upload.uploaded_at` or `uploaded_at` at least 7 days old. Missing time is `OBSERVATION_WINDOW_UNKNOWN`. An earlier time is `OBSERVATION_WINDOW_NOT_DUE` and exits 5 before any provider read. `execute_feedback` repeats the check. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the window contract and local selftest. Actions was not re-run. No provider write or read.
- **Important discovery:** Run 276 could dispatch collect as soon as a video id existed. That fetch would be committed as COLLECTED and could later be compared as if the 7-day window had elapsed.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Dispatch collect_feedback=true only after uploaded_at is at least 7 days old. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T14:20:00Z — Run 276

- **Objective:** Remove the post-publish manual feedback CLI without retrying the OAuth stall or inventing metrics.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `youtube-production.yml`, `youtube_feedback.py`, `oauth_preflight.py`, selftest.
- **Action taken:** Added workflow input `collect_feedback` (default false). Authenticated execute or collect runs `oauth_preflight.py` first. Collect-only skips ffmpeg and materialize, then runs `youtube_feedback.py --execute` and `experiment_loop.py --write-state`. Persist commits feedback only when gate is COLLECTED and a provider video id exists. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the workflow contract and local selftest. Actions was not re-run. No provider write or read.
- **Important discovery:** The execute path persisted upload state and stopped. Every later video would still need a human to invoke the feedback CLI even after secrets exist.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. After a provider video id exists, dispatch collect_feedback=true. Do not invent a Q1 baseline or decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T13:30:00Z — Run 275

- **Objective:** Record an explicit keep/discard/retest without inferring it from the delta or retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `experiment_loop.py`, `complete.py`, selftest.
- **Action taken:** Added `load_decision()` for `experiment_decision.json`. The file is ignored until a numeric comparison exists. Valid keep/discard/retest with reason and a non-rejected source sets action `DECISION_RECORDED` and copies that decision into `result`. Missing, invented, or mismatched files stay pending. Extended the selftest. Did not write a Q1 decision.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the decision contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 274 could compute a delta but left `result` null forever. `complete.py` requires that field, and there was no file contract a later run could fill without editing code.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Flagged as a recurring external stall.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not invent a Q1 baseline or decision. Do not treat COMPARED as a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T12:25:00Z — Run 274

- **Objective:** Compute a post-publish primary-metric delta without inventing a baseline, a keep/discard, or retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `experiment_loop.py`, `complete.py`, selftest.
- **Action taken:** Added `compare_primary()`. A documented baseline plus one numeric collected value sets action `COMPARED` and fills `comparison` (observed, baseline, delta, direction). Decision stays `pending` and `result` stays null. Missing or conflicting metrics are `COMPARE_BLOCKED_METRIC`. `complete.py` now requires decision keep/discard/retest before COMPLETE.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0. No Q1 baseline was written.
- **Verification status:** completed for the comparison contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 273 stopped at COMPARE_READY even when the collected row already contained the primary metric. The next run would have had to hand-compute the delta.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Flagged as a recurring external stall.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not invent a Q1 baseline. Do not treat COMPARED as a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T11:17:00Z — Run 273

- **Objective:** Unlock post-publish comparison without inventing a baseline or retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, PROGRESS, `experiment_loop.py`, `complete.py`, production workflow, selftest.
- **Action taken:** Added `load_baseline()` for `experiment_baseline.json`. Rejected missing fields, disallowed changes, and sources named invented/assumed/placeholder/guess. A valid file sets action `COMPARE_READY` and leaves decision `pending`. Extended the selftest. Did not write a Q1 baseline.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the baseline contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Runs 266-272 kept meeting the same secret boundary. Further restatement does not move publish. The next unblocked contract was the comparison schema, not another preflight.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Flagged as a recurring external stall.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not invent a Q1 baseline. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T10:15:00Z — Run 272

- **Objective:** Stop an execute dispatch from downloading Q1 media when the three OAuth secrets are still empty, without polling secrets or retrying upload.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `youtube-production.yml`, `youtube_upload.py`, `youtube_feedback.py`.
- **Action taken:** Added `tools/oauth_preflight.py` (names and presence only). Wired it as the first step after checkout when execute=true, before Python setup, ffmpeg, and materialize. Extended the selftest for empty, blank, and present values, and for step order.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the preflight and selftest. Workflow order is unverified on Actions because execute was not dispatched. Dry-run path was not re-run.
- **Important discovery:** The previous execute step only failed after materialize. A mistaken execute=true dispatch would spend the release download before reporting missing secrets.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` are still unset. Not polled this run.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. The preflight should pass before materialize. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T09:15:00Z — Run 271

- **Objective:** Stop the post-upload loop from treating a real feedback fetch as no evidence, without retrying the OAuth boundary.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `youtube_feedback.py`, `experiment_loop.py`, `complete.py`, production workflow.
- **Action taken:** Added `collected_metrics()` which accepts only `gate=COLLECTED`, `attempted_fetch=true`, a non-empty metric row list, and a video id matching `upload_state.json`. Experiment and complete gates now use that helper. Extended the selftest for mismatch and matching collected rows.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Experiment with matching collected metrics is READY_TO_COMPARE and COMPARE_BLOCKED_NO_BASELINE. Result stays pending. Videos published stay 0.
- **Verification status:** completed. Local selftest passed, then Actions run 36988824728 succeeded on `613e8ee439ccf16e4ce8c5aaf4855fe30aa523dd`. No provider write.
- **Important discovery:** `inspect_feedback()` always sets metrics to None. Both learning gates used that field, so a later `feedback_state.json` would never advance the experiment or completion gates.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` are still unset. Secret list API returned 403 for this token. Do not poll.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not scaffold Q2. Do not invent a keep/discard from collected metrics.

## 2026-10-02T08:18:05Z — Run 270

- **Objective:** Prove the Run 269 production workflow instead of restating the OAuth hold.
- **Inspected:** STATE, NEXT, HANDOFF, RUNS, `youtube-production.yml`, `materialize_q1_release.py`.
- **Action taken:** Dispatched workflow_dispatch with execute=false. Run 36982959831 failed because materialize aborted when the expected truncated r249 master was present. Changed the guard to ignore that known sha, refuse an unexpected r249 master sha, and still refuse installing the banned sha as `export/master.mp4`. Pushed `9416aae2c482ca08fd55642e0fff94568482ee51` and redispatched.
- **Result:** Run 36983196381 succeeded. Materialize logged `ignored known-truncated r249 q1-master.mp4; installing r253 master only`, then 7 cards and `export/master.mp4`. Dry-run gate `YOUTUBE_AUTH_REQUIRED`, action `DRY_RUN`, export present, publish copy approved, captions 103 cues uploaded=false, thumbnail present uploaded=false. OAuth env vars were empty. Execute and state-persist steps skipped. Videos published stay 0.
- **Verification status:** Actions job 110762207440 conclusion success. Prior job 110761451601 conclusion failure, used as the regression evidence. No provider write claimed.
- **Important discovery:** The production path was blocked by a local guard, not by OAuth. Treating presence of the banned release asset as fatal prevented the r253 install.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` are unset.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not scaffold Q2. Do not restore the presence-only abort.

## 2026-10-05T04:20:00Z — Run 330

- **Objective:** Stop the dry-run from telling the operator to mint a youtube.upload-only token, without adding another local gate.
- **Inspected:** STATE, NEXT, BLOCKED, stall_watch, youtube_upload.py, oauth_setup.py, Q1 materialize.
- **Action taken:** Named the three consent scopes on the dry-run text and request body. Locked that warning in selftest. Materialized Q1 and confirmed media_qa PASS and YOUTUBE_AUTH_REQUIRED. Did not dispatch. Did not add a scanner.
- **Result:** selftest, upload_variant_freeze, and prove_locks passed locally. Videos published stay 0.
- **Verification status:** completed for the dry-run scope text and local gates. Actions was not re-run. No provider write.
- **Important discovery:** The execute path already refused an upload-only token, but the dry-run JSON still listed only youtube.upload. That was the operator-facing setup signal.
- **Blocker:** GitHub Actions secrets YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN. Not polled.
- **Recommended next action:** Add those three secrets with the consent scopes from oauth_setup.py, then dispatch youtube-production.yml with execute=true. Do not scaffold Q2. Do not add another scanner while publish stays at 0.

## 2026-10-05T08:20:00Z — Run 331

- **Objective:** Remove the repeated Studio step of adding each published video to a series playlist, without inventing an id or retrying the secret hold.
- **Inspected:** STATE, NEXT, BLOCKED, stall flags, channel.md, youtube-production.yml, youtube_api.py.
- **Action taken:** Added `playlist_id: not_set` and `tools/playlist_membership.py`. Dry-run default. `--execute` inserts only when a real PL id and a provider video id both exist. Unset and missing-id paths write no request. Workflow calls the tool after execute and persists `playlist_plan.md` only when that file is written. Contract locks the unset path.
- **Result:** Contract and selftest passed locally. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the skip path and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The Data API can add a video to a playlist with the already required force-ssl scope. Pin and end screen still cannot. The playlist id is the only missing human input, and it is once per channel, not once per video.
- **Blocker:** GitHub Actions secrets YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN. Not polled. Playlist id is also unset and is not the publish gate.
- **Recommended next action:** Add the three secrets with the consent scopes from oauth_setup.py, then dispatch youtube-production.yml with execute=true. Optionally create one series playlist and replace `playlist_id: not_set`. Do not scaffold Q2. Do not add another scanner.

## Run 332 — 2026-10-05T09:20:00Z
- objective: stop the OAuth-idle loop from disappearing when the run topic changes, and fail a mistyped playlist id
- action: `stall_watch.py` prints `STALL_OAUTH_IDLE` after eight unpolled published-0 deltas; `playlist_membership.py` exits 2 only on `invalid_playlist_id`
- result: contracts and selftest passed locally; current STATE prints `STALL_OAUTH_IDLE`; playlist plan for Q1 stays `not_set` exit 0
- verification: completed locally; Actions not re-run
- discovery: a 3-run same-topic flag clears after one subject change
- blocker: YouTube OAuth secrets still absent; not polled
- next: do not add another scanner or playlist variant; live execute after the three secrets, or a bugfix in a tool the production job already runs

## Run 333 — 2026-10-05T10:30:00Z
- objective: stop the dry-run request from advertising an upload-only scope, and print the existing idle flag on the production job
- action: `youtube_upload.py` `scope` is the joined consent set; `youtube-production.yml` runs `stall_watch.py` after checkout and does not fail on the flag
- result: selftest and upload-variant freeze passed locally; `auth_status` scope lists upload, force-ssl, and analytics; stall flag still `STALL_OAUTH_IDLE`
- verification: completed locally; Actions not re-run; no provider write
- discovery: Run 330 named `required_scopes` but left `scope` as youtube.upload, which is the field an operator would copy into the consent screen
- blocker: YouTube OAuth secrets still absent; not polled
- next: mint the refresh token with the three consent scopes, then dispatch execute=true; do not add another scanner or playlist variant

## Run 334 — 2026-10-05T08:17:14Z
- objective: stop a failed playlist insert from looking successful after a video id exists
- action: `playlist_membership.py` exits 2 on auth_required and on not_added with a detail; those rows write playlist_plan.md; not_set and missing video id stay exit 0 and write nothing
- result: playlist contract and selftest passed locally; Q1 playlist plan remains not_set
- verification: completed locally; Actions not re-run; no provider write
- discovery: Run 332 only failed a mistyped id; an API failure after a real PL id still exited 0 and skipped the plan file
- blocker: YouTube OAuth secrets still absent; not polled
- next: mint the refresh token with the three consent scopes, then dispatch execute=true; do not add another scanner

## Run 335 — 2026-10-05T09:11:00Z
- Objective: Stop the first analytics collect from treating a short, lag-cut window as the 7-day observation.
- Action: `window_status` due time is upload plus 7 days plus `DATA_LAG_DAYS` (3). `analytics_range` is the first 7 calendar days of that video. Selftest expects day 8 to stay not due and day 11 to be READY offline. Workflow summary and `docs/feedback_loop.md` say the same.
- Result: Local `check_feedback_fail_closed` returned no failures. No Analytics call. Videos published stay 0.
- Verification: completed for the window math and the existing feedback selftest helper. Full `selftest.py` not re-run. Actions not re-run.
- Discovery: The old due gate and the query end date disagreed, so the first experiment could be collected before the claimed window existed.
- Blocker: YouTube OAuth secrets still absent. Playlist id still `not_set`.
- Next: Do not rediscover this lag. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

## Run 336 — 2026-10-05T10:20:00Z
- Objective: Make the dry-run analytics plan use the same first-7-day dates the live fetch already uses.
- Action: `video_window()` fills `inspect_feedback` window from `analytics_range` when `uploaded_at` exists. Missing upload time leaves query dates empty. `request_plan` reads those dates. Selftest fails if a ready plan is not the upload date through upload plus 6 days.
- Result: `python3 tools/selftest.py` printed SELFTEST PASS. No Analytics call. Videos published stay 0.
- Verification: completed locally. Actions not re-run. No provider write.
- Discovery: Run 335 fixed the due gate and the execute query, but the plan an operator would copy still showed a sliding now window.
- Blocker: YouTube OAuth secrets still absent. Playlist id still `not_set`.
- Next: Do not restore the sliding query range. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

## Run 337 — 2026-10-05T11:20:00Z
- Objective: Stop a collected analytics file from counting as the first 7 days unless its window is that video's calendar range.
- Action: `collected_window_ok` refuses a missing kind, `sliding_now`, or dates that do not match `analytics_range`. `execute_feedback` stamps `kind: first_calendar_days` and queries `DEFAULT_WINDOW_DAYS` from `uploaded_at`. Selftest covers a sliding file and a matching file. Experiment fixture now includes the matching window.
- Result: `python3 tools/selftest.py` printed SELFTEST PASS. No Analytics call. Videos published stay 0.
- Verification: completed locally. Actions not re-run. No provider write.
- Discovery: Run 336 aligned the dry-run plan, but a COLLECTED file without kind still passed into experiment comparison.
- Blocker: YouTube OAuth secrets still absent. Playlist id still `not_set`.
- Next: Do not treat an unstamped collected file as the 7-day observation. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

## Run 338 — 2026-10-05T12:30:00Z
- Objective: Stop the production persist step from committing a COLLECTED analytics file that is not the first-calendar-days stamp.
- Action: `feedback_commit_decision` returns `skip_unstamped_window` when kind is missing or `sliding_now`, days are not 7, or start/end dates are absent. A stamped file still returns `commit_collected`. Selftest locks both. Workflow summary states the commit rule. Date match against `uploaded_at` stays in `collected_metrics`.
- Result: `python3 tools/selftest.py` printed SELFTEST PASS. No Analytics call. Videos published stay 0.
- Verification: completed locally. Actions not re-run. No provider write.
- Discovery: Run 337 closed the comparison path only. The workflow still committed any COLLECTED file with a video id, so a sliding or unstamped file could become the durable evidence.
- Blocker: YouTube OAuth secrets still absent. Playlist id still `not_set`.
- Next: Do not commit an unstamped collected file. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

## Run 339 — 2026-10-05T14:20:00Z
- Objective: Stop the production stall printer from treating `No new scanner` as another local-gate run.
- Action: Removed the bare `scanner` token from `tools/stall_watch.py` and scrub negation phrases before the local-gate match. Contract covers three boilerplate deltas. Real scan tokens still set `STALL_LOCAL_GATE`.
- Result: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. Current STATE prints `STALL_OAUTH_IDLE` only. `python3 tools/selftest.py` printed SELFTEST PASS. Videos published stay 0.
- Verification: completed locally. Actions not re-run. No provider write.
- Discovery: Runs 336-338 said `No new scanner` and that sentence kept `STALL_LOCAL_GATE` set, so later runs were told not to add a scanner they were not adding.
- Blocker: YouTube OAuth secrets still absent. Playlist id still `not_set`.
- Next: Do not restore the bare scanner token. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

## Run 340 — 2026-10-05T15:20:00Z
- Objective: Stop STATE.md from truncating before the current gate on the next agent fetch.
- Action: Moved deltas older than the newest 12 from STATE.md to docs/state_archive.md. Added tools/state_compact.py and a contract. Selftest runs the contract.
- Result: STATE.md is 12 run sections. Archive holds the older sections. stall_watch still prints STALL_OAUTH_IDLE. Videos published stay 0.
- Verification: state_compact_contract printed STATE COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: STATE.md was 52418 bytes and 67 run sections. The agent fetch truncated it before the publish-gate section.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not paste the archive back into STATE.md. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 342 — 2026-10-05T17:15:00Z
- Objective: Stop RUNS.md from truncating before the newest run log on the next agent fetch.
- Action: Moved entries older than the newest 12 from RUNS.md to docs/runs_archive.md. Added tools/runs_compact.py and a contract. Selftest runs the contract. Did not poll secrets. Did not add a scanner. Did not scaffold Q2.
- Result: RUNS.md keeps 12 entries plus the permanent footer. Archive holds the older entries, including Run 270. Videos published stay 0.
- Verification: runs_compact_contract printed RUNS COMPACT CONTRACT PASS. python3 tools/selftest.py printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: RUNS.md was 108696 bytes and 71 entries. The agent fetch cut the newest section before the recommended next action.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not paste the archive back into RUNS.md. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 343 — 2026-10-05T17:25:00Z
- Objective: Stop PROGRESS.md and FAILURES.md from truncating before the newest lesson on the next agent fetch.
- Action: Moved sections older than the newest 12 to docs/progress_archive.md and docs/failures_archive.md. Added tools/log_compact.py and a contract. Selftest runs the contract. Did not poll secrets. Did not add a scanner. Did not scaffold Q2.
- Result: Both live files are 12 sections. Archives hold the older notes. Videos published stay 0.
- Verification: log_compact_contract printed LOG COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: PROGRESS.md was 27269 bytes and FAILURES.md was 30708 bytes. NEXT.md truncated near 28KB, so both were already past the known fetch cut.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not paste the archives back. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 345 — 2026-10-05T19:20:00Z
- Objective: Stop a dead resumable Location from being reused forever or turning into a second videos.insert.
- Action: Probe a saved session URI before any chunk. A 404 or 410 drops the URI, sets session_expired_hold, and commits that hold. The next execute raises RESUMABLE_SESSION_EXPIRED and does not POST videos.insert. Did not add a reason. Did not poll secrets. Did not add a scanner. Did not scaffold Q2.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 344 committed the Location, but an expired session was skip_transient, so the dead URI stayed the next execute target.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not start a second videos.insert when Location exists or when session_expired_hold is set. Do not print the URI. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 344 — 2026-10-05T18:20:00Z
- Objective: Stop a killed execute from starting a second videos.insert after Location exists.
- Action: Saved the resumable session URI into upload_state.json and committed that row. The next execute resumes that URI and does not POST videos.insert. Fingerprint mismatch reuses the existing mismatch reason. Did not poll secrets. Did not add a scanner. Did not scaffold Q2.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Runs 340-343 only compacted fetch files. The open Location was still not durable, so the first real upload could duplicate if the runner died after the session POST.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not print the session URI. Do not start a second videos.insert when Location exists. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 346 — 2026-10-05T20:15:00Z
- Objective: Stop a committed dead-session hold from bricking the first upload after Studio shows no video.
- Action: Added a local release that clears `session_expired_hold` only with studio token `no_video_in_studio`, no provider video id, and no remaining Location. Persist commits that release. The production workflow does not pass the flag. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a YouTubeAPIError reason.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 345 fail-closed on 404/410, but nothing could clear the hold, so the first expired session would block every later execute even after a human checked Studio.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Eight-plus runs of upload-edge fixes have not published; that idle is the known credential stall, not a missing scanner.
- Next: Do not pass the release flag from Actions. Do not release without the Studio token. Do not start a second videos.insert when Location exists or when session_expired_hold is set. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 347 — 2026-10-05T21:15:00Z
- Objective: Stop a killed execute from losing the open Location and starting a second videos.insert.
- Action: Persist an open resumable session from the uploader before the first chunk when UPLOAD_EARLY_PERSIST=1. The production execute step sets that env. The plan does not contain the URI. A git failure does not raise into the upload. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a YouTubeAPIError reason.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 344 committed the Location only after the execute step returned. A timeout or runner kill skipped that step, so the next execute could POST videos.insert again.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Nine-plus runs of upload-edge fixes have not published; that idle is the known credential stall, not a missing scanner.
- Next: Do not print the session URI. Do not start a second videos.insert when Location exists or when session_expired_hold is set. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 348 — 2026-10-05T22:15:00Z
- Objective: Stop a job kill during caption wait from losing the provider video id.
- Action: Early-persist the provider video id before caption wait when UPLOAD_EARLY_PERSIST=1. Early-persist a 404/410 hold and a completed-without-id hold before those exceptions leave the step. Selftest locks the extra calls and that early persist pushes. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a YouTubeAPIError reason.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 347 pushed the Location only. Caption wait can outlive the job. A later 404 on that Location would set session_expired_hold with no video id even if the upload had already completed.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Ten-plus runs of upload-edge fixes have not published; that idle is the known credential stall, not a missing scanner.
- Next: Do not print the session URI. Do not start a second videos.insert when a video id or Location exists or when session_expired_hold is set. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 349 — 2026-10-05T22:35:00Z
- Objective: Stop a kill after captions.insert from retrying captions, and flag the upload-edge loop.
- Action: Early-persist caption, thumbnail, and comment status after each write when UPLOAD_EARLY_PERSIST=1. stall_watch now sets STALL_UPLOAD_EDGE after four OAuth-idle upload-edge deltas. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a YouTubeAPIError reason.
- Result: Selftest passed. Stall contract passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. Actions not re-run. No provider write.
- Discovery: Runs 344-348 each added a resumable or early-persist branch while OAuth stayed absent. That is the credential stall. Caption status was the remaining kill hole in that chain, and it is now the last early-persist call site while the flag is set.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: upload-edge fixes have not published a video. Do not add another one.
- Next: Do not add another Location, session hold, or early-persist call. Do not add a scanner. Do not scaffold Q2. Do not poll secrets. Wait for the three YouTube secrets, or fix a production tool that is not the uploader.

## Run 356 — 2026-10-06T05:11:00Z
- Objective: Stop stacked STATE headers from hiding or truncating the current gate.
- Action: `state_compact.py` now keeps one preamble and strips later `# STATE` headers before the size cap. Collapsed the live file from 13 headers to 1. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload probe.
- Result: Contract passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/state_compact_contract.py` printed STATE COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Each run prepended a full `# STATE` file. Compact counted `## Run` only, so the Run 343 body was already cut and a dangling header remained.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not prepend a second `# STATE` header. Do not add another export probe, media checker, or caption cue gate. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

Older runs live in `docs/runs_archive.md`. Do not paste the archive back. `tools/runs_compact.py` moves extras. It does not delete history.

## Run 357 — 2026-10-06T06:20:00Z
- Objective: Stop stacked FAILURES and PROGRESS headers from hiding the newest lesson.
- Action: `log_compact.py` drops a later file header and a repeated archive pointer. Both live logs now have one header and 12 sections. Finished the cut Run 356 STATE bullet. Did not poll secrets. Did not add a scanner or a probe.
- Result: Contracts passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/log_compact_contract.py` printed LOG COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 356 collapsed STATE headers only. FAILURES and PROGRESS still had stacked headers.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not prepend a second file header. Do not add another probe. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 358 — 2026-10-06T07:15:00Z
- Objective: Cut the manual OAuth token exchange down to one local command that cannot commit the refresh token.
- Action: Added `tools/oauth_exchange.py` and a contract. The recipe now points at it. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload probe.
- Result: Contract passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/oauth_exchange_contract.py` printed OAUTH EXCHANGE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: The setup recipe named the scopes but still left the consent URL and token POST to an unscripted browser step. A wrong scope still creates a private video that cannot take captions.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human runs the exchange once and stores the three secrets. Do not add another probe. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 359 — 2026-10-06T08:11:00Z
- Objective: Stop the first OAuth exchange from failing when the human pastes the localhost address bar.
- Action: `oauth_exchange.py` extracts the code from a redirect URL or a raw code. Denied redirects are refused. The token still writes only outside the repo. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload probe.
- Result: Contract passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/oauth_exchange_contract.py` printed OAUTH EXCHANGE CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Desktop consent does not load localhost. The code is in the address bar. A raw-code-only stdin read would send that URL to the token endpoint.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-idle runs have not published a video. Do not add another probe.
- Next: A human runs the exchange once and stores the three secrets. Paste the full redirect URL. Do not add another probe. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 360 — 2026-10-06T09:11:00Z
- Objective: Stop a second Active locks block from hiding the one human step on a truncated NEXT.md fetch.
- Action: `next_compact.py` keeps one Active locks block and drops a lone `.` paragraph. NEXT.md now names the three secrets as the step. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload probe. Did not add another OAuth exchange parser.
- Result: Contract passed. Oldest NEXT note archived. Videos published stay 0. No live execute.
- Verification: `python3 tools/next_compact_contract.py` printed NEXT COMPACT CONTRACT PASS. Actions not re-run. No provider write.
- Discovery: NEXT.md had two Active locks blocks plus a `.` paragraph. A truncated fetch could land in the copy and miss the human step. Runs 358-359 added exchange parsers and published nothing.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-helper runs have not published a video. Do not add another exchange parser.
- Next: A human stores the three secrets and dispatches execute=true. Do not add another probe. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 361 — 2026-10-06T10:12:00Z
- Objective: Stop lock sentences from keeping stall flags set, and stop a last chapter inside the final 10 seconds from being uploaded as if YouTube would show it.
- Action: `stall_watch.py` scrubs do-not-add sentences before the pre-upload and upload-edge token checks. `chapter_sync_reason` takes an optional duration and refuses `chapter_last_under_10s_before_end`. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser.
- Result: Stall contract passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Newest STATE deltas repeated the lock sentence, and that sentence contained the same tokens as a wired probe. The flag could not clear. YouTube also drops a chapter list whose last stamp is inside the final 10 seconds. That check was missing.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-idle runs have not published a video. Do not add another exchange parser.
- Next: A human stores the three secrets and dispatches execute=true. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.
## Run 362 — 2026-10-06T11:20:00Z
- Objective: Make the first private execute a copy-paste dispatch instead of an unscripted workflow click.
- Action: `tools/oauth_setup.py` now prints `gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false`. Selftest requires that command. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Recipe check passed. Selftest passed. Videos published stay 0. No live execute.
- Verification: `check_oauth_setup_recipe` returned no failures. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Step 8 named execute=true but not the `gh` invocation. A first dispatch with collect_feedback=true would fetch before a video id exists.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-idle runs have not published a video. Do not add another exchange parser.
- Next: A human stores the three secrets and runs that dispatch. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

Permanent log. Newest first. Do not paste the archive back into this file.

## Run 364 — 2026-10-06T13:22:00Z
- Objective: Make the repeated unpublished OAuth stall countable so later runs can flag it instead of restating it.
- Action: `tools/stall_watch.py` prints `idle_streak` and `suspicious: oauth_idle_without_publish` at 8 or more consecutive unpublished unpolled deltas. Contract covers the streak, the suspicious line, and a reset when the newest delta is not that shape. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Contract passed. Videos published stay 0. No live execute. Idle streak on this STATE is 13.
- Verification: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. Actions not re-run. No provider write.
- Discovery: Runs 352-363 each said videos published stay 0 and OAuth was not polled. The idle flag already existed, but it did not say how long the stall had lasted.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 363 — 2026-10-06T12:20:00Z
- Objective: Stop a progress section that omits the Run heading from being dropped by the size cap.
- Action: `tools/log_compact.py` promotes a bare `NNN — timestamp` line to a Run heading before it splits sections. Restored the Run 360 heading. Moved Run 351 and Run 350 progress sections into `docs/progress_archive.md`. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Contract passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/log_compact_contract.py` printed LOG COMPACT CONTRACT PASS. Actions not re-run. No provider write.
- Discovery: Run 360 wrote `360 — 2026-10-06T09:11:00Z` without the section prefix. Compact splits only on the Run heading, so that lesson was body text of Run 361.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-idle runs have not published a video. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 365 — 2026-10-06T15:20:00Z
- Objective: Restore a green selftest after a zero idle streak was treated as a stall flag and the live logs exceeded the compact cap.
- Action: `tools/stall_watch.py` omits `idle_streak: 0` from `flag_text`. A positive streak and `suspicious: oauth_idle_without_publish` at 8 or more stay. Compact moved the oldest STATE delta and the oldest NEXT note into the archives. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Stall contract passed. State and next compact contracts passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. Compact tools printed OK. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 364 made every file print a streak, including a clear file. Selftest treats a non-empty `flag_text` as a stall. The live STATE and NEXT files were also one section over the cap, so the compact contracts failed.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 366 — 2026-10-06T16:20:00Z
- Objective: Stop a shadowed stall-watch check from letting a broken contract print SELFTEST PASS.
- Action: Merged the two `check_stall_watch` definitions in `tools/selftest.py`. The remaining check runs `stall_watch_contract.py` and the inline OAuth-idle assertions. Removed the duplicate call. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: The later definition replaced the contract call. Selftest invoked the name twice and still never ran the contract.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 367 — 2026-10-06T17:11:00Z
- Objective: Stop the first Studio pass from asking for a playlist end-screen element while playlist_id is not_set.
- Action: `tools/studio_handoff.py` names a video element (best for viewer) until a playlist id is set. A set id still names a playlist element. The workflow comment no longer says a failed playlistItems.insert prevents videos.insert. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: The pin note said lower-left video or playlist. playlist_id is not_set, so that instruction would stall the end screen the same way a missing playlist stalls membership.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 368 — 2026-10-06T18:12:00Z
- Objective: Stop a failed playlist insert from painting the job red after videos.insert.
- Action: The playlist membership step treats exit 2 as `PLAYLIST_INSERT_NOT_UPLOAD_FAILURE` and exits 0. Selftest requires that marker. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 367 said a failed playlistItems.insert is not an upload failure, but the step still returned that exit code. A red job is the signal that invites a second execute.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 369 — 2026-10-06T19:12:00Z
- Objective: Stop a caption, thumbnail, or comment miss from painting the job red after videos.insert.
- Action: The execute step treats exit 4 with a saved provider video id and `POST_UPLOAD_INCOMPLETE` as `POST_UPLOAD_NOT_INSERT_FAILURE` and exits 0. An insert failure without that id still fails the step. Selftest requires that marker. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 368 stopped a red playlist step from inviting a second execute. The upload step still exits 4 after the video id is written when caption, thumbnail, or comment work is incomplete. That red job is the same signal.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 370 — 2026-10-06T21:16:00Z
- Objective: Stop a Studio pin miss or a rejected provider-state push from painting the job red after videos.insert.
- Action: The Studio pin step prints `STUDIO_PIN_NOT_INSERT_FAILURE` and exits 0 when `studio_handoff.py` exits non-zero. The persist step prints `PERSIST_PUSH_NOT_INSERT_FAILURE` and exits 0 when a provider video id exists and the commit or push fails. A persist miss without that id still fails the step. Selftest requires both markers. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Runs 368 and 369 stopped a red playlist step and a red post-upload step from inviting a second execute. The Studio pin step and the persist step could still fail the job after a video id existed.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 371 — 2026-10-06T23:13:00Z
- Objective: Stop a playlist-step crash and a contradictory job summary from looking like an insert failure after videos.insert.
- Action: The playlist membership step prints `PLAYLIST_INSERT_NOT_UPLOAD_FAILURE` and exits 0 on any non-zero exit when upload state exists, not only exit 2. The job summary now says a caption or thumbnail miss prints `POST_UPLOAD_NOT_INSERT_FAILURE` and exits 0. Selftest refuses the old non-zero summary sentence and a playlist `exit "$status"`. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 368 only swallowed playlist exit 2. A crash still exited 1 and failed the job. The summary still said a caption or thumbnail failure exits non-zero after the video id is written, which invites another execute.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 372 — 2026-10-07T00:15:00Z
- Objective: Stop a persist classify miss from painting the job red after videos.insert.
- Action: The persist step prints `PERSIST_PUSH_NOT_INSERT_FAILURE` and exits 0 when `classify-upload` fails and a provider video id exists. A miss without that id still fails the step. Selftest refuses `exit "$status"` in that step. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 370 swallowed a rejected commit or push. A non-zero `classify-upload` still exited the step and could invite another execute.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 373 — 2026-10-07T01:15:00Z
- Objective: Make the provider-state push actually run after videos.insert.
- Action: Replaced both workflow heredocs with `python3 tools/persist_provider_state.py push`. The old `<<'PY'` terminator was indented, so Bash never closed it and `push_with_retry` never ran. Selftest refuses a workflow heredoc. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. A local count of `<<'PY'` in the workflow is 0. Actions not re-run. No provider write.
- Discovery: Runs 370-372 treated a non-zero persist status as not an insert failure. That swallow hid a push that could not start. The video id would stay on the runner.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 374 — 2026-10-07T02:13:00Z
- Objective: Keep a provider video id on main when classify-upload misses, without painting the job red.
- Action: The persist step prints `PERSIST_CLASSIFY_MISS_STILL_COMMIT` and continues to `git add` when classify-upload is non-zero and a provider video id exists. Status 2 still skips. A miss without that id still fails. Selftest refuses an exit 0 between that sentence and `git add`. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Runs 372 and 373 stopped a classify miss from failing the job by exiting 0 before the commit. That left the video id on the runner, which is the same loss the heredoc fix was meant to stop.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 375 — 2026-10-07T03:11:00Z
- Objective: Keep a provider video id recoverable when git push is rejected after videos.insert.
- Action: The production workflow has `actions: write` and uploads `upload_state.json` as `provider-upload-state` with continue-on-error. A rejected push prints `python3 tools/persist_provider_state.py recover` (`gh run download --repo takenthatusernameis-collab/Content-Automation --name provider-upload-state`). Selftest refuses a workflow that lacks that artifact. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Runs 370-374 exit 0 after a rejected push so the job stays green. That still leaves the video id off main. The next execute can insert again. The artifact is the copy that survives the runner.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. If push is rejected, download `provider-upload-state` and commit it before another execute. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 376 — 2026-10-07T04:12:00Z
- Objective: Stop a rejected-push recovery from downloading the newest selftest run instead of the video id.
- Action: `artifact_recovery_command` now pins `youtube-production.yml` with `gh run list --workflow` before `gh run download --name provider-upload-state`. Selftest refuses a recovery command that omits that workflow. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write. The recover function does not call GitHub.
- Discovery: Run 375 uploaded the artifact, then printed a bare `gh run download --name`. After the next agent commit, the newest run is selftest.yml, which has no `provider-upload-state`. That download misses the video id and invites another execute.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. If push is rejected, run `python3 tools/persist_provider_state.py recover` and commit that file before another execute. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 377 — 2026-10-07T05:11:00Z
- Objective: Stop a rejected-push recovery from downloading a later production run that has no video id.
- Action: `artifact_recovery_command` walks the last 20 `youtube-production.yml` runs, skips an empty run id, and downloads `provider-upload-state` into `/tmp/provider-upload-state` from the first run that has the artifact. Selftest refuses `--limit 1` and a missing empty-id guard. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write. The recover function does not call GitHub.
- Discovery: Run 376 pinned the newest production run. A later execute=false dispatch of the same workflow has no `provider-upload-state`. An empty `databaseId` also expanded to a bare download.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. If push is rejected, run `python3 tools/persist_provider_state.py recover` and commit that `upload_state.json` before another execute. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 378 — 2026-10-07T06:14:00Z
- Objective: Stop a rejected-push recovery from keeping a newer production artifact that has no provider video id.
- Action: `artifact_recovery_command` clears the download dir each run, skips a missing artifact, and skips `upload_state.json` unless `provider_video_id` is a non-empty string. Selftest refuses a break before that check. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute. Q1 media QA still PASS after materialize (verified this run, not committed).
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. `python3 tools/materialize_q1_release.py` then `python3 tools/media_qa.py` printed gate PASS. Actions not re-run. No provider write. The recover function does not call GitHub.
- Discovery: Run 377 stopped on the first production artifact. A later execute can upload state with a null video id. That file would hide an older insert and invite another videos.insert.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish (runs 366-378, no publish). Do not add another exchange parser. Do not spend another run only restating this blocker.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. If push is rejected, run `python3 tools/persist_provider_state.py recover` and commit only the file that prints RECOVERED_RUN. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 379 — 2026-10-07T07:16:00Z
- Objective: Make Actions selftest green again after Run 378 overflowed the log caps.
- Action: Ran `state_compact.py`, `next_compact.py`, `runs_compact.py`, and `log_compact.py`. Archived the oldest sections. Did not change recovery, upload, or OAuth code. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Live logs are back at the 12-section cap before this entry is compacted. Videos published stay 0. No live execute.
- Verification: Actions run 37580716646 failed with STATE.md 13 sections and NEXT.md 13 notes. Local compact tools printed COMPACT OK. Selftest is the verification for this commit.
- Discovery: A local SELFTEST PASS does not mean the commit stayed under the cap. Run 378 added a section and did not archive one. Suspicious: oauth_idle_without_publish still stands, and log_cap_overflow is a separate repeated risk if each run prepends without compacting.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Do not spend another run only restating that blocker. Do not add another recovery edge while this selftest was red.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. If push is rejected, run `python3 tools/persist_provider_state.py recover` and commit only the file that prints RECOVERED_RUN. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 380 — 2026-10-07T08:11:00Z
- Objective: Stop a green local selftest from shipping over-cap logs when the section is added afterward.
- Action: Added `tools/compact_all.py`. It runs the four existing compact tools and refuses a live log still over cap. Selftest calls `compact_all.py --check` and does not write. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add an exchange parser. Did not add a recovery edge. Did not dispatch the workflow.
- Result: Videos published stay 0. No live execute. Log caps stay a same-commit step, not a new upload path.
- Verification: `python3 tools/compact_all.py` then `python3 tools/selftest.py` on this commit. No provider write.
- Discovery: Run 378 passed selftest, then prepended a 13th STATE section and a 13th NEXT note. Actions run 37580716646 failed the contracts. Suspicious: oauth_idle_without_publish still stands (no publish since before Run 270), and recovery-edge stacking (Runs 368-378) did not publish. Do not add another edge for that stall.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Do not spend another run only restating that blocker.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. After a log prepend, run `python3 tools/compact_all.py` before push. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 381 — 2026-10-07T09:13:00Z
- Objective: Flag stacked provider-state recovery edges while videos published stay 0.
- Action: `stall_watch.py` now sets `STALL_RECOVERY_EDGE` and `suspicious: recovery_edge_without_publish` when the last four STATE deltas wire a recovery path during the OAuth stall. Lock sentences do not set the flag. Contract and selftest cover both cases. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge.
- Result: Videos published stay 0. The flag is clear on this commit because the newest deltas are log-cap work, not recover wiring.
- Verification: `python3 tools/stall_watch_contract.py` and `python3 tools/selftest.py`. No provider write.
- Discovery: Runs 368-378 stacked recovery edges and prose warnings did not stop the next edge. The idle flag already existed; it did not name this pattern.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Do not spend another run only restating that blocker.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 382 — 2026-10-07T10:14:00Z
- Objective: Stop another provider-state recovery edge from landing while videos published stay 0.
- Action: Added `tools/recovery_freeze.py`. Selftest fails if the production workflow grows a second `provider-upload-state` artifact or a second `persist_provider_state.py recover` call. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Downloaded `q1-media-r253` `q1-master-r253.mp4` and matched the documented sha256 and stream shape.
- Result: Videos published stay 0. Recovery surface counts stay artifact=1 and recover_call=1. Master sha256 `4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546`, 1920x1080 h264 30fps yuv420p, stereo AAC 48000 Hz, 328.40s.
- Verification: `python3 tools/recovery_freeze.py`, `python3 tools/recovery_freeze_contract.py`, and `python3 tools/selftest.py`. No provider write.
- Discovery: `STALL_RECOVERY_EDGE` only prints after four wired deltas. It did not stop Runs 368-378. A build failure on a grown surface is the stop. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 383 — 2026-10-07T11:17:00Z
- Objective: Keep the remaining human publish step in one command that cannot drift from the OAuth recipe.
- Action: Added `tools/operator_card.py`. It prints the three secret-set commands and the dispatch line from `oauth_setup.py`, and fails if HANDOFF loses the documented master sha. Selftest runs the contract. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge.
- Result: Videos published stay 0. Operator card PASS. Dispatch line matches the recipe.
- Verification: `python3 tools/operator_card_contract.py` and `python3 tools/operator_card.py`. No provider write.
- Discovery: Runs 368-382 froze and flagged recovery edges, but the human step was still reconstructed from NEXT notes. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human runs `python3 tools/operator_card.py` and stores the three secrets. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 384 — 2026-10-07T12:20:00Z
- Objective: Make the one human publish command include the Google Cloud steps, not only the secret-set lines.
- Action: `tools/operator_card.py` reprints the numbered steps from `oauth_setup.recipe()`. The contract fails if Desktop app, YouTube Data API v3, the exchange command, or the dispatch line drifts. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not add a scanner. Did not scaffold Q2.
- Result: Videos published stay 0. Operator card PASS. Console steps match the recipe.
- Verification: `python3 tools/operator_card_contract.py` and `python3 tools/operator_card.py`. No provider write.
- Discovery: Run 383 printed secret-set commands and still sent the human to reconstruct the console clicks. Suspicious: oauth_idle_without_publish still has no publish since before Run 270, and Runs 368-383 added stall tooling instead of a publish.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human runs `python3 tools/operator_card.py` and stores the three secrets. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 385 — 2026-10-07T13:23:00Z
- Objective: Stop another operator-card extension from landing while videos published stay 0.
- Action: Added `tools/operator_card_freeze.py`. Selftest fails if `operator_card.py` grows a function, a second card module appears, or the card imports subprocess or a network client. `stall_watch.py` sets `STALL_OPERATOR_CARD` after three wired card deltas. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend operator_card. Did not add a scanner. Did not scaffold Q2.
- Result: Videos published stay 0. Operator-card defs stay 5. No live execute.
- Verification: `python3 tools/operator_card_freeze_contract.py`, `python3 tools/stall_watch_contract.py`, and `python3 tools/selftest.py`. No provider write.
- Discovery: Runs 383-384 reprinted the human step and still published nothing. A prose "do not add a second card" did not stop the reprint. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human runs `python3 tools/operator_card.py` and stores the three secrets. Do not extend the card. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 386 — 2026-10-07T16:13:00Z
- Objective: Stop a green selftest from shipping an over-cap log when the section is prepended afterward.
- Action: Called the existing `check_compact_all()` from selftest `main`. Added `tools/record_run.py`, which prepends the five live logs and runs `compact_all.py` before it exits. Opened issue 1 with the operator-card text. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend operator_card. Did not add a scanner. Did not scaffold Q2.
- Result: Videos published stay 0. Issue 1 is the human step. No live execute.
- Verification: `python3 tools/record_run_contract.py` and `python3 tools/selftest.py`. No provider write.
- Discovery: Run 380 said selftest calls `compact_all.py --check`. The function existed and was not in `main`, so the Actions cap was only the separate state/next contracts. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not extend the card. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

Older run notes live in `docs/runs_archive.md`. Do not paste the archive back.

## Run 387 — 2026-10-07T17:12:00Z
- Objective: Stop the NEXT header from staying on an older run after a log prepend.
- Action: `prepend_next` replaces the single `Updated:` line from the note. The contract fails if that line is missing or doubled. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend operator_card. Did not add a scanner. Did not scaffold Q2. Did not add a freeze module.
- Result: Videos published stay 0. NEXT header now matches the note that wrote it. No live execute.
- Verification: `python3 tools/record_run_contract.py` printed RECORD RUN CONTRACT PASS. This entry was written by `record_run.py`, which also runs compact. No provider write.
- Discovery: Run 386 prepended note 1zr50 and left `Updated: ... (Run 385)`. Suspicious: oauth_idle_without_publish still has no publish since before Run 270, and Runs 375-386 stacked recovery, card, and freeze tooling instead of a publish. Do not add another freeze for that stall.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not extend the card. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 388 — 2026-10-07T18:11:00Z
- Objective: Stop a duplicated archive pointer from shipping after a green section-count check.
- Action: `compact_all.py --check` now fails unless PROGRESS.md and FAILURES.md each have exactly one archive pointer. Ran `log_compact.py` so the Run 387 duplicates are gone. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend operator_card. Did not add a scanner. Did not scaffold Q2. Did not add a freeze module.
- Result: Videos published stay 0. Live logs have one pointer each. No live execute.
- Verification: `python3 tools/log_compact_contract.py` printed LOG COMPACT CONTRACT PASS. `python3 tools/compact_all.py --check` printed COMPACT ALL OK. No provider write.
- Discovery: Run 387 said record_run compacts, and the committed logs still had two identical pointers. `--check` did not read them. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Do not add another freeze for that stall.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not extend the card. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 390 — 2026-10-07T20:13:00Z
- Objective: Make the next queued idea paste name its own stall, and stop a false contract fail on the existing Q1 folder.
- Action: `idea_brief.py` why now now includes the queue problem. The contract requires Q2 and Q3 why-now lines to differ and accepts Q1 status=used. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend the card. Did not add a scanner. Did not scaffold Q2. Did not add a freeze module. Did not add a compact check.
- Result: Videos published stay 0. Q2 why now names the missing start cue. Q3 why now names competing lists. No live execute.
- Verification: `python3 tools/idea_brief_contract.py` printed IDEA BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The idea contract already failed on main because it wanted Q1 status queued and the 002 folder absent. A shared why-now line would have been rewritten by hand on every later packet.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not scaffold Q2. Do not add a scanner. Do not poll secrets.

## Run 389 — 2026-10-07T19:11:00Z
- Objective: Flag three consecutive log-hygiene deltas so the next run does not invent another compact check.
- Action: `stall_watch.py` sets `STALL_LOG_HYGIENE` after three wired log-cap or header deltas while videos published stay 0. Contract and selftest cover the flag and the lock sentence. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend operator_card. Did not add a scanner. Did not scaffold Q2. Did not add a freeze module. Did not add a compact check.
- Result: Videos published stay 0. The flag names Runs 386-388. No live execute.
- Verification: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: Runs 386-388 tightened log checks and still published nothing. Suspicious: log_hygiene_without_publish and oauth_idle_without_publish. Do not add another compact check for that stall.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not extend the card. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets. Do not add a compact check.

## Run 392 — 2026-10-07T22:12:00Z
- Objective: Stop the approved Q1 pin from posting a reply ask without rewriting that draft.
- Action: `viewer_comment` drops the reply sentence the same way it drops the stub pin note. The publish contract checks the posted pin and still requires Q1 bytes unchanged. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend the card. Did not add a scanner. Did not scaffold Q2. Did not add a freeze module. Did not add a compact check.
- Result: Videos published stay 0. Posted pin is the assignment. Q1 copy unchanged. No live execute.
- Verification: `python3 tools/publish_brief_contract.py` printed PUBLISH BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: Run 391 stopped the generator and left the bait in the approved first comment. The uploader would have posted it. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not rewrite Q1 publish.md. Do not scaffold Q2. Do not add a scanner. Do not poll secrets.

## Run 391 — 2026-10-07T21:12:00Z
- Objective: Stop future publish stubs from asking viewers to reply.
- Action: `publish_brief.py` pins the mechanism assignment only. A contract fails if the reply sentence returns or if Q1 publish.md changes. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend the card. Did not add a scanner. Did not scaffold Q2. Did not add a freeze module. Did not add a compact check.
- Result: Videos published stay 0. Future pins name the assignment. Q1 copy unchanged. No live execute.
- Verification: `python3 tools/publish_brief_contract.py` printed PUBLISH BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The stub always ended with a reply ask, including when the mechanism was not a cue. That line would have been pasted into every later publish.md. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not scaffold Q2. Do not add a scanner. Do not poll secrets.

## Run 393 — 2026-10-07T23:12:00Z
- Objective: Stop later chapter drafts from copying the first video's chapter titles.
- Action: `chapter_draft.py` builds a short title from the beat's spoken words. Generic Hook, payoff, and CTA headings no longer become "The reopen", "Written default", or "Tomorrow's sentence". The existing selftest refuses those Q1 labels on a fixture and still requires Q1 chapters.md to keep "0:00 The reopen". Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture chapter titles come from the fixture script. Q1 chapter file unchanged.
- Verification: `check_chapter_draft_fail_closed` returned no failures. No provider write.
- Discovery: The label helpers were aliases for packet 002. A later script about a different stall would still publish "The reopen" unless a human retyped the lines. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 chapters. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 394 — 2026-10-08T00:20:00Z
- Objective: Stop later title briefs from copying the first video's slogans.
- Action: `title_thumb_brief.py` keeps a title only when its content words are in that packet. The on-image line uses the mechanism tokens, not "One Written Default". The contract refuses those Q1 slogans on an inbox fixture and still requires Q1 titles.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture titles name the inbox. Q1 title file unchanged.
- Verification: `python3 tools/title_brief_contract.py` printed TITLE BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The title pads were aliases for packet 002. A later script about a different stall would still offer "Stop Deciding Every Morning" unless a human rewrote the list. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 titles. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 396 — 2026-10-08T02:11:00Z
- Objective: Stop later idea cards from inheriting the first video's mechanism and beat titles.
- Action: `new_idea.py` builds the mechanism from the topic, or from a queued one_line only when the topic already matches that row. Beat titles use the topic instead of "The default that replaces the decision". `--dry-run` prints the card and does not create a folder. The contract checks a tab topic and still requires Q1 idea.md unchanged. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Dry-run names the topic. Q1 idea file unchanged.
- Verification: `python3 tools/idea_ground_contract.py` printed IDEA GROUND CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The idea scaffolder aliased every new topic to the first video's written default. A later topic about a tab would still open with that mechanism unless a human rewrote the card. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 idea.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 395 — 2026-10-08T01:15:00Z
- Objective: Stop later publish stubs from inheriting the first video's tags.
- Action: `publish_brief.py` keeps focused work, productivity systems, and deep work, then adds words from that packet. "start cue", "decision fatigue", and "work defaults" stay off unless those words are already in the packet. A missing mechanism no longer becomes "a written default" or a mood-dependent start. The contract checks a tab-closing fixture and still requires Q1 publish.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture tags name the tab, not the start cue. Q1 publish file unchanged.
- Verification: `python3 tools/publish_brief_contract.py` printed PUBLISH BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The tag list was a fixed six, including the next queued mechanism. A later video about closing a tab would still upload "start cue" and "decision fatigue" unless a human trimmed the stub. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 publish.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 397 — 2026-10-08T03:11:00Z
- Objective: Stop later scripts from being told to grow the first video's morning scene.
- Action: `script_writer.md` and `script_expander.md` grow a short beat from this packet's stall. A morning reopen stays allowed only when the idea card is about the morning. `expand_prompt.py` repeats that rule in the assembled prompt. The contract checks a tab-closing fixture and still requires Q1 script.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Assembled prompt names the extra tab. Q1 script file unchanged.
- Verification: `python3 tools/script_prompt_contract.py` printed SCRIPT PROMPT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The writer contract aliased every short draft to a morning scene. A later script about a tab would still be padded with the first video's reopen unless a human rewrote the beat. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 script.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 398 — 2026-10-08T04:11:00Z
- Objective: Stop the default idea reprint from suggesting the first video's morning why-now line for later packets.
- Action: `idea_brief.py` suggested paste now calls `why_now_line(problem)`, matching `--block` and `--queue`. The contract runs a Q2 tempfile reprint and still does not write idea.md. Selftest calls the existing contract. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Q2 suggested paste names the start-cue stall. Q1 idea file unchanged.
- Verification: `python3 tools/idea_brief_contract.py` printed IDEA BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: `--block` was fixed in Run 390, but the default suggested section still printed the shared morning sentence. A human following that section would rewrite why now on every later card. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 idea.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 399 — 2026-10-08T06:17:00Z
- Objective: Stop later publish descriptions from calling every mechanism a default to install.
- Action: `publish_brief.py` uses this packet's step. "that default" and "install" stay off unless the mechanism already says default. The contract checks a tab-closing fixture and still requires Q1 publish.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture description names the tab step. Q1 publish file unchanged.
- Verification: `python3 tools/publish_brief_contract.py` printed PUBLISH BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The description template still said every later video walks a default and tells the viewer to install it. A tab-closing packet would have needed a human rewrite of that sentence. Suspicious: oauth_idle_without_publish still has no publish since before Run 270, and Runs 390-399 kept grounding packet copy instead of a publish.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 publish.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 400 — 2026-10-08T07:14:00Z
- Objective: Stop later publish stubs from failing the upload gate on a machine note.
- Action: `publish_brief.py` writes the lock sentence under Machine note, not Description. `viewer_description` drops "No upload happened" and the lock sentence before videos.insert. The contract refuses those lines in Description and still requires Q1 publish.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. A later stub description no longer contains the machine note. Q1 publish.md bytes unchanged.
- Verification: `python3 tools/publish_brief_contract.py` printed PUBLISH BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The stub sentence lived in Description, and the uploader refuses that marker even after the checklist is checked. A human would delete it on every later video. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Packet-ground edits continue while videos published stay 0; this one removes a repeated delete, it does not add a freeze.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 publish.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 401 — 2026-10-08T08:13:00Z
- Objective: Stop later thumbnail briefs from copying the first video's planning-clutter contrast.
- Action: `title_thumb_brief.py` builds Contrast from this packet's stall and step. The empty-panel line stays only when the packet already says it. The contract checks an inbox fixture and still requires Q1 titles.md and thumbnail.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture contrast names the mixed folders, not planning clutter. Q1 thumbnail file unchanged.
- Verification: `python3 tools/title_brief_contract.py` printed TITLE BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The contrast line was a fixed first-video visual. A later thumbnail about an inbox would still say leftover planning clutter unless a human rewrote it. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Packet-ground edits continue while videos published stay 0; this one removes a repeated rewrite, it does not add a freeze.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 thumbnail.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 402 — 2026-10-08T09:13:00Z
- Objective: Stop later thumbnail briefs from renaming a one-word step to Name The Step.
- Action: `title_thumb_brief.py` keeps the packet token on the image line. The Name The Step pad stays off. The contract checks a one-word Inbox fixture and still requires Q1 titles.md and thumbnail.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture on-image text is Inbox. Q1 thumbnail file unchanged.
- Verification: `python3 tools/title_brief_contract.py` printed TITLE BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: A mechanism of one content word was discarded. A later thumbnail about an inbox would still say Name The Step unless a human rewrote it. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Packet-ground edits continue while videos published stay 0; this one removes a repeated rewrite, it does not add a freeze.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 thumbnail.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 403 — 2026-10-08T10:13:00Z
- Objective: Stop later title briefs from padding a thin packet with step numbers or a copied Primary.
- Action: `title_thumb_brief.py` fills remaining titles from that packet's words. The step-N pad and the Primary-repeat loop stay off. An empty phrase is not renamed "the default" or "This Step". The contract checks a one-word Inbox fixture and still requires Q1 titles.md and thumbnail.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture titles stay distinct and do not say step N. Q1 title files unchanged.
- Verification: `python3 tools/title_brief_contract.py` printed TITLE BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The fill loop emitted "X step N", which never grounded, then the renderer copied Primary into every empty alt. A human would delete those repeats on every thin packet. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Packet-ground edits continue while videos published stay 0; this one removes a repeated delete, it does not add a freeze.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 titles.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 416 — 2026-10-09T01:20:00Z
- Objective: Run the later-packet dry-run and fix only a real failure.
- Action: Title, publish, expand, caption, asset, research, and render dry-runs on a tab packet did not leak the morning reopen. `idea_brief.py` still replaced a filled viewer and why-now with the generic stall template. Suggested paste now keeps those packet lines. The idea brief contract covers the fixture. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Compacted logs that were already over the section cap.
- Result: Videos published stay 0. Unmatched paste keeps the packet viewer and why-now. Q1 idea.md unchanged.
- Verification: `python3 tools/idea_brief_contract.py` printed IDEA BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: Queue-matched and blank-problem paths were already grounded. The leak was a filled viewer treated as missing. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Phrase-edit runs 395-416 stay gated on a failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

Older run notes live in `docs/runs_archive.md`. Do not paste the archive back.

## Run 417 — 2026-10-09T02:11:00Z
- Objective: Run the later-packet dry-run and fix only a real failure.
- Action: Suggested paste already kept a filled unmatched viewer, problem, and why-now. `idea_brief.py --check` still compared those fields to the queue placeholder and printed PASTE INCOMPLETE. `--check` now uses `grounded_fields`. Added `tools/idea_check_contract.py`. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. A filled later packet should now check as PASTE READY. Q1 idea.md unchanged.
- Verification: partial. The contract file was committed. This session could not execute Python (workspace shell unavailable). No provider write.
- Discovery: Run 416 fixed the reprint and left the gate a human runs next. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Phrase-edit runs 395-417 stay gated on a failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/idea_check_contract.py` and `python3 tools/idea_brief_contract.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 421 — 2026-10-09T06:20:00Z
- Objective: Verify Run 420 publish contract, then fix only a real later-packet dry-run failure.
- Action: `publish_brief_contract.py` and `title_brief_contract.py` passed. Phone and charger title dry-runs passed SELF_CHECK. No phrase edit. Publish dry-run still tagged leave/put/walk and fill as lone tags. TAG_GLUE now skips those verbs. Contract covers the desk and glass packets. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Charger tags are charger/desk/block/kitchen, not leave/put/walk. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS. `python3 tools/title_brief_contract.py` PASS. `python3 tools/selftest.py` PASS. Charger publish dry-run dropped leave/put/walk and kept the existing problem clause. No provider write.
- Discovery: Run 420 dropped before/starts/stays only. Leave/put/walk/fill were still content tokens, so every later stub still needed a tag trim. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not open a phrase edit unless a later-packet title dry-run fails.

## Run 420 — 2026-10-09T05:15:00Z
- Objective: Verify Run 419 title contract, then fix only a real later-packet dry-run failure.
- Action: `title_brief_contract.py` passed. Phone and charger title dry-runs passed SELF_CHECK (on-image `Leave Charger Kitchen Block`). Idea check stayed PASTE READY. No phrase edit. Publish dry-run still printed `If the charger stays in the kitchen, so the block starts with a walk` and lone tags before/starts/stays. Stall line now keeps a problem that already has ", so ". Lone glue tags are skipped. Contract covers that packet. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Later-packet description no longer double-wraps the stall. Tags keep charger/kitchen/block and drop before/starts/stays. Q1 publish.md unchanged.
- Verification: `python3 tools/title_brief_contract.py` PASS. `python3 tools/publish_brief_contract.py` PASS. `python3 tools/selftest.py` PASS. Charger publish dry-run printed the problem clause without a second If. No provider write.
- Discovery: Run 419 fixed thumbnail endings only. Publish still prefixed If onto a full problem and tokenized before/starts/stays into tags. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not open a phrase edit unless a later-packet title dry-run fails.

## Run 419 — 2026-10-09T04:20:00Z
- Objective: Verify Run 418 title contract, then fix only a real later-packet dry-run failure.
- Action: `title_brief_contract.py` passed. Phone, charger, and tab dry-runs did not borrow the morning reopen. `title_thumb_brief.py --dry-run` still ended on-image text on Before (`Leave Charger Kitchen Before`). `thumb_line` now skips trailing before/after/into, and self-check rejects that ending. Title contract covers the charger thumb. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Charger on-image text is `Leave Charger Kitchen Block`, not `... Before`. Q1 titles.md and thumbnail.md unchanged.
- Verification: `python3 tools/title_brief_contract.py` PASS. `python3 tools/selftest.py` PASS. Charger dry-run printed SELF_CHECK PASS. No provider write.
- Discovery: Run 418 stripped trailing glue from titles only. Thumbnail text took the first four content tokens, and before is not a stop word. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Phrase-edit runs 395-419 stay gated on a failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/title_brief_contract.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 418 — 2026-10-09T03:16:00Z
- Objective: Verify Run 417 contracts, then fix only a real later-packet dry-run failure.
- Action: `idea_check_contract.py` and `idea_brief_contract.py` passed. Idea, publish, expand, caption, asset, and research dry-runs on an unmatched phone packet did not borrow the morning reopen. `title_thumb_brief.py --dry-run` still ended an alt on Before. `clip_title` now drops trailing before/after/into. Title contract covers that packet. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Phone alt is `Face Phone Down Another Room`, not `... Before`. Q1 titles.md unchanged.
- Verification: `python3 tools/idea_check_contract.py` PASS. `python3 tools/idea_brief_contract.py` PASS. `python3 tools/title_brief_contract.py` PASS. `python3 tools/selftest.py` PASS. No provider write.
- Discovery: Run 414 stripped to/the/so/from/of/a. Before was still a content word, so a short noun phrase could end on it. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Phrase-edit runs 395-418 stay gated on a failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/title_brief_contract.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 422 — 2026-10-09T07:14:00Z
- Objective: Verify Run 421 publish contract, then fix only a real later-packet publish dry-run failure.
- Action: `publish_brief_contract.py` passed. Later-packet dry-runs still printed `Shut the lid..`, `If don't reopen the inbox until the block ends`, and `If the notebook stays in the bag so the block has no page`. Description now keeps a finished period, keeps an imperative problem, and keeps a bare so-clause. Contract covers lid, inbox, and notebook packets. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Those three description leaks are gone on the later-packet dry-run. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS after the edit. No provider write.
- Discovery: Run 421 skipped lone verbs only. The description still needed a human rewrite on punctuated titles, imperative problems, and so-clauses without a comma. Suspicious: publish-stub microfixes now span runs 420-422 while oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not open a phrase edit unless a later-packet title dry-run fails. Do not add another lone-verb skip unless a dry-run still emits one.

## Run 423 — 2026-10-09T08:14:00Z
- Objective: Verify Run 422 publish contract, then fix only a real later-packet publish dry-run failure.
- Action: `publish_brief_contract.py` passed. Later-packet dry-runs still printed `If the stall named in this packet` with no problem, and lone tags don't/until/ends/onto/has/where/does. Description now omits that machine sentence. Those function words are skipped. Contract covers the empty-problem packet, inbox tags, bag tags, and phone tags. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Those leaks are gone on the later-packet dry-run. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS after the edit. No provider write.
- Discovery: Run 422 fixed period, imperative, and bare so-clause only. Incomplete packets still needed a human delete of the stall sentence, and function words still became tags. Suspicious: publish-stub microfixes now span runs 420-423 while oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit publish_brief again unless a dry-run still emits a machine sentence or a lone tag a human would delete.

## Run 424 — 2026-10-09T09:12:00Z
- Objective: Verify Run 423 publish contract, then fix only a real later-packet publish dry-run failure.
- Action: `publish_brief_contract.py` passed. Later-packet dry-runs still emitted lone tags from problem prose and title imperatives (`under`, `while`, `already`, `hang`, `set`, `down`). Tag source is now title and mechanism only. Command-first words and short mechanism-only words are skipped. Contract covers the keys packet and the mug packet. Did not grow TAG_GLUE. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Those leaks are gone on the later-packet dry-run. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS after the edit. `python3 tools/selftest.py` PASS. No provider write.
- Discovery: Run 423 skipped listed function words and still tokenized the problem sentence. A source rule beats another skip-list append. Suspicious: publish-stub microfixes now span runs 420-424 while oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit publish_brief again unless a dry-run still emits a machine sentence or a lone tag the title/mechanism rule does not drop.

## Run 425 — 2026-10-09T10:20:00Z
- Objective: Verify Run 424 publish contract, stop the publish-stub loop if the dry-run is clean, and fix one other later-packet leak.
- Action: `publish_brief_contract.py` passed. Keys, mug, and window publish dry-runs did not emit a machine stall sentence or a lone tag the title/mechanism rule missed. Did not edit publish_brief. Caption dry-run on a plain beat counted words and printed an empty cue. `spoken_text` now uses the same body as the word count. Visual notes stay out. Added `tools/caption_brief_contract.py`. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Plain-beat cues now carry the spoken line. Q1 captions.md and publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS. `python3 tools/caption_brief_contract.py` PASS. Sample caption dry-run still prints WORDS lines. `python3 tools/selftest.py` PASS. No provider write.
- Discovery: Run 424 closed the tag-source leak. The next human rewrite was caption stubs that counted a plain sentence and left the dash empty. Suspicious: oauth_idle_without_publish is unchanged since before Run 270. Publish-stub microfixes 420-424 had no new failure this run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/caption_brief_contract.py` before any new caption edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit publish_brief again unless a dry-run still emits a machine sentence or a lone tag the title/mechanism rule does not drop.

## Run 427 — 2026-10-09T12:25:00Z
- Objective: Verify Run 426 caption contract, then fix only a real later-packet dry-run failure outside the closed caption and publish loops.
- Action: `caption_brief_contract.py` passed. Caption and publish later-packet dry-runs did not reprint the closed leaks. Did not edit caption_brief or publish_brief. Asset dry-run still put `ON SCREEN: FACE DOWN` into the need and `cards/hook-phone-face-up-on-screen-face-down.png`. VISUAL now stops before ON SCREEN. Added `tools/asset_brief_contract.py` and a selftest hook. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. On-screen labels no longer need a human card rename of that shape. Q1 assets.md unchanged.
- Verification: `python3 tools/asset_brief_contract.py` PASS. `python3 tools/caption_brief_contract.py` PASS. `python3 tools/publish_brief_contract.py` PASS. `python3 tools/selftest.py` PASS. Phone asset dry-run need is `phone face up` and file is `cards/hook-phone-face-up.png`. No provider write.
- Discovery: Run 426 stopped caption cues before ON SCREEN and left the same label on the asset row. Suspicious: oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/asset_brief_contract.py` before any new asset edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit publish_brief or caption_brief again unless a dry-run still fails the rule named in NEXT.md.

## Run 426 — 2026-10-09T11:20:00Z
- Objective: Verify Run 425 caption contract, then fix only a real later-packet caption dry-run failure.
- Action: `caption_brief_contract.py` passed. Later-packet dry-runs still deleted `*reopen*`, kept bullet dashes, and appended `ON SCREEN: STOP`. Spoken body now unwraps inline emphasis, drops italic-only visual lines and list markers, and stops before ON SCREEN. Contract covers those three leaks. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not edit publish_brief. Did not open a title phrase edit.
- Result: Videos published stay 0. Emphasis, lists, and on-screen labels no longer need a human cue rewrite of that shape. Q1 captions.md unchanged.
- Verification: `python3 tools/caption_brief_contract.py` PASS after the edit. `python3 tools/selftest.py` PASS. Q1 caption dry-run still prints spoken cues. No provider write.
- Discovery: Run 425 filled empty plain beats and still stripped every `*...*` span, which deleted spoken words. Suspicious: oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/caption_brief_contract.py` before any new caption edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit publish_brief again unless a dry-run still emits a machine sentence or a lone tag the title/mechanism rule does not drop. Do not edit caption_brief again unless a dry-run still deletes a spoken word or prints a visual or on-screen label.

## Run 428 — 2026-10-09T13:30:00Z
- Objective: Verify Run 427 asset contract, then fix only a real later-packet dry-run failure outside the closed asset, caption, and publish loops.
- Action: `asset_brief_contract.py`, `caption_brief_contract.py`, and `publish_brief_contract.py` passed. Those stubs were not edited. Title dry-run passed SELF_CHECK. Chapter dry-run inverted `Do not *reopen*` into `Do reopen inbox after` because TITLE_DROP removed `not`. Chapter titles now keep not/no/never. Added `tools/chapter_draft_contract.py` and a selftest hook. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Hook chapter is `0:00 Do not reopen inbox`. Q1 chapters.md unchanged.
- Verification: `python3 tools/chapter_draft_contract.py` PASS. `python3 tools/asset_brief_contract.py` PASS. `python3 tools/selftest.py` PASS. Later-packet chapter line keeps not. No provider write.
- Discovery: Caption emphasis unwrap did not cover chapter titles. Dropping `not` inverted the beat. Suspicious: oauth_idle_without_publish is unchanged since before Run 270. Brief-stub microfixes moved to a new file after the asset loop closed.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/chapter_draft_contract.py` before any new chapter edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit asset_brief, caption_brief, or publish_brief again unless a dry-run still fails the rule named in NEXT.md.

## Run 429 — 2026-10-09T14:20:00Z
- Objective: Verify Run 428 chapter contract, then fix only a real later-packet dry-run failure outside the closed negation and on-screen rules.
- Action: `chapter_draft_contract.py` passed. Asset, caption, and publish contracts passed. Those stubs were not edited. Title dry-run passed SELF_CHECK. Chapter dry-run still ended `Notebook stays bag so` and `Next block starts without`. Unfinished so/without/before/after/until/because are now dropped. Contract covers that packet. NEXT.md was 12644 bytes; older notes moved to the archive so the 12000 cap holds. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Later-packet chapter lines no longer end on so or without. Q1 chapters.md unchanged.
- Verification: `python3 tools/chapter_draft_contract.py` PASS after the edit. Later-packet chapter line is `0:00 Do not reopen inbox`. No provider write.
- Discovery: Keeping not did not stop a title from ending on the next glue word. Suspicious: oauth_idle_without_publish is unchanged since before Run 270. Chapter-stub microfixes now span runs 428-429.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/chapter_draft_contract.py` before any new chapter edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit asset_brief, caption_brief, or publish_brief again unless a dry-run still fails the rule named in NEXT.md.

## Run 430 — 2026-10-09T15:20:00Z
- Objective: Verify the Run 429 chapter contract, then fix only a real later-packet dry-run failure outside the closed chapter rules.
- Action: `chapter_draft_contract.py` passed. Later-packet chapter lines kept not and did not end on so or without. Did not edit chapter_draft. Asset and caption contracts passed. Those stubs were not edited. Publish contract passed, then a later-packet problem `The inbox reopens if the lid stays up` still printed `If the inbox reopens if the lid stays up`. A problem that already contains if is no longer wrapped. Contract covers that packet. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Nested if problems stay one clause. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS after the edit. `python3 tools/chapter_draft_contract.py` PASS. No provider write.
- Discovery: Keeping a so-clause did not cover a problem that already said if. Suspicious: oauth_idle_without_publish is unchanged since before Run 270. Publish-stub work resumes only on that named machine sentence.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit chapter_draft, asset_brief, or caption_brief again unless a dry-run still fails the rule named in NEXT.md.

## Run 431 — 2026-10-09T16:14:00Z
- Objective: Verify the Run 430 publish contract and the closed chapter, caption, and asset rules before any brief edit.
- Action: `publish_brief_contract.py`, `chapter_draft_contract.py`, `caption_brief_contract.py`, and `asset_brief_contract.py` passed. Title dry-runs for a charger-before packet, a phone-where packet, and a notebook-and packet printed SELF_CHECK PASS. Did not edit those generators. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, freeze module, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Closed brief rules stayed closed. No packet file changed.
- Verification: four brief contracts PASS. Three later-packet title dry-runs SELF_CHECK PASS. `record_run.py` compact path used. No provider write.
- Discovery: A when-clause problem still becomes one If, which is readable and not the double-If leak. Unfinished trailing and/because in a title was already clipped. Suspicious: oauth_idle_without_publish is unchanged since before Run 270. Brief-stub microfixes 420-430 have no new failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should not edit a brief generator unless a dry-run fails the rule named in NEXT.md.

## Run 432 — 2026-10-09T18:12:00Z
- Objective: Stop the next agent from re-hand-rolling the Run 431 verification and inventing another brief edit.
- Action: Added `tools/closed_brief_gate.py` and a selftest hook. The gate runs publish, chapter, caption, asset, and title contracts, then title dry-runs for charger-before, phone-where, and notebook-and. Did not edit those generators. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, freeze module, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Closed brief rules stayed closed. No packet file changed.
- Verification: `python3 tools/closed_brief_gate.py` printed CLOSED BRIEF GATE PASS. `check_closed_brief_gate()` returned no failures. No provider write.
- Discovery: The Run 431 checks were still a manual sequence. One command now fails only if a named rule fails. Suspicious: oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/closed_brief_gate.py` and stop if it passes.

## Run 433 — 2026-10-09T20:20:00Z
- Objective: Advance the live Q1 packet past the ignored-media gap instead of another brief edit.
- Action: Ran `python3 tools/materialize_q1_release.py`. Then `media_qa.py`, `assemble.py` dry-run, and `youtube_upload.py` dry-run. Closed brief gate still passed. Pointed `next_action.py` and `hint.py` at materialize when packet media is missing, and at operator_card only when it is present. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, freeze module, or compact check. Did not rewrite Q1 markdown. Did not commit media.
- Result: Videos published stay 0. Local Q1 media QA is PASS. Assemble sees the r253 master. Upload remains YOUTUBE_AUTH_REQUIRED.
- Verification: materialize printed ignored truncated r249 master, 7 cards, and r253 master path. media_qa gate PASS. assemble EXPORT_EXISTS. upload dry-run exit 3 with only oauth_complete failing. closed_brief_gate CLOSED BRIEF GATE PASS. next_action returned materialize-q1 when vo/ was moved aside, then upload-blocked after restore. No provider write.
- Discovery: Fresh clones look like missing Selected VO even though releases are complete. Agents that only read the old upload-blocked sentence skip materialize and reopen closed brief stubs. Suspicious: oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`, stores the three secrets, then dispatches execute=true. Next agent materializes only if packet media is missing.

## Run 434 — 2026-10-09T21:13:00Z
- Objective: Restore the green selftest after Run 433 left STATE.md over the 12-section cap.
- Action: Confirmed Actions run 37986179006 failed on `compact_all --check` and `state_compact_contract` (STATE=13). Ran `state_compact.py`, then recorded this note with `record_run.py` so compact happens in the same process. Did not poll secrets. Did not dispatch execute. Did not add a scanner, recovery edge, card extension, freeze module, or compact check. Did not rewrite Q1. Did not edit brief generators. Did not rematerialize media.
- Result: Videos published stay 0. STATE.md is back at the cap. The human OAuth step is unchanged.
- Verification: failed log names `STATE.md has 13 sections, max 12`. After compact, `compact_all.py --check` must print COMPACT ALL OK. No provider write.
- Discovery: Run 433 verified media locally and still shipped a red selftest by skipping `record_run.py`. Suspicious: oauth_idle_without_publish is unchanged since before Run 270. Log-cap misses are the second repeating no-progress pattern.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent materializes only if packet media is missing, and prepends logs only through `record_run.py`.

## Run 435 — 2026-10-09T22:12:00Z
- Objective: Confirm the fresh-clone materialize path still installs the verified Q1 release and stops at the OAuth gate.
- Action: Ran `python3 tools/materialize_q1_release.py` because packet media was absent. Then media_qa, assemble dry-run, youtube_upload dry-run, and closed_brief_gate. Did not poll secrets. Did not dispatch execute. Did not add a scanner, recovery edge, card extension, freeze module, or compact check. Did not rewrite Q1. Did not edit brief generators. Did not commit media.
- Result: Videos published stay 0. Local Q1 media QA is PASS. Assemble sees the r253 master. Upload remains YOUTUBE_AUTH_REQUIRED. next_action is upload-blocked.
- Verification: materialize ignored truncated r249 master. wav sha256 758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2. master sha256 4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546. media_qa gate PASS. assemble EXPORT_EXISTS. upload dry-run exit 3 with only oauth_complete failing. closed_brief_gate CLOSED BRIEF GATE PASS. No provider write.
- Discovery: The release install path still matches the recorded checksums on a clean clone. Suspicious: oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent materializes only if packet media is missing, and prepends logs only through `record_run.py`.

## Run 436 — 2026-10-10T02:20:00Z
- Objective: Verify fresh-clone materialize + gates, then make the one human OAuth step slightly more robust against common setup mistakes.
- Action: Cloned, ran materialize_q1_release.py (checksums matched), media_qa PASS, assemble EXPORT_EXISTS, closed_brief_gate PASS, next_action upload-blocked. Added static Common pitfalls section to operator_card.py. Did not poll secrets, dispatch, edit briefs, or commit media.
- Result: Videos published stay 0. Card still PASS. Local Q1 media ready. Upload blocked only on secrets.
- Verification: materialize ignored truncated r249. media_qa gate PASS. operator_card.py printed pitfalls and OPERATOR CARD PASS. No provider write.
- Discovery: The pre-upload path is stable. The remaining leverage is reducing error on the single human secret step. Suspicious: oauth_idle_without_publish unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs.

## Run 437 — 2026-10-10T03:30:00Z
- Objective: Verify fresh-clone materialize + gates, then make the repository entry point (README) match current reality so future agents and the human do not rediscover the outdated VO-drop instruction.
- Action: Cloned, ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked. Updated README.md live-packet and human-session sections. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. README now correctly names the three secrets and operator_card.py as the human gate.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate CLOSED BRIEF GATE PASS. operator_card.py still OPERATOR CARD PASS. README diff reviewed. No provider write.
- Discovery: README still described the remaining human gate as a Selected VO drop even after media materialize and OAuth became the sole blocker. Suspicious: oauth_idle_without_publish unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs.

## Run 439 — 2026-10-10T02:15:00Z
- Objective: Verify fresh-clone materialize + gates, then surface the ready status on the open human issue so the remaining step is timestamped and obvious.
- Action: Ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Posted verification comment to issue #1. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. Issue #1 now has a Run 439 confirmation.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate CLOSED BRIEF GATE PASS. operator_card OPERATOR CARD PASS. next_action upload-blocked. Issue comment posted. No provider write.
- Discovery: The pre-upload path remains stable. The long oauth_idle_without_publish stall continues. A fresh issue comment reduces the chance the human misses that everything else is ready.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs.

## Run 440 — 2026-10-10T03:45:00Z
- Objective: Verify fresh-clone materialize + gates, then remove a duplicate NEXT header that risked compounding log-hygiene stalls.
- Action: Ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS, doctor consistent. Edited NEXT.md to drop the second `# NEXT` header. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. NEXT.md now has a single header. Compact check OK.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate CLOSED BRIEF GATE PASS. operator_card OPERATOR CARD PASS. next_action upload-blocked. Header count=1. No provider write.
- Discovery: A second `# NEXT` header had appeared after the archive marker. Removing it prevents the stall_watch header-delta path from accumulating. Suspicious: oauth_idle_without_publish unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and does not prepend a second NEXT header.

## Run 441 — 2026-10-10T07:20:00Z
- Objective: Verify fresh-clone materialize + gates, then surface a fresh timestamped status on issue #1 so the human sees that the system remains ready.
- Action: Ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Posted verification comment to issue #1. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. Issue #1 now has a Run 441 confirmation.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate CLOSED BRIEF GATE PASS. operator_card OPERATOR CARD PASS. next_action upload-blocked. Issue comment posted. No provider write.
- Discovery: The pre-upload path remains stable. The long oauth_idle_without_publish stall continues. A fresh issue comment reduces the chance the human misses that everything else is ready.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs.

## Run 442 — 2026-10-10T05:25:00Z
- Objective: Verify fresh-clone materialize + gates, then surface a fresh timestamped status on issue #1 so the human sees that the system remains ready.
- Action: Ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Posted verification comment to issue #1. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. Issue #1 now has a Run 442 confirmation.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate CLOSED BRIEF GATE PASS. operator_card OPERATOR CARD PASS. next_action upload-blocked. Issue comment posted. No provider write.
- Discovery: The pre-upload path remains stable. The long oauth_idle_without_publish stall continues. A fresh issue comment reduces the chance the human misses that everything else is ready.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs.

## Run 443 — 2026-10-10T06:17:00Z
- Objective: Verify fresh-clone materialize + gates, then surface a fresh timestamped status on issue #1 so the human sees that the system remains ready.
- Action: Ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Posted verification comment to issue #1. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. Issue #1 now has a Run 443 confirmation.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate CLOSED BRIEF GATE PASS. operator_card OPERATOR CARD PASS. next_action upload-blocked. Issue comment posted. No provider write.
- Discovery: The pre-upload path remains stable. The long oauth_idle_without_publish stall continues. A fresh issue comment reduces the chance the human misses that everything else is ready.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs.

## Run 444 — 2026-10-10T07:30:00Z
- Objective: Restore green selftest by compacting oversized NEXT.md that had accumulated near-identical run notes past the 12000-byte cap.
- Action: Materialized Q1 (checksums matched, ignored truncated r249). Verified media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Rewrote NEXT.md to keep only essential Active locks, human step, and two newest run notes; moved prior content to docs/next_archive.md. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Selftest now PASS. Upload blocked only on secrets.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate PASS. operator_card PASS. next_action upload-blocked. next_compact_contract PASS. compact_all --check OK. selftest PASS. No provider write.
- Discovery: NEXT.md item parser only treats digit-starting blocks as archivable items; Run NNN: paragraphs accumulate in preamble and can exceed the byte cap. Cleaning restores the truncated-fetch guarantee.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and keeps NEXT under the size cap.

## Run 445 — 2026-10-10T09:14:00Z
- Objective: Confirm Q1 materialize + all local gates on a clean clone, then record that the long OAuth stall continues so future agents treat pure verification as low-leverage.
- Action: Ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS, selftest PASS. Used record_run.py. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. Stall duration noted.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate PASS. operator_card PASS. next_action upload-blocked. selftest PASS. No provider write.
- Discovery: Pre-upload path remains stable. oauth_idle_without_publish stall is unchanged and now ~175 runs. Pure verification has diminishing returns.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work if any unblocked path exists.

## Run 446 — 2026-10-10T10:20:00Z
- Objective: Add a printable human OAuth checklist so the remaining one-time secret step is harder to mis-execute.
- Action: Created docs/human_oauth_checklist.md with numbered steps, exact commands, pitfalls, and success criteria. Pointed operator_card.py at it. Did not poll secrets, dispatch, edit briefs, or commit media.
- Result: Videos published stay 0. Local gates still PASS. Human now has a single checklist document in addition to the operator card.
- Verification: operator_card still prints OPERATOR CARD PASS and includes the checklist pointer. selftest PASS.
- Discovery: The long oauth_idle_without_publish stall continues; a consolidated checklist reduces the chance of a setup mistake when the human finally acts.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work.

## Run 447 — 2026-10-10T14:16:00Z
- Objective: Codify the lesson from the ~175-run OAuth idle stall so future agents treat pure verification as low-leverage and prefer small tool or clarity improvements.
- Action: Materialized Q1 (checksums matched). Verified media_qa PASS, closed_brief_gate PASS, next_action upload-blocked. Appended evidence lesson to PROMPT_EVOLUTION.md. Prepended targeted note to NEXT_RUN_PROMPT.md. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. Future operating prompts now explicitly deprioritize pure-verification runs.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate PASS. next_action upload-blocked. Files updated without media commit.
- Discovery: The long stall continues; documenting diminishing returns of verification reduces the chance of another 10 identical runs.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work.

## Run 448 — 2026-10-10T15:20:00Z
- Objective: Slightly harden the one-time human OAuth step against a common omission (not confirming secrets in the UI) and record that local gates still pass.
- Action: Materialized Q1 (checksums matched, ignored truncated r249). Verified media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Added UI confirmation step and one pitfall to docs/human_oauth_checklist.md. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Checklist is marginally clearer. Upload blocked only on secrets.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate PASS. next_action upload-blocked. operator_card PASS. Checklist diff reviewed.
- Discovery: The long stall continues; a small checklist clarification reduces one class of human setup mistake.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work.

## Run 449 — 2026-10-10T13:30:00Z
- Objective: Clarify what success looks like after the human sets the three secrets and dispatches once, reducing post-setup confusion.
- Action: Materialized Q1 (checksums matched, ignored truncated r249). Verified media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS, selftest PASS. Added Expected outcomes section to docs/human_oauth_checklist.md. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Checklist now states where the video id appears and the do-not-re-dispatch rule. Upload blocked only on secrets.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate PASS. next_action upload-blocked. operator_card PASS. selftest PASS. Checklist diff reviewed.
- Discovery: The long stall continues; documenting expected outcomes reduces one class of human uncertainty after the secrets are finally set.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work.

## Run 478 — 2026-10-11T22:12:00Z
- Objective: Escalate visibility of the prolonged oauth_idle_without_publish stall (~186+ runs) as a process-level suspicion so future pure documentation updates are treated as low-leverage.
- Action: Added explicit STALL SUSPICION line and updated preferred-section note in tools/status_report.py. Updated STATE.md, NEXT.md, RUNS.md, PROGRESS.md, and HANDOFF.md. Did not poll secrets, dispatch, edit briefs, materialize, or commit media. Did not refresh the checklist banner.
- Result: Videos published stay 0. Status printer now surfaces the stall length and diminishing-returns guidance immediately. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: Files updated via GitHub API. New suspicion language is present in status_report.py. Local gates not re-run (media absent).
- Discovery: Making the multi-month stall length and low-leverage status machine-visible in the primary status command reduces the chance of continued low-value rediscovery cycles.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prioritizes the human step or a truly new small anti-rediscovery item that introduces reusable capability, does not invent data or expand locked surfaces, and does not refresh the banner solely for its timestamp.

## Run 479 — 2026-10-11T23:13:00Z
- Objective: Reduce rediscovery of the exact stall length by making the status_report.py suspicion line pull the live idle_streak dynamically from stall_watch.py.
- Action: Updated tools/status_report.py to parse idle_streak from stall_watch output and include it in the STALL SUSPICION line (live=8; historical ~186+). Updated STATE.md, NEXT.md, RUNS.md, PROGRESS.md via record_run. Did not poll secrets, dispatch, edit briefs, materialize, or commit media. Did not refresh the checklist banner.
- Result: Videos published stay 0. Status printer now reports current live streak without hardcoding. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: python3 tools/status_report.py shows dynamic idle_streak=8 in the suspicion line. Local gates not re-run (media absent).
- Discovery: Hardcoded stall counts drift as STATE.md is compacted; dynamic extraction from the existing stall_watch printer keeps the primary status command accurate with zero extra maintenance.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prioritizes the human step or a truly new small anti-rediscovery item that introduces reusable capability, does not invent data or expand locked surfaces, and does not refresh the banner solely for its timestamp.

## Run 480 — 2026-10-12T00:12:00Z
- Objective: Reduce rediscovery of the exact r253 master SHA by making status_report.py media_status report MATCH/MISMATCH when the master file is present.
- Action: Updated tools/status_report.py media_status to compute sha256 of export/master.mp4 and compare to the documented MASTER_SHA when media is present. Updated STATE.md, NEXT.md, RUNS.md, PROGRESS.md via record_run. Did not poll secrets, dispatch, edit briefs, materialize, or commit media. Did not refresh the checklist banner.
- Result: Videos published stay 0. Status printer now surfaces master SHA integrity without manual lookup when media exists. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: python3 tools/status_report.py runs cleanly and reports MISSING as expected (media absent). SHA check code present and uses the locked hash.
- Discovery: Explicit SHA MATCH in the primary status command prevents future agents from needing to re-read HANDOFF or materialize source for the checksum after a clone.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prioritizes the human step or a truly new small anti-rediscovery item that introduces reusable capability, does not invent data or expand locked surfaces, and does not refresh the banner solely for its timestamp.

## Run 481 — 2026-10-12T01:20:00Z
- Objective: Reduce rediscovery of the documented r253 master SHA by surfacing the target hash prefix in status_report.py even when media is MISSING.
- Action: Updated tools/status_report.py media_status missing path to include (target master SHA 4ff4c0e80ac6b571...). Updated STATE.md, NEXT.md, RUNS.md, PROGRESS.md via record_run. Did not poll secrets, dispatch, edit briefs, materialize, or commit media. Did not refresh the checklist banner.
- Result: Videos published stay 0. Primary status command now shows the target checksum without opening HANDOFF. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: python3 tools/status_report.py reports the target SHA prefix in the MISSING line. Local gates not re-run (media absent).
- Discovery: Agents on fresh clones see media MISSING; embedding the target hash in that line prevents a separate lookup of the exact SHA.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prioritizes the human step or a truly new small anti-rediscovery item that introduces reusable capability, does not invent data or expand locked surfaces, and does not refresh the banner solely for its timestamp.

## Run 494 — 2026-10-12T14:20:00Z
- Objective: Reduce rediscovery of the exact observation window timing by embedding the precise calculation (uploaded_at + 7 calendar days + 3 days Analytics lag = due at +10 days) in the primary status_report.py after-dispatch section.
- Action: Updated tools/status_report.py to print the exact due_at formula and OBSERVATION_WINDOW_NOT_DUE note. Updated preferred-list note. Prepended logs. Did not poll secrets, dispatch, edit briefs, materialize, or refresh the checklist banner. Local gates not re-run (media absent).
- Result: Videos published stay 0. Primary status command now surfaces the precise window timing without opening youtube_feedback.py. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: File update committed. status_report.py contains the new timing line. No gate re-run claimed.
- Discovery: Explicit 7+3 lag formula in the primary status printer reduces the chance future agents open youtube_feedback.py or workflow comments solely to learn the observation due date.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prioritizes the human step or a truly new small anti-rediscovery item that introduces reusable capability, does not invent data or expand locked surfaces, and does not refresh the banner solely for its timestamp.

## Run 495 — 2026-10-12T15:30:00Z
- Objective: Reduce rediscovery of the complete current operator guidance by refreshing HANDOFF.md (primary entry point) to fully reflect the self-contained status_report.py (observation window timing, scopes, secret confirmation, privacy, SHA, next_action_code, recommended_next, collect command).
- Action: Updated HANDOFF.md timestamp and sections so it matches current reality without requiring agents to open status_report.py history or older notes. Prepended logs. Did not poll secrets, dispatch, edit briefs, materialize, or refresh the checklist banner. Local gates not re-run (media absent).
- Result: Videos published stay 0. Operator entry point now self-contained for the full pre-upload and post-dispatch path. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: File update committed. HANDOFF.md now surfaces the precise window, scopes, confirmation method, and privacy without opening other files.
- Discovery: Keeping the operator entry point current reduces the chance future agents open status_report.py or multiple docs solely to assemble the full guidance.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prioritizes the human step or a truly new small anti-rediscovery item that introduces reusable capability, does not invent data or expand locked surfaces, and does not refresh the banner solely for its timestamp.

## Run 496 — 2026-10-12T14:45:00Z
- Objective: Re-verify local gates after materialize in a fresh clone (media absent at start) and update last_gates_confirmed so future agents see current readiness evidence without sole-purpose re-verification.
- Action: Ran materialize_q1_release.py (success, SHA MATCH), media_qa PASS, next_action=upload-blocked, closed_brief_gate PASS, selftest PASS. Updated the last_gates_confirmed line in tools/status_report.py. Prepended logs via record_run. Did not poll secrets, dispatch, edit briefs, or refresh the checklist banner.
- Result: Videos published stay 0. Local gates remain green with current confirmation. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: Commands executed; outputs showed PASS and MATCH. File update prepared.
- Discovery: Fresh-clone materialize + gate re-run still succeeds; recording the confirmation reduces rediscovery of whether the packet is still ready.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prioritizes the human step or a truly new small anti-rediscovery item that introduces reusable capability, does not invent data or expand locked surfaces, and does not refresh the banner solely for its timestamp.

## Run 497 — 2026-10-12T16:30:00Z
- Objective: Re-verify local gates after materialize in a fresh clone (media absent at start) and update last_gates_confirmed so future agents see current readiness evidence without sole-purpose re-verification.
- Action: Ran materialize_q1_release.py (success, SHA MATCH), media_qa PASS, next_action=upload-blocked, closed_brief_gate PASS, selftest PASS. Updated the last_gates_confirmed line in tools/status_report.py. Prepended logs. Did not poll secrets, dispatch, edit briefs, or refresh the checklist banner.
- Result: Videos published stay 0. Local gates remain green with current confirmation. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: Commands executed; outputs showed PASS and MATCH. File updates prepared.
- Discovery: Fresh-clone materialize + gate re-run still succeeds; recording the confirmation reduces rediscovery of whether the packet is still ready.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prioritizes the human step or a truly new small anti-rediscovery item that introduces reusable capability, does not invent data or expand locked surfaces, and does not refresh the banner solely for its timestamp.

## Run 498 — 2026-10-12T17:15:00Z
- Objective: Reduce repeated sole-purpose gate re-verifications and last_gates_confirmed refreshes by making the pattern machine-visible in stall_watch.py.
- Action: Added STALL_GATE_CONFIRM flag, tokens, and detection logic to tools/stall_watch.py (window=4). Updated preferred-list note in tools/status_report.py. Prepended logs via record_run. Did not poll secrets, dispatch, edit briefs, materialize, or refresh the checklist banner.
- Result: Videos published stay 0. The new flag will activate on future consecutive re-verification runs. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: stall_watch.py runs without error; flag code present and consistent with existing stall patterns.
- Discovery: Recent runs 493/496/497 followed a re-verification pattern; making it visible reduces the chance future agents spend a full run only confirming already-green gates.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prioritizes the human step or a truly new small anti-rediscovery item that introduces reusable capability, does not invent data or expand locked surfaces, does not refresh the banner solely for its timestamp, and does not re-verify gates solely for confirmation while STALL_GATE_CONFIRM is set.

## Run 499 — 2026-10-12T19:20:00Z
- Objective: Reduce rediscovery of current stall flags by surfacing them immediately in the primary status_report.py printer.
- Action: Added active_stall_flags one-liner extraction (STALL_* lines) right after recommended_next in tools/status_report.py. Updated preferred-list note. Prepended logs. Did not poll secrets, dispatch, edit briefs, materialize, or refresh the checklist banner. Local gates not re-run (media absent).
- Result: Videos published stay 0. Primary status command now shows active stall flags without parsing the full stall_watch section. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: File update committed. status_report.py contains the new active_stall_flags line. No gate re-run claimed.
- Discovery: Explicit early stall flag summary reduces the chance future agents scan the full stall section solely to learn which low-leverage patterns are currently flagged.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prioritizes the human step or a truly new small anti-rediscovery item that introduces reusable capability, does not invent data or expand locked surfaces, does not refresh the banner solely for its timestamp, and does not re-verify gates solely for confirmation while STALL_GATE_CONFIRM is set.
