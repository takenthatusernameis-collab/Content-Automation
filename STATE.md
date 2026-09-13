# STATE

Updated: 2026-09-13T21:18:00Z (Run 127)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 script.md applied + titles/thumb filled + vo_session ready-to-record + captions stub + assets list + publish stub (tags trimmed) + qa mechanical + render presence all-missing + operator after-VO / after-edit / after-presence commands + Selected VO path locked packet-relative + local media gitignored + BLOCKED VO path matches gates + README front door names live packet + agent_session live-job pin + human_session live-job pin + production_rules Human handoff live-job pin -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- idea_brief reprints only; never writes idea.md
- PATH/draft.md is not script.md until apply --write (Q1 already applied)
- Run 111: scaffolded Q1, pasted idea.md, marked Q1 used
- Run 112: filled Q1 draft.md spoken WORDS (manual 941)
- Run 113: official-equivalent words count 952 IN BAND; applied onto script.md; status stayed draft
- Run 114: titles.md + thumbnail.md filled; validate PASS; status ready_for_vo
- Run 115: filled vo_session.md (ready-to-record, 952w / ~06:21) and captions.md stub (7 cues). Locked heuristic Primary. Did not invent VO.
- Run 116: filled assets.md (7 planned cards from VISUAL) and publish.md stub (title/description/tags/pin). Status stayed ready_for_vo.
- Run 117: trimmed publish.md tags. Filled qa.md mechanical boxes PASS and render.md presence all-missing. Status stayed ready_for_vo.
- Run 118: documented after-VO operator path on human_session step 5 and narration.md. No wav invented. No status bump. No Q2. No new CLI.
- Run 119: documented after-edit card path on human_session step 6. No png invented.
- Run 120: documented after-presence publish edit on human_session step 7. Did not upload.
- Run 121: locked Selected VO to packet-relative `videos/NNN-slug/vo/...`. Repo-root `vo/` is not Selected VO. No wav invented. No status bump. No Q2. No new CLI. Did not map forbidden tools.
- Run 122: added `.gitignore` for packet vo audio, cards images, exports video, and repo-root dumps. Presence tools still check local disk. No wav invented. No status bump. No Q2. No new CLI.
- Run 123: BLOCKED.md TTS/mic row now names the packet-relative Selected VO path. Repo-root `vo/` is not a setup instruction. No wav invented. No status bump. No Q2. No new CLI.
- Run 124: README opens on the live Q1 packet and the exact Selected VO path. sample-001 commands stay contract examples, not the start job. No wav invented. No status bump. No Q2. No new CLI.
- Run 125: docs/agent_session.md now opens on the live Q1 job before reconstruct waves. WAVE 3 board printers are confirmation only while ready_for_vo has no take. No wav invented. No status bump. No Q2. No new CLI.
- Run 126: docs/human_session.md now opens on the live Q1 recording gate. doctor / queue_status / new_packet are labeled new-packet only. Steps 1-4 kept as completed path. No new step. No wav invented. No status bump. No Q2. No new CLI.
- Run 127: docs/production_rules.md Human handoff no longer says start with doctor / queue_status / next_topic. Live job is the Q1 packet-relative take. No new Live job page. No wav invented. No status bump. No Q2. No new CLI.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.

## What exists now (after Run 127)
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- idea.md mechanism filled
- draft.md + script.md spoken WORDS (952 IN BAND, hook 28)
- titles.md Primary locked as heuristic; thumbnail on-image `One Written Default`
- vo_session.md reading card ready-to-record; named take missing
- captions.md stub from WORDS (not SRT)
- assets.md stub: 7 planned cards; no image files in git
- publish.md stub: tags trimmed; description + pin still human; not uploaded
- qa.md: mechanical PASS; all human boxes open
- render.md: all-missing (0 present / 11 missing)
- packet.md status `ready_for_vo`
- `.gitignore` excludes local Selected VO / cards / exports binaries
- BLOCKED.md no longer advertises repo-root `vo/` as the record path
- README front door no longer leads with fixture scaffold as the live job
- agent_session no longer leads with reconstruct waves as the live job
- human_session no longer leads with doctor/scaffold as the live job
- production_rules Human handoff no longer leads with doctor/queue as the live job
- Human still must record selected VO and build cards locally
- Queue Q1 used; Q2-Q5 queued
- Reconstruct-loop watch from Runs 099-103 remains in force

## Pipeline map
Q1 is past paste + draft + words count + script apply + title/thumb + ready_for_vo + reading card + asset list + publish stub + tag trim + qa mechanical + render presence + after-VO / after-edit / after-presence operator commands + Selected VO path lock + media gitignore + BLOCKED path lock + README live-packet pin + agent_session live-job pin + human_session live-job pin + production_rules Human handoff live-job pin.
Next live command: record/generate selected VO per `docs/narration.md` and `vo_session.md`. Place at `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`. Do not invent a wav. Do not drop it at repo-root `vo/`. Do not `git add -f` it. Do not upload. Do not scaffold Q2.

After a high-risk GitHub write: `python3 tools/prove_locks.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 22 | 21 | rules page no longer presents doctor as the live job |
| Automated steps | 84 | 84 | no new CLI |
| Videos produced | 0 | 0 | ready_for_vo; no selected take |

## Active constraints
- Do not auto-scaffold another packet while Q1 has no VO
- Do not map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / needed.py / idea_brief.py / idea_brief_contract.py / doctor.py
- Do not make idea-lock INFO a BLOCKED error or --strict FAIL
- Do not treat draft.md as script.md
- Do not write idea.md from idea_brief
- Do not retry HTTPS clone as the first action
- Do not add another wrapper CLI
- Do not add WAVE 4
- Reconstruct-loop watch: do not add another reconstruct path unless a READY lie is proven
- Do not rewrite writer prompts unless a later words.py miss
- Do not add a Band-landing reprint CLI
- Do not strip Target column / hint Target comment
- Do not apply_script --write against sample-001
- Do not invent a wav or ffmpeg recipe
- Do not bump status past ready_for_vo without Selected VO on disk
- Do not treat repo-root `vo/` as Selected VO
- Do not commit card binaries or treat planned rows as ready
- Do not `git add -f` ignored media
- Do not treat a publish.md edit as an upload
- Do not add another operator step that only restates NEXT.md
- Do not add another Live job banner unless a first-contact lie is proven
