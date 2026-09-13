# STATE

Updated: 2026-09-13T12:25:00Z (Run 118)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 script.md applied + titles/thumb filled + vo_session ready-to-record + captions stub + assets list + publish stub (tags trimmed) + qa mechanical + render presence all-missing + operator after-VO commands on human_session + status ready_for_vo -> automated -> self-improving

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
- Run 118: documented after-VO operator path on human_session step 5 and narration.md. No wav invented. No status bump. No Q2. No new CLI. Did not map forbidden tools.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.

## What exists now (after Run 118)
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- idea.md mechanism filled
- draft.md + script.md spoken WORDS (952 IN BAND, hook 28)
- titles.md Primary locked as heuristic; thumbnail on-image `One Written Default`
- vo_session.md reading card ready-to-record; named take missing
- captions.md stub from WORDS (not SRT)
- assets.md stub: 7 planned cards; no image files in git
- publish.md stub: tags trimmed; not uploaded
- qa.md: mechanical PASS; all human boxes open
- render.md: all-missing (0 present / 11 missing)
- packet.md status `ready_for_vo`
- Operator page now names the take path and the vo_session --force / set_status ready_for_edit dry-run
- Human still must record selected VO and build cards locally
- Queue Q1 used; Q2-Q5 queued
- Reconstruct-loop watch from Runs 099-103 remains in force

## Pipeline map
Q1 is past paste + draft + words count + script apply + title/thumb + ready_for_vo + reading card + asset list + publish stub + tag trim + qa mechanical + render presence + after-VO operator commands.
Next live command: record/generate selected VO per `docs/narration.md` and `vo_session.md`. Place at `vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`. Do not invent a wav. Do not upload. Do not scaffold Q2.

After a high-risk GitHub write: `python3 tools/prove_locks.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 30 | 29 | after-VO commands no longer hunted across NEXT/narration/packet |
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
- Do not make expand_prompt write expand.md
- Do not strip Target column / hint Target comment
- Do not apply_script --write against sample-001
- Do not invent a wav or ffmpeg recipe
- Do not bump status past ready_for_vo without Selected VO on disk
- Do not commit card binaries or treat planned rows as ready
