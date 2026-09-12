# DECISIONS

Format: date | decision | why | revisit when

- 2026-09-12 | queue_status and next_topic print idea_brief --queue ID only for the first ok-queued row; queue_contract locks that print | Run 095/096 built --queue but the live board still hid it | If Q1 is scaffolded; do not print --queue for mark-needed rows
- 2026-09-12 | idea_brief_contract.py must prove --queue Q1 paste, missing-id exit 2, and --queue --check exit 2 without creating a folder | Run 095 added --queue without a lock | If --queue regresses; do not map this contract; do not add another idea_brief flag
- 2026-09-12 | idea_brief.py --queue ID reprints paste_block from topic_queue without a videos/ folder | Operators could not recover the six-field paste until after scaffold | If Q1 is scaffolded; do not write idea.md from this flag; do not treat it as new_packet
- 2026-09-12 | words_contract.py must prove IN BAND --strict exit 0 while INFO still prints | Run 093 documented band-only --strict without an IN BAND lock | If words.py --strict starts keying off hook length or idea-lock INFO; do not map this contract
- 2026-09-12 | words.py prints apply_script.idea_lock_notes() after the band / Grow / Cut / Next lines; INFO never changes --strict | Apply dry-run is one step too late if the operator only watches the band numbers | If idea_lock_notes moves files; do not make INFO a --strict FAIL
- 2026-09-12 | idea_lock.py stays as an optional extra CLI after the words.py fold | Some operators will still want the notes without a full band pass | Delete only if it starts drifting from apply_script.idea_lock_notes
- 2026-09-12 | apply_script.py dry-run prints idea-lock INFO; INFO never becomes check() BLOCKED | Expand Idea locks are wasted if apply still reports OK on a generic draft | Do not turn INFO into FAIL
- 2026-09-12 | After Runs 082–088, do not spend a run aligning another page to name idea_brief unless that page is factually wrong | Six page-alignment runs left videos at 0 | If a live printer disagrees with the locked CLIs
- 2026-09-11 | words.py is a read-only band printer, not a lock, and stays unmapped | Checking draft.md first cuts the expand → apply → duration WARN loop | Do not treat IN BAND as apply --write

Earlier decisions remain in force.
