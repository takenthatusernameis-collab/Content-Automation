# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-12T11:05:00Z — Run 092

- **Objective:** After apply dry-run prints idea-lock INFO, stop the operator from learning a generic draft missed the mechanism only at apply time. Surface the same INFO on words.py, which already runs on PATH/draft.md first.
- **Inspected:** STATE/NEXT/RUNS after Run 091. words.py printed band / Delta / Hook / Beats / Grow / Cut / Next only. apply_script.py already owned idea_lock_notes().
- **Action taken:** words.py now calls apply_script.idea_lock_notes() after Next. INFO never changes --strict. Import failure prints a fallback INFO. Did not edit apply_script.py, words_contract.py, prove_locks, placeholder_guard, needed.py, idea_brief, or operator boards. Did not scaffold Q1. Did not write idea.md. Did not map any file. Did not turn INFO into FAIL.
- **Result:** words.py committed with print_idea_lock_notes(). Local compile + --strict BELOW draft still exits 2 and prints lock INFO. Queue rows remain queued. No new packet folder. No media.
- **Verification status:** completed for local compile and a BELOW draft that prints idea-lock INFO without changing --strict. unverified for live words.py against a real packet folder with idea.md (HTTPS clone blocked). Did not claim contract PASS this run. Human should run prove_locks.py after this words.py write.
- **Important discovery:** Apply lock INFO is wasted if the operator only looks at words.py band numbers and rewrites for length.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs queue_status.py then human_session.md. After a folder exists: idea_brief --block / --check / expand_prompt / draft.md / words.py / apply dry-run. Do not make lock INFO FAIL. Do not auto-scaffold Q1.

## 2026-09-12T10:20:00Z — Run 091

- apply_script.py idea_lock_notes() prints INFO only. script_writer.md saves PATH/draft.md.

## 2026-09-12T09:16:00Z — Run 090

- expand_prompt.py Idea locks + idea_brief refuse text.

## 2026-09-12T08:11:00Z — Run 089

- idea_brief --block pastes six idea.md fields. --check still gates three.

## Earlier runs 001–88
See prior commits for full detail.
