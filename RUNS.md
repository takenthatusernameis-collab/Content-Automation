# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-12T10:20:00Z — Run 091

- **Objective:** After expand_prompt prints Idea locks, stop apply dry-run from accepting a generic draft that never names the pasted mechanism, and stop the first-draft writer prompt from writing script.md directly.
- **Inspected:** STATE/NEXT/RUNS after Run 090. apply_script.py checked headings, hook band, fixture, and expand-prompt markers only. prompts/script_writer.md ended at validate_packet / expand_brief and did not name draft.md or words.py.
- **Action taken:** Added idea_lock_notes() to tools/apply_script.py. Dry-run prints INFO for mechanism / topic token overlap. INFO is not a check() error and does not change exit codes. Updated prompts/script_writer.md to treat idea.md fields as locks, save PATH/draft.md, and run words.py + apply dry-run before --write --refresh. Did not edit write_path_contract, contract_shape, prove_locks, placeholder_guard, words.py, needed.py, idea_brief, or operator boards. Did not scaffold Q1. Did not write idea.md. Did not map any file. Did not turn INFO into FAIL.
- **Result:** First push of apply_script.py accidentally landed PLACEHOLDER_SEE_NEXT (commit 6f6a4da). Restored same run to 10697 bytes (commit 9950bd9) with idea_lock_notes(). script_writer.md names draft.md, words.py, and lock-miss rewrite. Queue rows remain queued. No new packet folder. No media.
- **Verification status:** completed for committed apply_script.py size 10697 and markers (idea lock, does not block --write). unverified for live apply against a real packet folder (HTTPS clone blocked; packet tree not on this sandbox disk). Did not claim WRITE PATH CONTRACT PASS, WORDS CONTRACT PASS, PLACEHOLDER GUARD PASS, or PROVE LOCKS PASS this run. Human should run prove_locks.py after this high-risk apply_script write. Recorded the placeholder in FAILURES.md.
- **Important discovery:** Idea locks in the expand prompt are wasted if apply still reports OK on a draft that never uses the mechanism tokens.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After a mark-needed folder exists, paste idea_brief --block, --check, expand_prompt, save draft.md, words.py, apply dry-run (read lock INFO). Do not make lock INFO a BLOCKED error. Do not auto-write idea.md. Do not auto-scaffold Q1. After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py`.

## 2026-09-12T09:16:00Z — Run 090

- **Objective:** After idea_brief --block fills all six idea.md fields, stop the expand writer from treating idea.md as an optional blob and stop the refuse path from sending the operator back to the new_packet reprint.
- **Inspected:** STATE/NEXT/RUNS after Run 089. expand_prompt.py dumped clipped idea.md with no parsed locks. Refuse text said "Paste the new_packet reprint into idea.md first." script_expander.md still used /tmp/new-script.md and did not name idea_brief.
- **Action taken:** Added idea_locks() to tools/expand_prompt.py and an Idea locks section in the assembled prompt. Refuse path now prints idea_brief --block/--check. Output steps name PATH/draft.md and words.py. Updated prompts/script_expander.md to match. Did not edit idea_brief.py, idea_brief_contract, printers, prove_locks, placeholder_guard, words.py, write-path tools, or needed.py. Did not scaffold Q1. Did not write idea.md. Did not map any file. Did not align another operator board page.
- **Result:** expand_prompt.py committed at 8111 bytes with idea_locks and idea_brief refuse lines. script_expander.md names idea_brief, Idea locks, words.py, and draft.md. Queue rows remain queued. No new packet folder. No media.
- **Verification status:** completed for committed blob markers (Idea locks, idea_brief.py, draft.md) and size 8111. compile-checked locally before push. unverified for live expand_prompt against a real packet folder (HTTPS clone blocked; packet tree not on this sandbox disk). Did not claim IDEA BRIEF CONTRACT PASS, WRITE PATH CONTRACT PASS, WORDS CONTRACT PASS, PLACEHOLDER GUARD PASS, or PROVE LOCKS PASS this run.
- **Important discovery:** Filling idea.md is wasted if the expand assembler does not surface those fields as locks. The leftover labor after Run 089 was generic scripts that ignore the paste.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After a mark-needed folder exists, paste idea_brief --block, --check, then expand_prompt (Idea locks in stdout). Do not drop idea_locks. Do not auto-write idea.md. Do not auto-scaffold Q1. After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py`.

## 2026-09-12T08:11:00Z — Run 089

- **Objective:** Stop the 082–088 page-alignment chain. Make fill-idea a single paste of the whole idea.md template instead of three locked fields plus three leftover blanks.
- **Inspected:** STATE/NEXT/RUNS after Run 088. idea.md template has six fields. idea_brief --block only printed topic / problem / mechanism. idea_brief_contract gates those three. Remaining labor is still human Q1 scaffold + WORDS in band.
- **Action taken:** Extended tools/idea_brief.py paste_block with viewer / why now / related from the channel lock. --check still gates only the three locked fields; extras print INFO. Flagged Runs 082–088 in FAILURES.md as a watch. Did not edit idea_brief_contract, printers, prove_locks, placeholder_guard, words.py, write-path tools, or needed.py. Did not scaffold Q1. Did not write idea.md. Did not map any file.
- **Result:** idea_brief.py committed at 8491 bytes with VIEWER / WHY_NOW / RELATED in paste_block. Queue rows remain queued. No new packet folder. No media.
- **Verification status:** completed for committed blob markers (topic/viewer/problem/mechanism/why now/related in paste_block). unverified for live idea_brief --block/--check against a real packet folder (HTTPS clone blocked; packet tree not on this sandbox disk). Did not claim IDEA BRIEF CONTRACT PASS, WRITE PATH CONTRACT PASS, WORDS CONTRACT PASS, PLACEHOLDER GUARD PASS, or PROVE LOCKS PASS this run.
- **Important discovery:** Aligning more operator pages does not fill idea.md. The leftover invent pass after a three-field --check was still human labor on every future packet.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After a mark-needed folder exists, paste `idea_brief.py PATH --block` (now six fields) and `--check`. Do not align another page to name idea_brief. Do not auto-write idea.md. Do not auto-scaffold Q1. Do not make extras a --check FAIL. After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py`.

## Earlier runs 001–88
See prior commits for full detail.
