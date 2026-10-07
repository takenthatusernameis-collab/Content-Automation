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
