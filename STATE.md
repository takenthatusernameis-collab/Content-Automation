# STATE

Updated: 2026-09-19T00:10:00Z (Run 213)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + narration adapter (WORDS extract / wav inspect / vo_origin sidecar) + labeled generated fallback authorized after 24h deadline -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- script.md 952 IN BAND; status `ready_for_vo`; selected take not in git
- Run 213: 24-hour VO request elapsed at 2026-09-19T00:00:00Z. Added `tools/narration_adapter.py`. Wrote Q1 `vo_origin.md` with `kind: generated`. Synthesized a workspace-only MP3 of Q1 WORDS (~5.1MB); not committed. No status bump. No Q2. No wav force-add.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.
- Executive trajectory decision: SHIP the first completed video before adding further broad architecture.

## What exists now (after Run 213)
- idea.md / draft.md / script.md / titles.md / thumbnail.md filled
- vo_session.md ready-to-record; named take missing from git
- vo_origin.md kind=generated (labeled fallback)
- captions.md stub with DROP; assets.md 7 planned cards; publish.md stub
- qa.md mechanical PASS; human VO box unchecked
- render.md all-missing plus DROP line
- packet.md status `ready_for_vo`
- Queue Q1 used; Q2-Q5 queued
- Packet listing has no committed `vo/` audio

## Pipeline map
Next live command: place a packet-relative take (human or generated) at `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav` on the machine that runs gates. Then `python3 tools/narration_adapter.py PATH` and `python3 tools/vo_session.py PATH --force`. Do not invent a committed wav. Do not `git add -f`. Do not upload. Do not scaffold Q2.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 11 | 10 | generated fallback authorized; human VO optional |
| Automated steps | 85 | 86 | narration_adapter.py |
| Videos produced | 0 | 0 | ready_for_vo; take not on gate machine |

## Capability roadmap status
- Content/editorial gates: BUILT
- Narration adapter: READY_FOR_MEDIA (extract/inspect/origin BUILT; take must exist locally)
- Visual/card generator: NOT_BUILT
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
- Do not add another wrapper CLI, WAVE 4, or Live job banner unless a first-contact lie is proven
- Do not re-split selected_vo_drop into a second string builder
