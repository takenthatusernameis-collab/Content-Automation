# STATE

Updated: 2026-09-19T08:03:00Z (Run 220)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + narration adapter + labeled generated fallback + local card generator + WORDS timeline planner + fail-closed media QA + credential-ready dry-run uploader + fail-closed ffmpeg assemble planner + fail-closed feedback collector + fail-closed experiment ledger -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- script.md 952 IN BAND; status `ready_for_vo`; selected take not in git
- Run 220: added `tools/experiment_loop.py`. Reuses youtube_feedback.inspect_feedback. Missing video ID is HOLD_UNPUBLISHED. Empty metrics are HOLD_NO_EVIDENCE. Never invents keep/discard. Never calls Analytics.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.
- Executive trajectory decision: SHIP the first completed video before adding further broad architecture.

## What exists now (after Run 220)
- idea.md / draft.md / script.md / titles.md / thumbnail.md filled
- vo_session.md ready-to-record; named take missing from git
- vo_origin.md kind=generated (labeled fallback)
- captions.md stub with DROP; assets.md 7 planned cards; publish.md stub
- qa.md mechanical PASS; human VO box unchecked
- render.md all-missing plus DROP line
- packet.md status `ready_for_vo`
- Queue Q1 used; Q2-Q5 queued
- Packet listing has no committed `vo/` audio and no committed card PNGs
- Card generator READY_FOR_MEDIA; timeline planner READY_FOR_MEDIA; media QA READY_FOR_MEDIA
- YouTube uploader READY_FOR_CREDENTIAL and READY_FOR_MEDIA (dry-run; no master export; no OAuth)
- Assembler PLAN_BUILT / READY_FOR_MEDIA (recipe exists; encode still gated)
- Feedback collector READY_FOR_CREDENTIAL (dry-run; HOLD_UNPUBLISHED until a provider video ID exists)
- Experiment ledger PLAN_BUILT (dry-run; HOLD_UNPUBLISHED / HOLD_NO_EVIDENCE until a published video has real metrics)

## Pipeline map
On the machine that runs gates:
1. Place Selected VO at `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`
2. `python3 tools/narration_adapter.py PATH` then `python3 tools/vo_session.py PATH --force`
3. `python3 tools/card_generator.py PATH --write-manifest` (do not `git add -f` pngs)
4. `python3 tools/timeline.py PATH --write` then `python3 tools/media_qa.py PATH`
5. Inspect ready_to_assemble; `python3 tools/assemble.py PATH` (expect HOLD_MEDIA until VO+cards exist). Do not `--execute` until gate READY_TO_ENCODE.
6. After a local master exists: `python3 tools/youtube_upload.py PATH` (expect `YOUTUBE_AUTH_REQUIRED` until OAuth env is set)
7. After a real provider_video_id exists in upload_state.json: `python3 tools/youtube_feedback.py PATH` (expect HOLD_UNPUBLISHED until then; never treat empty metrics as collected feedback)
8. After feedback exists: `python3 tools/experiment_loop.py PATH` (expect HOLD_NO_EVIDENCE until metrics are real; never treat pending as keep/discard)
Do not invent a committed wav. Do not upload. Do not scaffold Q2.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 5.4 | 5.3 | experiment recipe replaces ad-hoc hypothesis notes |
| Automated steps | 92 | 93 | experiment_loop.py |
| Videos produced | 0 | 0 | ready_for_vo; take not on gate machine |

## Capability roadmap status
- Content/editorial gates: BUILT
- Narration adapter: READY_FOR_MEDIA
- Visual/card generator: READY_FOR_MEDIA
- Render/assembly: PLAN_BUILT / READY_FOR_MEDIA (timeline + assemble recipe; encode gated)
- Media QA: READY_FOR_MEDIA (fail-closed; WAV/PNG checks; no ffmpeg)
- Credential-ready YouTube uploader: READY_FOR_CREDENTIAL (dry-run adapter BUILT; live videos.insert NOT_BUILT)
- YouTube Analytics/comment feedback ingestion: READY_FOR_CREDENTIAL (dry-run adapter BUILT; live fetch NOT_BUILT)
- Experiment/improvement loop: PLAN_BUILT (dry-run ledger BUILT; compare-with-baseline still blocked on published evidence)

## Active constraints
- Do not auto-scaffold another packet while Q1 has no on-disk VO
- Do not map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / needed.py / idea_brief.py / idea_brief_contract.py / doctor.py
- Do not invent a committed wav or bump status past ready_for_vo without Selected VO on disk
- Do not treat repo-root `vo/` as Selected VO
- Do not describe generated VO as a human recording
- Do not commit card PNGs to flip assets.md rows
- Do not add another wrapper CLI, WAVE 4, or Live job banner unless a first-contact lie is proven
- Do not re-split selected_vo_drop into a second string builder
- Do not run ffmpeg / assemble --execute before timeline ready_to_assemble=yes and media_qa gate PASS
- Do not call YouTube APIs or print OAuth values
- Do not invent analytics, comments, or experiment results
