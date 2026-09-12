# STATE

Updated: 2026-09-12T11:12:00Z (Run 092)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + write-path + words.py band + apply idea-lock INFO + idea_lock.py printer** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- idea_brief reprints only; never writes idea.md
- PATH/draft.md is not script.md until apply --write
- Run 091: apply_script.py dry-run prints idea-lock INFO. INFO never blocks --write.
- Run 092: tools/idea_lock.py prints the same INFO against draft.md/script.md. Exit 0. Unmapped. words.py does **not** yet import idea_lock_notes (fold that next if no Q1 packet exists).
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.

## What exists now (after Run 092)
- tools/idea_lock.py committed
- apply_script.py still owns idea_lock_notes()
- words.py unchanged this run (still band / Grow / Cut only)
- No new packet folder; queue still queued

## Pipeline map
After scaffold: idea_brief --block / paste / --check / expand_prompt / save draft.md / `words.py PATH` / `idea_lock.py PATH` / apply dry-run / `--write --refresh` / set_status ready_for_vo if WORDS in band.
After a high-risk GitHub write: `python3 tools/prove_locks.py`.
Start of session: `python3 tools/queue_status.py` then `python3 tools/next_topic.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 83 | 82 | idea_lock.py shows mechanism miss before apply |
| Automated steps | 72 | 73 | new read-only printer wrapping idea_lock_notes |
| Videos produced | 0 | 0 | fixture only |

## Active constraints
- Do not auto-scaffold Q1
- Do not map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / needed.py
- Do not make idea-lock INFO a BLOCKED error or --strict FAIL
- Do not treat draft.md as script.md
- Do not write idea.md from idea_brief
- Do not retry HTTPS clone as the first action
- Do not spend a run aligning another page to name idea_brief
- Next code fold if Q1 is still absent: words.py imports idea_lock_notes so the extra CLI is not required
