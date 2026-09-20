# STATE

Updated: 2026-09-20T18:20:00Z (Run 238)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + narration adapter + labeled generated fallback + local card generator + WORDS timeline planner + fail-closed media QA (header + PCM peak/RMS/silence/clip + export ftyp when present) + credential-ready dry-run uploader (ftyp-required master + selftest lock) + fail-closed ffmpeg assemble planner + fail-closed feedback collector + fail-closed experiment ledger + fail-closed completion gate + HEAD selftest lock for experiment/complete/level-checks/export-ftyp/upload-junk-master + gate-machine drop recipe with optional local TTS one-liners + operator/agent pages, hint/next_action, and pipeline_status missing-VO DROP point at that drop + hint.py and next_action.py post-VO codes name existing CLIs + clone-less bootstrap/doctor reconstruct fetch docs/gate_machine.md + WAVE 3 queue_status/next_topic hold Q2 and print that hold before scaffold copy-paste + README Human session / Local tools lead with the Q1 drop before doctor/idea_brief/new_packet -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- script.md 952 IN BAND; status `ready_for_vo`; selected take not in git
- Run 238: README front door now lists the packet-relative drop and narration_adapter before doctor/queue/idea_brief/new_packet. Scaffold and sample-001 commands stay printed but labeled parked until Q1 ships. No new adapter. No invented wav/mp4. Production freeze otherwise honored.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.
- Executive trajectory decision: SHIP the first completed video before adding further broad architecture.

## What exists now (after Run 238)
- idea.md / draft.md / script.md / titles.md / thumbnail.md filled
- vo_session.md ready-to-record; named take missing from git
- vo_origin.md kind=generated (labeled fallback)
- captions.md stub with DROP; assets.md 7 planned cards; publish.md stub
- qa.md mechanical PASS; human VO box unchecked
- render.md all-missing plus DROP line
- packet.md status `ready_for_vo`
- Queue Q1 used; Q2-Q5 queued
- Packet listing has no committed `vo/` audio and no committed card PNGs
- Completion gate PLAN_BUILT (`tools/complete.py` on main)
- Selftest DROP lock for experiment_loop.py / complete.py / youtube_upload.py is on HEAD
- media_qa level checks + export ftyp sniff on HEAD; youtube_upload ftyp on HEAD; upload fail-closed fixture on HEAD; fail-closed without a take
- Gate-machine drop recipe: `docs/gate_machine.md` (includes optional already-installed TTS one-liners)
- human_session + agent_session + hint/next_action + pipeline_status point that drop at gate_machine
- hint.py and next_action.py post-VO codes now match NEXT steps 3-4
- Clone-less first-fetch includes the drop page (7 bootstrap paths)
- WAVE 3 board printers name the Q2 hold *first*
- README Human session / Local tools name the Q1 drop *first*

## Pipeline map
On the machine that runs gates (`docs/gate_machine.md`):
1. Place Selected VO at the packet-relative DROP path (record, cp an existing generated file, or use one optional TTS one-liner on that page)
2. narration_adapter.py then vo_session.py --force
3. card_generator.py --write-manifest (do not git add -f pngs)
4. timeline.py --write then media_qa.py (expect peak/RMS/silence/clip; export_decodable only if a master exists)
5. assemble.py without --execute until READY_TO_ENCODE
6. youtube_upload.py after a local master with a real ftyp box
7. youtube_feedback.py after a real provider_video_id
8. experiment_loop.py after real metrics
9. complete.py (expect INCOMPLETE_MEDIA until VO+cards exist; junk mp4 is still incomplete)
Do not invent a committed wav or mp4. Do not upload. Do not scaffold Q2.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|
| Estimated human min / video | 3.8 | 3.7 | README no longer leads with doctor/scaffold |
| Automated steps | 94 | 94 | freeze: still no 95th adapter |
| Videos produced | 0 | 0 | ready_for_vo; take not on gate machine |

## Capability roadmap status
- Completion gate: PLAN_BUILT (complete.py + HEAD selftest lock)
- Experiment loop selftest lock: DONE on HEAD (Run 222)
- Media QA loudness/silence/clip: LANDED on HEAD (Run 223)
- Export ftyp sniff: LANDED on HEAD for media_qa/assemble/complete (Run 224) and youtube_upload (Run 225)
- Upload junk-master selftest: LANDED on HEAD (Run 226; still READY_FOR_MEDIA / READY_FOR_CREDENTIAL)
- Runs 227-237: freeze honor / drop-page / printer / reconstruct / WAVE 3 hold-before-scaffold
- Run 238: README hold-before-scaffold order; no capability change

## Active constraints
- Do not add another dry-run adapter before on-disk Selected VO
- Do not invent a committed wav or bump status past ready_for_vo without Selected VO on disk
- Do not treat complete.py INCOMPLETE_* as license to invent media or a keep/discard
- Do not write a dummy export/master.mp4 to flip gates
- Do not add another selftest fixture unless a live printer regression is proven on HEAD
- Do not treat docs/gate_machine.md as permission to commit sandbox audio
- Do not wrap the optional TTS one-liners into tools/
- Do not restore "recording is the only gate" or blanket "no ffmpeg recipe" language on operator pages or hint.py edit commands
- Do not strip the docs/gate_machine.md pointer from hint.py / next_action.py / pipeline_status.py
- Do not revert hint.py or next_action.py build-cards/edit to stock-download or editor-only wording
- Do not strip docs/gate_machine.md from needed.py BOOTSTRAP or doctor UNMAPPED_PATHS
- Do not strip the Q1 gate_machine hold from queue_status.py or next_topic.py
- Do not move scaffold copy-paste above the Q1 hold in queue_status.py, next_topic.py, or the doctor footer
- Do not move README Human session / Local tools doctor, idea_brief, new_packet, or sample-001 commands above the live Q1 drop
