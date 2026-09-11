# DECISIONS

Format: date | decision | why | revisit when

- 2026-09-11 | write_path_contract subprocess-runs non-fixture apply_script --refresh (no --write), --write, and --write --refresh | The printed human_session success line is `--write --refresh`; helper-only checks cannot catch a dry-run that refreshes derived files or a --write that no-ops | If leftover labor remains after a human-owned non-fixture draft.md dry-run; do not drop these subprocesses; do not auto-scaffold Q1
- 2026-09-11 | write_path_contract subprocess-runs apply_script --from fixture/draft.md --write and expects exit 1 + BLOCKED + unchanged script.md | Helper-only apply_check cannot catch a main() that writes script.md before the fixture refuse; NEXT already forbids --write on sample-001 | If leftover labor remains after a human-owned non-fixture draft.md dry-run; do not drop the fixture --write subprocess; do not auto-scaffold Q1
- 2026-09-11 | write_path_contract subprocess-runs apply_script dry-run --from an existing draft.md and expects exit 0 + Dry-run only + unchanged script.md | After the missing-file CLI lock, leftover risk was a default-write regression hiding behind helper checks | If leftover labor remains after the printed apply dry-run on an existing draft.md; do not add --seed-idea; do not drop the existing-draft subprocess
- 2026-09-11 | apply_script missing --from path exits 2 with a draft.md hint instead of a traceback | After PATH/draft.md was printed, leftover labor was a stack trace if the human ran the line before saving the draft; another idea_brief flag would hide that | If leftover labor remains after the printed apply dry-run on an existing draft.md; do not add --seed-idea
- 2026-09-11 | idea_brief.py --check PASTE READY prints dry-run apply_script --from FILE after expand_prompt; still does not write and does not print --write | After expand_prompt was printed, leftover labor was hunting apply_script on human_session; another flag would hide that | If leftover labor remains after the printed apply dry-run; do not add --seed-idea

Earlier decisions remain in force (see prior commits for the full list).
