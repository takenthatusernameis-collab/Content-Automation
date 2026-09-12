# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-12T16:20:00Z — Run 097

- **Objective:** Surface the existing idea_brief --queue reprint on the live operator printers so a human does not open docs to recover the Q1 paste.
- **Inspected:** STATE/NEXT after Run 096. --queue and idea_brief_contract existed, but queue_status and next_topic only printed new_packet / post-folder --block.
- **Action taken:** queue_status.report() prints `idea_brief.py --queue ID` for the first ok-queued row. next_topic.py prints the same line before scaffold. queue_contract locks `--queue Q2` on the tempfile board (Q1 is mark-needed there) and forbids `--queue Q1` in that tree. Did not scaffold Q1. Did not write idea.md. Did not map idea_brief. Did not add a flag.
- **Result:** Local QUEUE CONTRACT PASS (exit 0). Queue still queued. No new packet. No media.
- **Verification status:** completed for local queue_contract PASS. unverified on a full GitHub checkout (HTTPS clone blocked).
- **Important discovery:** The remaining human gate is still creating the folder and saving draft.md in band. Printer alignment of an already-built flag is the last cheap step before that gate.
- **Blocker:** Human-owned non-fixture draft still missing. HTTPS clone unavailable; do not retry it first.
- **Recommended next action:** Human follows docs/human_session.md on Q1. May run idea_brief --queue Q1 from the board first. Do not add another idea_brief flag.

## 2026-09-12T15:10:00Z — Run 096

- **Objective:** Lock idea_brief.py --queue so the pre-scaffold paste cannot regress without a contract fail.
- **Result:** Local IDEA BRIEF CONTRACT PASS (exit 0). Queue still queued.

## 2026-09-12T14:25:00Z — Run 095

- **Objective:** Let an operator reprint the Q1 idea.md paste before a packet folder exists, without writing idea.md or scaffolding Q1.
- **Result:** Local --queue Q1 exit 0. Queue still queued.

## 2026-09-12T13:30:00Z — Run 094

- **Objective:** Lock words.py --strict to the total band only, including IN BAND + INFO.
- **Result:** Local words_contract PASS.

## Earlier runs 001–93
See prior commits for full detail.
