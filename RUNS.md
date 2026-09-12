# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-12T15:10:00Z — Run 096

- **Objective:** Lock idea_brief.py --queue so the pre-scaffold paste cannot regress without a contract fail.
- **Inspected:** STATE/NEXT after Run 095. --queue existed and was locally verified, but idea_brief_contract.py still only covered folder --block/--check.
- **Action taken:** Extended tools/idea_brief_contract.py with queue_locks(): --queue Q1 exit 0 and six-field paste; missing Q9 exit 2; --queue --check exit 2; videos/ folder set unchanged. Did not scaffold Q1. Did not write idea.md. Did not map idea_brief or the contract. Did not add a wrapper CLI. Did not change human_session.
- **Result:** Local IDEA BRIEF CONTRACT PASS (exit 0) on a reconstruct tree. Queue still queued. No new packet. No media.
- **Verification status:** completed for local contract PASS including --queue cases. unverified on a full GitHub checkout (HTTPS clone blocked).
- **Important discovery:** The remaining human gate is still creating the folder and saving draft.md in band. Another reprint flag would not move that gate.
- **Blocker:** Human-owned non-fixture draft still missing. HTTPS clone unavailable; do not retry it first.
- **Recommended next action:** Human follows docs/human_session.md on Q1. May run idea_brief --queue Q1 first. Do not add another idea_brief flag.

## 2026-09-12T14:25:00Z — Run 095

- **Objective:** Let an operator reprint the Q1 idea.md paste before a packet folder exists, without writing idea.md or scaffolding Q1.
- **Result:** Local --queue Q1 exit 0. Queue still queued.

## 2026-09-12T13:30:00Z — Run 094

- **Objective:** Lock words.py --strict to the total band only, including IN BAND + INFO.
- **Result:** Local words_contract PASS.

## Earlier runs 001–93
See prior commits for full detail.
