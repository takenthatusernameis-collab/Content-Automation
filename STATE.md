# STATE

Updated: 2026-09-14T02:04:00Z (Run 132)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + printers/gates/render.md/vo_session.md DROP agree via render_brief.selected_vo_drop -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- script.md 952 IN BAND; status `ready_for_vo`; selected take missing
- Run 132: `tools/vo_session.py` imports `selected_vo_drop()`. Generated vo_session.md header prints DROP with the repo-root path. Record-to line uses the same helper. Live Q1 reading card header updated. No new CLI. No wav invented. No status bump. No Q2.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.

## What exists now (after Run 132)
- idea.md / draft.md / script.md / titles.md / thumbnail.md filled
- vo_session.md ready-to-record; named take missing; header DROP matches board/gate
- captions.md stub; assets.md 7 planned cards; publish.md stub
- qa.md mechanical PASS; render.md all-missing plus DROP line
- packet.md status `ready_for_vo`
- Human still must record selected VO and build cards locally
- Queue Q1 used; Q2-Q5 queued

## Pipeline map
Next live command: record selected VO at `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`. Do not invent a wav. Do not drop it at repo-root `vo/`. Do not `git add -f` it. Do not upload. Do not scaffold Q2.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 17 | 16 | reading card now names the same DROP path as the board/gate |
| Automated steps | 84 | 84 | no new CLI; shared helper only |
| Videos produced | 0 | 0 | ready_for_vo; no selected take |

## Active constraints
- Do not auto-scaffold another packet while Q1 has no VO
- Do not map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / needed.py / idea_brief.py / idea_brief_contract.py / doctor.py
- Do not invent a wav or bump status past ready_for_vo without Selected VO on disk
- Do not treat repo-root `vo/` as Selected VO
- Do not add another wrapper CLI, WAVE 4, or Live job banner unless a first-contact lie is proven
- Do not re-split selected_vo_drop into a second string builder
