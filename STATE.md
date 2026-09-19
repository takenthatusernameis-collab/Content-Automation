# STATE

Updated: 2026-09-19T13:05:00Z (Run 225)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + narration adapter + labeled generated fallback + local card generator + WORDS timeline planner + fail-closed media QA (header + PCM peak/RMS/silence/clip + export ftyp when present) + credential-ready dry-run uploader (ftyp-required master) + fail-closed ffmpeg assemble planner + fail-closed feedback collector + fail-closed experiment ledger + fail-closed completion gate + HEAD selftest lock for experiment/complete/level-checks/export-ftyp -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- script.md 952 IN BAND; status `ready_for_vo`; selected take not in git
- Run 225: `tools/youtube_upload.py` now requires `mp4_header_ok` before master_export_present. A junk `export/master.mp4` stays HOLD_LOCAL. media_qa / assemble / complete already shared that helper (Run 224). No new adapter. No invented wav or mp4.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.
- Executive trajectory decision: SHIP the first completed video before adding further broad architecture.

## What exists now (after Run 225)
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
- Selftest DROP lock for experiment_loop.py / complete.py is on HEAD
- media_qa level checks + export ftyp sniff on HEAD; youtube_upload ftyp on HEAD; fail-closed without a take

## Pipeline map
On the machine that runs gates:
1. Place Selected VO at the packet-relative DROP path
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
| Estimated human min / video | 5.0 | 4.9 | junk masters cannot look upload-ready |
| Automated steps | 94 | 94 | quality of existing youtube_upload, not a 95th adapter |
| Videos produced | 0 | 0 | ready_for_vo; take not on gate machine |

## Capability roadmap status
- Completion gate: PLAN_BUILT (complete.py + HEAD selftest lock)
- Experiment loop selftest lock: DONE on HEAD (Run 222)
- Media QA loudness/silence/clip: LANDED on HEAD (Run 223)
- Export ftyp sniff: LANDED on HEAD for media_qa/assemble/complete (Run 224) and youtube_upload (Run 225; still READY_FOR_MEDIA / READY_FOR_CREDENTIAL)

## Active constraints
- Do not add another dry-run adapter before on-disk Selected VO
- Do not invent a committed wav or bump status past ready_for_vo without Selected VO on disk
- Do not treat complete.py INCOMPLETE_* as license to invent media or a keep/discard
- Do not write a dummy export/master.mp4 to flip gates
