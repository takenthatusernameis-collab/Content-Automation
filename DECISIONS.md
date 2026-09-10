# DECISIONS

Format: date | decision | why | revisit when

- 2026-09-10 | expand_prompt refuses a blank or template-default idea.md mechanism (exit 2); it does not write idea.md | After the scaffold reprint existed, leftover labor was skipping the paste and expanding from empty fields; auto-writing idea.md would hide that skip | If a human later wants --allow-blank-idea for assembler dry-runs of empty templates (do not add without evidence)
- 2026-09-10 | new_packet reprints idea.md topic + queue one_line after scaffold; it does not write idea.md | After title/path were pinned, leftover labor was copying one_line from the queue; auto-writing idea.md would hide a blank-template expand the same way auto-mark hides a missing folder | If a human later wants a --seed-idea flag (do not add without evidence)
- 2026-09-10 | Pin Q1 working title and predicted folder on human_session; edit idea.md before expand | After commands were restored, leftover labor was inventing a title and expanding from the scaffold default mechanism | If Q1 is replaced or scaffolded under a different slug; do not auto-scaffold to avoid the guess
- 2026-09-10 | Stop extending needed.py after WAVE 3 reconstruct + operator exist | Runs 037-042 compounded reconstruct helpers while videos produced stayed 0; human_session had deferred the first-video write path | If a new clone-less guess appears after WAVE 3 READY; do not add WAVE 4 by default

Earlier decisions remain in force (see prior commits for the full list).
