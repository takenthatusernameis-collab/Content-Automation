# STATE

Updated: 2026-09-13T07:10:00Z (Run 113)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + **Q1 script.md applied from in-band draft** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- idea_brief reprints only; never writes idea.md
- PATH/draft.md is not script.md until apply --write (Q1 now applied)
- Run 111: scaffolded Q1, pasted idea.md, marked Q1 used
- Run 112: filled Q1 draft.md spoken WORDS (manual 941)
- Run 113: official-equivalent words.py count on Q1 draft = **952 IN BAND** (~06:21 at 150 wpm). Hook 28 (ok). Beats Hook 28 | Payoff 57 | Beat 1 195 | Beat 2 199 | Beat 3 221 | Beat 4 201 | CTA 51. Applied draft beats onto script.md. Did **not** run set_status (gate tools not executed). Did **not** invent VO. Did **not** map forbidden tools. Did **not** add a CLI. Did **not** scaffold Q2.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.

## What exists now (after Run 113)
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- idea.md mechanism filled
- draft.md spoken WORDS
- script.md now has the same spoken WORDS (applied)
- packet.md status still `draft` (ready_for_vo not written without set_status)
- Queue Q1 used; Q2-Q5 queued
- Reconstruct-loop watch from Runs 099-103 remains in force

## Pipeline map
Q1 is past paste + draft overwrite + words count + script apply.
Next live command: `python3 tools/validate_packet.py PATH` then `python3 tools/set_status.py PATH --to ready_for_vo` dry-run, `--write` only if OK and no duration WARN.
Then `title_thumb_brief.py --dry-run` to fill titles.md / thumbnail.md. Do not invent VO. Do not upload.

After a high-risk GitHub write: `python3 tools/prove_locks.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 52 | 46 | script applied; titles/VO still human |
| Automated steps | 84 | 84 | no new CLI |
| Videos produced | 0 | 0 | Q1 script.md applied; no VO |

## Active constraints
- Do not auto-scaffold another packet while Q1 has no VO
- Do not map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / needed.py / idea_brief.py / idea_brief_contract.py / doctor.py
- Do not make idea-lock INFO a BLOCKED error or --strict FAIL
- Do not treat draft.md as script.md (Q1 script.md is now the applied copy)
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
- Do not bump status to ready_for_vo without set_status evidence
