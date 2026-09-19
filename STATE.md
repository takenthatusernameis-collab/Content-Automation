# STATE

Updated: 2026-09-19T22:20:00Z (Run 229)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + narration adapter + labeled generated fallback + local card generator + WORDS timeline planner + fail-closed media QA (header + PCM peak/RMS/silence/clip + export ftyp when present) + credential-ready dry-run uploader (ftyp-required master + selftest lock) + fail-closed ffmpeg assemble planner + fail-closed feedback collector + fail-closed experiment ledger + fail-closed completion gate + HEAD selftest lock for experiment/complete/level-checks/export-ftyp/upload-junk-master + gate-machine drop recipe with optional local TTS one-liners -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- script.md 952 IN BAND; status `ready_for_vo`; selected take not in git
- Run 229: added optional local TTS copy-paste (espeak-ng/ffmpeg, macOS say/ffmpeg, or cp) to `docs/gate_machine.md`. No new adapter. No invented wav/mp4. Production freeze otherwise honored.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.
- Executive trajectory decision: SHIP the first completed video before adding further broad architecture.

## What exists now (after Run 229)
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
| Estimated human min / video | 4.7 | 4.6 | operator no longer has to invent a TTS command |
| Automated steps | 94 | 94 | freeze: still no 95th adapter |
| Videos produced | 0 | 0 | ready_for_vo; take not on gate machine |

## Capability roadmap status
- Completion gate: PLAN_BUILT (complete.py + HEAD selftest lock)
- Experiment loop selftest lock: DONE on HEAD (Run 222)
- Media QA loudness/silence/clip: LANDED on HEAD (Run 223)
- Export ftyp sniff: LANDED on HEAD for media_qa/assemble/complete (Run 224) and youtube_upload (Run 225)
- Upload junk-master selftest: LANDED on HEAD (Run 226; still READY_FOR_MEDIA / READY_FOR_CREDENTIAL)
- Run 227: freeze honor; no capability change
- Run 228: operator drop recipe page; no capability change
- Run 229: optional local TTS one-liners on existing drop page; no new printer

## Active constraints
- Do not add another dry-run adapter before on-disk Selected VO
- Do not invent a committed wav or bump status past ready_for_vo without Selected VO on disk
- Do not treat complete.py INCOMPLETE_* as license to invent media or a keep/discard
- Do not write a dummy export/master.mp4 to flip gates
- Do not add another selftest fixture unless a live printer regression is proven on HEAD
- Do not treat docs/gate_machine.md as permission to commit sandbox audio
- Do not wrap the optional TTS one-liners into tools/
