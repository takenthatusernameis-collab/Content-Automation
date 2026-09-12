# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-12T14:25:00Z — Run 095

- **Objective:** Let an operator reprint the Q1 idea.md paste before a packet folder exists, without writing idea.md or scaffolding Q1.
- **Inspected:** STATE/NEXT after Run 094. words_contract IN BAND locked. Queue still queued. Fixture only. idea_brief required a packet directory.
- **Action taken:** Added `idea_brief.py --queue ID`. Prints the same six-field paste_block as --block from topic_queue + idea_followup. Missing id exits 2. --check with --queue exits 2. No folder required. Did not write idea.md. Did not scaffold Q1. Did not map idea_brief. Did not add an idea-lock wrapper. Did not change human_session (page-alignment ban).
- **Result:** Local --queue Q1 exit 0 with topic/problem/mechanism present. Committed tools/idea_brief.py (~10KB, includes print_queue_block). Queue still queued. No new packet. No media.
- **Verification status:** completed for local --queue Q1/Q9/--check combo. unverified for idea_brief_contract.py on a full repo checkout (HTTPS clone blocked; contract file not extended this run).
- **Important discovery:** The paste no longer depends on scaffold stdout or a videos/ folder. The remaining human gate is still creating the folder and saving draft.md in band.
- **Blocker:** Human-owned non-fixture draft still missing. HTTPS clone unavailable; do not retry it first.
- **Recommended next action:** Human follows docs/human_session.md on Q1. May run idea_brief --queue Q1 first. Do not add another idea-lock wrapper.

## 2026-09-12T13:30:00Z — Run 094

- **Objective:** Lock the documented rule that words.py --strict keys off the total band only, including an IN BAND draft that still prints idea-lock INFO.
- **Result:** Local words_contract PASS (exit 0). Queue still queued.

## 2026-09-12T12:15:00Z — Run 093

- **Objective:** Fold apply_script.idea_lock_notes into words.py so idea_lock.py is not a required extra command.
- **Result:** words.py 15563 bytes with the fold. words_contract PASS locally.

## Earlier runs 001–92
See prior commits for full detail.
