# STATE

Updated: 2026-09-13T08:15:00Z (Run 114)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 script.md applied + **titles/thumbnail brief filled + status ready_for_vo** -> automated -> self-improving

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
- Run 114: validate_packet on empty titles/thumb = FAIL (0 titles, missing on-image text). Generated heuristic titles.md + thumbnail.md via title_thumb_brief rules. Re-validate PASS (including --duration). set_status-equivalent check OK (gate empty, no duration WARN). Wrote packet.md status `ready_for_vo`. Did **not** invent VO. Did **not** map forbidden tools. Did **not** add a CLI. Did **not** scaffold Q2.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.

## What exists now (after Run 114)
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- idea.md mechanism filled
- draft.md + script.md spoken WORDS (952 IN BAND, hook 28)
- titles.md Primary + 5 alts; thumbnail on-image `One Written Default` (3 words)
- packet.md status `ready_for_vo`
- Human still must pick/lock Primary and record VO
- Queue Q1 used; Q2-Q5 queued
- Reconstruct-loop watch from Runs 099-103 remains in force

## Pipeline map
Q1 is past paste + draft + words count + script apply + title/thumb brief + status ready_for_vo.
Next live command: human locks Primary (or keep heuristic). Then record/generate selected VO per `docs/narration.md`. Do not invent a wav. Do not upload. Do not scaffold Q2.

After a high-risk GitHub write: `python3 tools/prove_locks.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 46 | 40 | titles/thumb heuristic; VO still human |
| Automated steps | 84 | 84 | no new CLI; existing brief used |
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
