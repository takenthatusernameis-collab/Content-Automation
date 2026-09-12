# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-12T01:15:00Z — Run 082

- **Objective:** After scaffold, hint.py still told the operator to paste idea.md from memory and apply from FILE. human_session already names idea_brief --block/--check and words.py PATH/draft.md. That lookup is recurring human labor on every packet.
- **Inspected:** STATE/NEXT/RUNS/ROADMAP after Run 081. Lock wrappers are complete and another wrapper is forbidden. Remaining labor is still human Q1 scaffold + WORDS in band. hint.py was the printer that did not match the session.
- **Action taken:** Updated tools/hint.py fill-idea to print idea_brief reprint / --block / --check. Updated write-script and expand-script to print expand_prompt, words.py PATH, and apply from PATH/draft.md (fixture still refuses --write). Did not edit prove_locks, placeholder_guard, words.py, write-path tools, or needed.py. Did not scaffold Q1. Did not write idea.md. Did not map any file. Did not add a lock wrapper.
- **Result:** hint.py compiles. Source contains idea_brief.py, words.py, draft.md, and --write --refresh. Queue rows remain queued. No new packet folder. No media. No new tool file.
- **Verification status:** completed for syntax and marker presence on the local hint.py blob. unverified for live hint.py against sample-001 or a Q1 folder (HTTPS clone blocked; packet tree not on this sandbox disk). Did not claim WRITE PATH CONTRACT PASS, WORDS CONTRACT PASS, PLACEHOLDER GUARD PASS, or PROVE LOCKS PASS this run.
- **Important discovery:** Session docs can be correct while the command printer the human is told to re-run still omits the later tools. Align the printer; do not add another lock.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After scaffold, `python3 tools/hint.py PATH` should now print idea_brief and words.py. After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py`. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1. Do not add another words.py printer line. Do not add another order wrapper. Do not map words.py, words_contract.py, placeholder_guard.py, or prove_locks.py.

## 2026-09-12T00:21:00Z — Run 081

- **Objective:** prove_locks.py is now the advertised first post-write command, but placeholder_guard did not witness that wrapper. An emptied prove_locks.py would still let the inner three look healthy if an agent ran them as fallback.
- **Inspected:** STATE/NEXT/RUNS/ROADMAP after Run 080. Remaining labor is still human Q1 scaffold + WORDS in band. Another wrapper around prove_locks is forbidden. Extending the existing guard is the leftover hole.
- **Action taken:** Added prove_locks.py to tools/placeholder_guard.py CHECKS (800-byte floor + PROVE LOCKS PASS + the three inner filenames). Did not edit prove_locks.py, words.py, write-path tools, or needed.py. Did not scaffold Q1. Did not write idea.md. Did not map any file.
- **Result:** Isolated sandbox: missing prove_locks.py FAIL exit 1; 8-byte see-next prove_locks.py FAIL (undersize + placeholder + missing markers). Queue rows remain queued. No new packet folder. No media. No new tool file.
- **Verification status:** completed for isolated FAIL paths on the new sibling. unverified for live PLACEHOLDER GUARD PASS / PROVE LOCKS PASS against the committed sibling tree (HTTPS clone blocked; siblings not on this sandbox disk). Did not claim WRITE PATH CONTRACT PASS, WORDS CONTRACT PASS, PLACEHOLDER GUARD PASS, or PROVE LOCKS PASS this run.
- **Important discovery:** A preferred wrapper that is not in the first inner lock can be emptied without the fallback path noticing.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After saving PATH/draft.md, run `python3 tools/words.py PATH`. After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py`. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1. Do not add another words.py printer line. Do not add another order wrapper. Do not map words.py, words_contract.py, placeholder_guard.py, or prove_locks.py.

## 2026-09-11T22:03:00Z — Run 080

- **Objective:** Run 079 added tools/prove_locks.py but left NEXT_RUN_PROMPT.md listing placeholder_guard, words_contract, and verify_write_path as the primary post-write actions. Future agents copy the addendum first. Align the addendum and the run record so the wrapper is the first command, without another lock file.
- **Action taken:** Rewrote NEXT_RUN_PROMPT.md so prove_locks.py is the first post-write command and the three inner commands are fallback.
- **Result:** Documentation now matches agent_session and DECISIONS for the post-write order.
- **Verification status:** completed for NEXT_RUN_PROMPT text. unverified for live PROVE LOCKS PASS.
- **Important discovery:** Adding a preferred command without updating NEXT_RUN_PROMPT in the same run recreates the skip that the command was meant to prevent.

## 2026-09-11T21:20:00Z — Run 079

- **Action taken:** Added tools/prove_locks.py.
- **Result:** Isolated sandbox: missing placeholder_guard.py FAIL exit 1.

## 2026-09-11T20:10:00Z — Run 078

- **Action taken:** Added tools/placeholder_guard.py.
- **Result:** Isolated sandbox: missing siblings FAIL exit 1.

## Earlier runs 001–77
See prior commits for full detail.
