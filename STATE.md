# STATE

Updated: 2026-09-19T01:15:00Z (Run 214)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + narration adapter + labeled generated fallback + local card generator (Pillow, gitignored PNGs) -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- script.md 952 IN BAND; status `ready_for_vo`; selected take not in git
- Run 214: added `tools/card_generator.py`. Parses assets.md, writes 1920x1080 text/diagram PNGs under packet `cards/`, optional `card_manifest.md`, optional `--mark-ready`. Binaries stay gitignored. No status bump. No Q2. No wav force-add.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.
- Executive trajectory decision: SHIP the first completed video before adding further broad architecture.

## What exists now (after Run 214)
- idea.md / draft.md / script.md / titles.md / thumbnail.md filled
- vo_session.md ready-to-record; named take missing from git
- vo_origin.md kind=generated (labeled fallback)
- captions.md stub with DROP; assets.md 7 planned cards; publish.md stub
- qa.md mechanical PASS; human VO box unchecked
- render.md all-missing plus DROP line
- packet.md status `ready_for_vo`
- Queue Q1 used; Q2-Q5 queued
- Packet listing has no committed `vo/` audio and no committed card PNGs
- Card generator READY_FOR_MEDIA (needs Pillow + a writable packet folder)

## Pipeline map
On the machine that runs gates:
1. Place Selected VO at `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`
2. `python3 tools/narration_adapter.py PATH` then `python3 tools/vo_session.py PATH --force`
3. `python3 tools/card_generator.py PATH --write-manifest` (do not `git add -f` pngs)
Do not invent a committed wav. Do not upload. Do not scaffold Q2.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 10 | 8 | card generator removes manual title-card build |
| Automated steps | 86 | 87 | card_generator.py |
| Videos produced | 0 | 0 | ready_for_vo; take not on gate machine |

## Capability roadmap status
- Content/editorial gates: BUILT
- Narration adapter: READY_FOR_MEDIA
- Visual/card generator: READY_FOR_MEDIA (Run 214; Pillow; local pngs)
- Render/assembly: NOT_BUILT
- Media QA: NOT_BUILT
- Credential-ready YouTube uploader: READY_FOR_CREDENTIAL (contract only; implementation NOT_BUILT)
- YouTube Analytics/comment feedback ingestion: NOT_BUILT
- Experiment/improvement loop: contract BUILT; execution tooling NOT_BUILT

## Active constraints
- Do not auto-scaffold another packet while Q1 has no on-disk VO
- Do not map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / needed.py / idea_brief.py / idea_brief_contract.py / doctor.py
- Do not invent a committed wav or bump status past ready_for_vo without Selected VO on disk
- Do not treat repo-root `vo/` as Selected VO
- Do not describe generated VO as a human recording
- Do not commit card PNGs to flip assets.md rows
- Do not add another wrapper CLI, WAVE 4, or Live job banner unless a first-contact lie is proven
- Do not re-split selected_vo_drop into a second string builder
