# DECISIONS

Format: date | decision | why | revisit when

- 2026-09-12 | words.py prints apply_script.idea_lock_notes() after the band / Grow / Cut lines; INFO never changes --strict | Apply dry-run is one step too late if the operator already spent an expand pass on a generic draft | If idea_lock_notes moves files; do not make INFO a --strict FAIL; do not treat lock miss as apply --write
- 2026-09-12 | apply_script.py dry-run prints idea-lock INFO; INFO never becomes check() BLOCKED | Expand Idea locks are wasted if apply still reports OK on a generic draft | Do not turn INFO into FAIL
- 2026-09-12 | After Runs 082–088, do not spend a run aligning another page to name idea_brief unless that page is factually wrong | Six page-alignment runs left videos at 0 | If a live printer disagrees with the locked CLIs
- 2026-09-11 | words.py is a read-only band printer, not a lock, and stays unmapped | Checking draft.md first cuts the expand → apply → duration WARN loop | Do not treat IN BAND as apply --write

Earlier decisions remain in force.
