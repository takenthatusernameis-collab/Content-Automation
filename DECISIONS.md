# DECISIONS

Format: date | decision | why | revisit when

- 2026-09-11 | write_path_contract subprocess-runs apply_script dry-run --from an existing draft.md and expects exit 0 + Dry-run only + unchanged script.md | After the missing-file CLI lock, leftover risk was a default-write regression hiding behind helper checks | If leftover labor remains after the printed apply dry-run on an existing draft.md; do not add --seed-idea; do not drop the existing-draft subprocess
- 2026-09-11 | apply_script missing --from path exits 2 with a draft.md hint instead of a traceback | After PATH/draft.md was printed, leftover labor was a stack trace if the human ran the line before saving the draft; another idea_brief flag would hide that | If leftover labor remains after the printed apply dry-run on an existing draft.md; do not add --seed-idea
- 2026-09-11 | idea_brief.py --check PASTE READY prints dry-run apply_script --from FILE after expand_prompt; still does not write and does not print --write | After expand_prompt was printed, leftover labor was hunting apply_script on human_session; another flag would hide that | If leftover labor remains after the printed apply dry-run; do not add --seed-idea
- 2026-09-10 | default idea_brief reprint prints the exact --check (and --block) command for that packet | After --check existed, leftover labor was replacing the PATH placeholder on the default reprint; another flag would hide that | If leftover labor remains after PASTE READY + printed expand_prompt; do not add --seed-idea
- 2026-09-10 | idea_brief.py --check compares current idea.md to the suggested paste and still does not write idea.md | After --block existed, leftover labor was guessing whether the hand paste matched; --seed-idea would hide a blank-template expand | If a human wants --seed-idea; do not treat PASS as Q1 scaffolded
- 2026-09-10 | idea_brief.py --block prints a paste-ready idea.md body and still does not write idea.md | After reprint recover existed, leftover labor was reshaping three labeled lines into the idea.md template; --seed-idea would hide a blank-template expand | If a human wants --seed-idea; do not treat PASS as Q1 scaffolded
- 2026-09-10 | idea_brief_contract.py locks idea_brief as a read-only reprint recover; stays unmapped in which_contract | Run 052 shipped the recover tool with no lock; a later run could add --write and hide a blank-template expand | If a human wants --seed-idea; do not treat PASS as Q1 scaffolded

Earlier decisions remain in force (see prior commits for the full list).
