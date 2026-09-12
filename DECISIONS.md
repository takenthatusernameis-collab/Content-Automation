# DECISIONS

Format: date | decision | why | revisit when

- 2026-09-12 | apply_script.py dry-run prints idea-lock INFO for mechanism / topic tokens vs incoming draft; INFO never becomes check() BLOCKED | Expand Idea locks are wasted if apply still reports OK on a generic draft | If idea.md field names change; do not turn INFO into FAIL; do not treat lock miss as apply --write
- 2026-09-12 | prompts/script_writer.md saves PATH/draft.md and runs words.py / apply dry-run before --write --refresh | First-draft path still wrote script.md and skipped the draft convention locked elsewhere | If apply CLI flags change; do not write script.md from the prompt
- 2026-09-12 | expand_prompt.py prints parsed Idea locks from idea.md and refuses with idea_brief --block/--check | A filled idea.md is wasted if the expand assembler dumps it as a raw clip and the refuse path sends the operator back to the new_packet reprint | If idea.md field names change; do not write script.md from this tool; do not drop Idea locks; do not map expand_prompt.py
- 2026-09-12 | idea_brief --block pastes the full idea.md template (topic, viewer, problem, mechanism, why now, related). --check still gates only topic / problem / mechanism | The three-field block left viewer / why now / related blank after a successful --check, so fill-idea still needed a second invent pass | If channel.md audience changes; do not write idea.md from this tool; do not make extras a --check FAIL
- 2026-09-12 | After Runs 082–088, do not spend a run aligning another page to name idea_brief unless that page is factually wrong | Six page-alignment runs left videos at 0 and automated steps at 71 | If a live printer disagrees with the locked CLIs
- 2026-09-11 | prove_locks.py is an unmapped order wrapper (placeholder_guard then words_contract then verify_write_path) | After a GitHub write agents skipped one of three unmapped commands; the advertised order should be one copy-paste | If those three files merge; do not drop them because the wrapper exists; do not map into needed.py; do not treat PASS as apply --write
- 2026-09-11 | words.py is a read-only band printer, not a lock, and stays unmapped | Operator leftover loop is expand → apply → duration WARN. Checking draft.md first cuts that loop without another reconstruct witness | If format bands move; do not treat IN BAND as apply --write; do not map into needed.py
- 2026-09-11 | write_path_contract must stay an executable tempfile CLI lock, not a docstring-only file | Run 066 claimed PASS while the committed blob was 986 bytes of documentation | If the file has no def main; do not treat STATE PASS as a substitute
- 2026-09-11 | apply_script missing --from exits 2 with draft.md hint | Avoid traceback before the human saves draft.md | Do not add --seed-idea

Earlier decisions remain in force.
