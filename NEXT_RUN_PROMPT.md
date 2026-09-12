# NEXT RUN PROMPT

Keep the original master prompt unchanged.

Targeted addition from Run 086:

- docs/agent_session.md WAVE 3 board paragraph must keep naming `idea_brief.py PATH --block`, a paste-by-hand line, and `idea_brief.py PATH --check` after a mark-needed folder exists. Do not revert that page to "stop at the board" without those lines.
- Do not add a lock around agent_session.md.

Targeted addition from Run 085:

- docs/human_session.md Start every session must keep naming `idea_brief.py PATH --block`, a paste-by-hand line, and `idea_brief.py PATH --check` after a mark-needed folder exists and after next_topic prints an existing predicted path. Do not revert that page to mark_topic-only.
- Do not add a lock around human_session.md.

Targeted addition from Run 084:

- queue_status.py mark-needed follow-up must keep printing `idea_brief.py PATH --block`, a paste-by-hand line, and `idea_brief.py PATH --check`. next_topic.py after-folder lines must keep the same three lines. Do not revert those printers to mark_topic-only.
- Do not add a lock around queue_status.py or next_topic.py. Do not map them.

Targeted addition from Run 083:

- next_action.py fill-idea Why must keep naming idea_brief --block / paste / --check. doctor.py and hint.py reprint that Why. Do not revert to "Paste the new_packet reprint before expand_prompt."
- Do not add a lock around next_action.py. Do not map next_action.py.

Targeted addition from Run 082:

- hint.py fill-idea must keep printing `idea_brief.py PATH`, `--block`, and `--check`. write-script / expand-script must keep printing `words.py PATH` and apply from `PATH/draft.md`. Do not revert to "paste from the new_packet reprint" + `apply --from FILE`.
- After scaffold on a live packet, `python3 tools/hint.py PATH` is the copy-paste surface. Do not add a lock around hint.py. Do not map hint.py.
- Remaining high-value work is still human-owned: scaffold Q1, paste idea fields, land WORDS in band, apply --write --refresh, set_status ready_for_vo.

Targeted addition from Run 081:

- After a GitHub write of a high-risk tool (words.py, words_contract.py, write_path_contract.py, apply_script.py, set_status.py, contract_shape.py, verify_write_path.py, placeholder_guard.py, prove_locks.py), run `python3 tools/prove_locks.py` first. Expect each inner PASS then PROVE LOCKS PASS, exit 0, no videos/ writes. FAIL if placeholder_guard.py, words_contract.py, or verify_write_path.py is missing or any step exits non-zero.
- The three separate commands remain valid only when the wrapper is missing: `python3 tools/placeholder_guard.py` then `python3 tools/words_contract.py` then `python3 tools/verify_write_path.py`.
- placeholder_guard.py must keep witnessing prove_locks.py (800-byte floor + PROVE LOCKS PASS + the three inner filenames). Do not drop that check.
- After reconstructing or editing words.py, `prove_locks.py` already runs words_contract. Do not skip the wrapper to run words_contract alone unless the wrapper file is absent.
- After the human saves PATH/draft.md, run `python3 tools/words.py PATH` before apply --write. Read Result, Delta, Hook Delta, Beats, Thin, and Grow or Cut. `--strict` exits 2 when the draft is not IN BAND. It does not fail on hook length, thin headings, Grow, or Cut alone.
- After reconstructing write-path tools, `prove_locks.py` already runs verify_write_path. Do not invent a two-command order from memory.
- Do not add another printer line to words.py unless a new heading-choice guess is observed. Runs 071-076 already cover band, Delta, Hook Delta, Beats, Thin, Grow, and Cut.
- Do not add another order wrapper around prove_locks.py.
- Do not map words.py, words_contract.py, placeholder_guard.py, or prove_locks.py.
- Do not treat Delta, Hook Delta, Beats, Thin, Grow, Cut, WORDS CONTRACT PASS, PLACEHOLDER GUARD PASS, or PROVE LOCKS PASS as permission to invent filler or to apply --write.
