# STATE

Updated: 2026-09-13T06:30:00Z (Run 112)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + first non-fixture draft.md with WORDS in band (not yet applied to script.md)** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- idea_brief reprints only; never writes idea.md
- PATH/draft.md is not script.md until apply --write
- Run 111 (other agent): scaffolded `videos/002-stop-deciding-what-to-work-on-every-morning`, pasted idea.md, marked Q1 used. Packet was incomplete vs template.
- Run 112: filled Q1 `draft.md` spoken WORDS (manual count hook 27 / payoff 55 / beats 192+197+220+200 / CTA 50 / total 941, inside 900-1500). Copied missing template packet files. Did **not** run apply --write. Did **not** overwrite script.md. Did **not** invent VO. Did **not** map forbidden tools. Did **not** add a CLI.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.

## What exists now (after Run 112)
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- idea.md mechanism filled (written next-action default)
- draft.md has first WORDS (claimed 941; words.py is official and unrun this sandbox)
- script.md still empty template headings
- Packet now has expand/research/titles/thumbnail/assets/captions/qa/publish/render/vo_session placeholders
- Queue Q1 is used; Q2-Q5 queued
- Reconstruct-loop watch from Runs 099-103 remains in force

## Pipeline map
Before scaffold: `python3 tools/doctor.py` then `python3 tools/queue_status.py` then `python3 tools/next_topic.py`.
After scaffold: idea_brief --block / paste / --check / expand_prompt / overwrite PATH/draft.md / `words.py PATH` / apply dry-run / `--write --refresh` / set_status ready_for_vo if WORDS in band.
Q1 is past paste + draft overwrite. Next live command is words.py on PATH, then apply dry-run, then `--write --refresh` only if IN BAND.
After a high-risk GitHub write: `python3 tools/prove_locks.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 64 | 52 | first non-fixture draft exists; apply + VO still human |
| Automated steps | 84 | 84 | no new CLI |
| Videos produced | 0 | 0 | Q1 draft only; script.md not applied |

## Active constraints
- Do not auto-scaffold another packet while Q1 draft is unapplied
- Do not map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / needed.py / idea_brief.py / idea_brief_contract.py / doctor.py
- Do not make idea-lock INFO a BLOCKED error or --strict FAIL
- Do not treat draft.md as script.md
- Do not write idea.md from idea_brief
- Do not retry HTTPS clone as the first action
- Do not add another wrapper CLI around idea_lock_notes
- Do not add WAVE 4
- Reconstruct-loop watch: do not add another reconstruct path unless a READY lie is proven
- Do not rewrite writer prompts unless this draft misses band under words.py
- Do not add a Band-landing reprint CLI
- Do not hide the empty-WORDS expand budget table
- Do not make expand_prompt write expand.md
- Do not strip the Target column from docs/human_session.md step 3
- Do not strip the Target comment from hint.py write-script/expand-script commands
- Do not apply_script --write against sample-001
- Do not invent a wav or ffmpeg recipe
