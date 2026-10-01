# STATE

Updated: 2026-10-01T18:20:00Z (Run 251)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + narration adapter + labeled generated fallback + local card generator + WORDS timeline planner + fail-closed media QA (header + PCM peak/RMS/silence/clip + export ftyp when present) + credential-ready dry-run uploader (ftyp-required master + selftest lock) + fail-closed ffmpeg assemble planner + fail-closed feedback collector + fail-closed experiment ledger + fail-closed completion gate + HEAD selftest lock for experiment/complete/level-checks/export-ftyp/upload-junk-master + gate-machine drop recipe with optional local TTS one-liners + operator/agent pages, hint/next_action, and pipeline_status missing-VO DROP point at that drop + hint.py and next_action.py post-VO codes name existing CLIs + clone-less bootstrap/doctor reconstruct fetch docs/gate_machine.md + WAVE 3 queue_status/next_topic hold Q2 and print that hold before scaffold copy-paste + README Human session / Local tools lead with the Q1 drop before doctor/idea_brief/new_packet -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone works in this sandbox when `gh` is authenticated. Do not retry the parked clone-failure path. Media stays gitignored. Push code with git, not media.
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- script.md 952 IN BAND; status `ready_for_vo`; selected take not in git
- Run 248 re-downloaded the existing Drive wav and seven cards, matched sha256, and left them in the operator session as `q1-handoff/` and `q1-handoff-verified.zip` (19908902 bytes). It did not regenerate or re-upload. Neither the wav nor the PNGs are on the packet paths. Session artifacts are not durable for the next agent.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.
- Executive trajectory decision: HOLD for on-disk Selected VO; SHIP the first completed video once that file exists. Do not expand architecture.

## What exists now (after Run 248)
- idea.md / draft.md / script.md / titles.md / thumbnail.md filled
- vo_session.md ready-to-record; named take missing from git
- vo_origin.md kind=generated (labeled fallback)
- captions.md stub with DROP; assets.md 7 planned cards; publish.md stub
- qa.md mechanical PASS; human VO box unchecked
- render.md all-missing plus DROP line
- packet.md status `ready_for_vo`
- Queue Q1 used; Q2-Q5 queued
- Packet listing has no committed `vo/` audio and no committed card PNGs
- Durable generated handoff: Drive file id `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` in folder `1ftaVyh8BWQeWp45TIyX7Hh1o0MPmGRev` (27200958 bytes, sha256 `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`). Copy target remains the packet-relative DROP path. Not anonymously downloadable (Run 246). No share-permission tool (Run 248).
- Durable cards: seven 1920x1080 PNGs in that folder. File ids and sha256 are in `HANDOFF.md`. `cards.sha256` file id `1Exe7TolCKO8f7-vZ6HCSseGEmrVLyU2x`. Copy target is packet `cards/`.
- Run 248 operator session also has those same bytes. That chat zip is a human copy source only.
- Completion gate PLAN_BUILT (`tools/complete.py` on main)
- Selftest DROP lock for experiment_loop.py / complete.py / youtube_upload.py is on HEAD
- media_qa level checks + export ftyp sniff on HEAD; youtube_upload ftyp on HEAD; upload fail-closed fixture on HEAD; fail-closed without a take
- Gate-machine drop recipe: `docs/gate_machine.md` (includes optional already-installed TTS one-liners, the Drive wav id, and the card copy)
- human_session + agent_session + hint/next_action + pipeline_status point that drop at gate_machine
- hint.py and next_action.py post-VO codes now match NEXT steps 3-4
- Clone-less first-fetch includes the drop page (7 bootstrap paths)
- WAVE 3 board printers name the Q2 hold *first*
- README Human session / Local tools name the Q1 drop *first*

## Pipeline map
On the machine that runs gates (`docs/gate_machine.md`), using the Run 248 zip or a signed-in Drive download:
1. Copy Drive file `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` onto the packet-relative DROP path and check sha256 against `HANDOFF.md`. DROP: `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav` (or .flac). A Drive file or a chat zip counts only after that copy. Do not use an unauthenticated curl; Run 246 showed it returns a Google sign-in page.
2. Copy the seven card ids in `HANDOFF.md` into `videos/002-stop-deciding-what-to-work-on-every-morning/cards/`. Drive PNGs are not packet cards until that copy.
3. narration_adapter.py then vo_session.py --force
4. card_generator.py --inspect-only (do not regenerate if all seven are yes; do not git add -f pngs)
5. timeline.py --write then media_qa.py (expect peak/RMS/silence/clip; export_decodable only if a master exists)
6. assemble.py without --execute until READY_TO_ENCODE
7. youtube_upload.py after a local master with a real ftyp box
8. youtube_feedback.py after a real provider_video_id
9. experiment_loop.py after real metrics
10. complete.py (expect INCOMPLETE_MEDIA until VO+cards exist; junk mp4 is still incomplete)
Do not invent a committed wav or mp4. Do not upload. Do not scaffold Q2.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 3.2 | 3.2 | release fetch verified; remaining human gate is YouTube OAuth |
| Automated steps | 96 | 96 | end-screen pad fixed; step count unchanged |
| Videos produced | 0 | 0 | local master exists; not uploaded |
| Days since last media progress | 0 | 0 | release re-verified; words extract fixed |

## Capability roadmap status
- Completion gate: PLAN_BUILT (complete.py + HEAD selftest lock)
- Experiment loop selftest lock: DONE on HEAD (Run 222)
- Media QA loudness/silence/clip: LANDED on HEAD (Run 223)
- Export ftyp sniff: LANDED on HEAD for media_qa/assemble/complete (Run 224) and youtube_upload (Run 225)
- Upload junk-master selftest: LANDED on HEAD (Run 226; still READY_FOR_MEDIA / READY_FOR_CREDENTIAL)
- Runs 227-238: freeze honor / drop-page / printer / reconstruct / WAVE 3 hold-before-scaffold / README first-block
- Run 239: treadmill flagged; HOLD until Selected VO; no capability change
- Run 240: HOLD re-verified against live packet listing; no capability change
- Run 241: 11-day gap HOLD heartbeat; packet still has no `vo/`; no capability change
- Run 242: sandbox generated-VO handoff measured against media_qa levels; not committed; not durable
- Run 243: same synthesis left in operator artifacts plus sha256 in `HANDOFF.md`; still not Selected VO
- Run 244: same bytes uploaded to Drive and verified by file id + size; still not Selected VO; no capability change
- Run 245: Drive wav re-downloaded and sha256 matched; seven cards uploaded and size-matched; still not Selected VO
- Run 246: same Drive bytes re-checked; anonymous fetch is a login wall; still not Selected VO; no capability change
- Run 247: same Drive bytes placed in the operator session zip; sha256 matched; still not Selected VO; no capability change
- Run 248: same Drive bytes re-checked and placed in this session zip; no share or release-upload tool; still not Selected VO; no capability change


## Run 249 delta
- Clone with GH_TOKEN works in this sandbox. Do not treat BLOCKED clone as always-failed.
- timeline.match_card no longer maps every Beat N to Beat 1.
- assemble --execute encodes one card at a time.
- Private release `q1-media-r249`: wav, seven PNGs, `q1-master.mp4` (sha256 `abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53`, 6499414 bytes, 308.40 s, 1920x1080, ftyp). Not a YouTube upload. Not committed media.
- Packet status stays `ready_for_vo` until the DROP file is on the checkout that will publish.
- Flag cleared for "another session zip". Do not re-download Drive unless the release asset is missing.


## Run 251 delta
- assemble no longer drops the end screen. Recipe and segmented mux use `apad=pad_dur=20` then `-shortest`. Bare `apad` hangs (filter never EOFs). Selftest locks `apad=pad_dur=`.
- Synthetic proof: VO 2.00s + 4s end card. Old mux duration 2.00s. Padded mux duration 6.00s (silent video 6.02s).
- `q1-media-r249` master sha256 `abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53` is the truncated 308.40s encode. Do not upload it as the finished export. Re-encode with assemble --execute after this commit. Do not regenerate the wav or cards.
- Packet status stays `ready_for_vo`. YouTube OAuth still absent. Did not re-download the release.

## Run 250 delta
- `gh release download q1-media-r249` matched wav sha256 `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2` and master sha256 `abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53`.
- On that checkout, narration_adapter, card inspect, and media_qa PASS. complete.py is INCOMPLETE_PUBLISH (no provider_video_id). youtube_upload.py is YOUTUBE_AUTH_REQUIRED. Status was not bumped.
- extract_words ignored multiline WORDS bodies, so the adapter printed words: 0. Regex now uses DOTALL and stops at VISUAL or the next heading. Live packet extracts 941 words. selftest PASS.
- assemble dry-run still prints the single-graph argv but now labels it do_not_copy_on_2gb. Execute remains segmented.
- Do not re-download the release unless an asset is missing. Do not regenerate. Next human gate is YouTube OAuth, not another zip.

## Active constraints
- Do not add another dry-run adapter before on-disk Selected VO
- Do not invent a committed wav or bump status past ready_for_vo without Selected VO on disk
- Do not treat complete.py INCOMPLETE_* as license to invent media or a keep/discard
- Do not write a dummy export/master.mp4 to flip gates
- Do not add another selftest fixture unless a live printer regression is proven on HEAD
- Do not treat docs/gate_machine.md or the Drive file id as permission to commit sandbox audio or PNGs
- Do not wrap the optional TTS one-liners into tools/
- Do not restore "recording is the only gate" or blanket "no ffmpeg recipe" language on operator pages or hint.py edit commands
- Do not strip the docs/gate_machine.md pointer from hint.py / next_action.py / pipeline_status.py
- Do not revert hint.py or next_action.py build-cards/edit to stock-download or editor-only wording
- Do not strip docs/gate_machine.md from needed.py BOOTSTRAP or doctor UNMAPPED_PATHS
- Do not strip the Q1 gate_machine hold from queue_status.py or next_topic.py
- Do not move scaffold copy-paste above the Q1 hold in queue_status.py, next_topic.py, or the doctor footer
- Do not move README Human session / Local tools doctor, idea_brief, new_packet, or sample-001 commands above the live Q1 drop
- Do not commit another documentation-order or printer-alignment change unless a proven HEAD regression sends operators to scaffold Q2 or invent media
- Do not commit another hold-verification run in the same week if RUNS.md already records a current HOLD and VO is still missing
- Do not regenerate the generated wav while Drive file `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` lists 27200958 bytes and sha256 `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2` is current
- Do not regenerate the seven cards while the Drive ids in `HANDOFF.md` list the recorded byte sizes
- Do not describe the Drive handoff or the Run 248 session zip as a human recording or as gate-machine Selected VO
- Do not add a public curl/gdown fetcher. Run 246 showed the wav file id is not anonymously downloadable. Run 248 found no share-permission tool.
- Flag: runs 239-248 have not placed a file at the packet-relative DROP path. Another Drive upload or another session zip is not that copy. Next agent should not re-download unless the operator says the Run 248 zip was lost.
