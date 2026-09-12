# STATE

Updated: 2026-09-12T11:05:00Z (Run 092)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + words.py band + idea-lock INFO on words and apply** -> automated -> self-improving

See ROADMAP.md and RUNS.md for the full lock list. Run 092 added words.py print_idea_lock_notes() importing apply_script.idea_lock_notes(). INFO never changes --strict and is not apply --write.

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured
- HTTPS clone from this agent sandbox still fails (private repo). Push via GitHub file API.
- idea_brief reprints only; never writes idea.md
- Off-repo expand draft convention: PATH/draft.md is not script.md until apply --write
- words.py is a read-only band printer. Do not map it in needed.py.
- words_contract.py / placeholder_guard.py / prove_locks.py stay unmapped.

## What exists now (after Run 092)
- words.py prints idea-lock INFO after Next / Grow / Cut
- apply_script.py still owns idea_lock_notes(); words.py imports it
- Isolated check: words.py contains idea_lock_notes and does not block --write
- No new packet folder; queue still queued

## Pipeline map
After scaffold: idea_brief --block / paste / --check / expand_prompt (Idea locks) / save draft.md / `words.py PATH` (band + idea-lock INFO) / apply dry-run (same INFO) / `--write --refresh` / set_status ready_for_vo if WORDS in band.
After a GitHub write of any high-risk tool: `python3 tools/prove_locks.py`.
Start of session: `python3 tools/queue_status.py` then `python3 tools/next_topic.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 83 | 82 | words.py flags a draft that ignores the pasted mechanism before apply |
| Automated steps | 72 | 73 | words.py gained the same read-only lock-overlap printer as apply |
| Videos produced | 0 | 0 | fixture only |
| Write-path contract | body + trio + ordered verify 070 | unchanged 092 | run prove_locks.py after a high-risk GitHub write |

## Active constraints
- Do not auto-scaffold Q1
- Do not map needed.py / doctor.py / expand_prompt.py / idea_gate_contract.py / operator_pin_contract.py / idea_brief_contract.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py
- Do not add WAVE 4 unless a new post-WAVE-3 guess is observed
- Do not retry HTTPS clone after one failure
- Do not write idea.md from new_packet or idea_brief
- Do not treat draft.md as script.md
- Do not make --check FAIL on blank viewer / why now / related
- Do not spend the next run aligning another markdown page to name idea_brief --block/--check
- Do not drop the Idea locks section from expand_prompt.py
- Do not make apply_script or words.py idea-lock INFO a BLOCKED error
- Do not make words.py --strict fail on hook, thin headings, Grow, Cut, or idea-lock INFO alone
- Do not treat words.py IN BAND as apply --write
- Do not drop the words.py import of apply_script.idea_lock_notes
- Do not drop write_path_contract / contract_shape / verify_write_path / placeholder_guard / prove_locks
- Do not add another order wrapper around prove_locks.py
