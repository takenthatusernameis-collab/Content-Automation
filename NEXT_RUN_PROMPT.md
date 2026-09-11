# NEXT RUN PROMPT

Keep the original master prompt unchanged.

Targeted addition from Run 078:

- After a GitHub write of a high-risk tool (words.py, words_contract.py, write_path_contract.py, apply_script.py, set_status.py, contract_shape.py, verify_write_path.py), run `python3 tools/placeholder_guard.py`. Expect PLACEHOLDER GUARD PASS, exit 0, no videos/ writes. FAIL if any listed file is missing, under its size floor, missing markers, or a placeholder / docstring-only body.
- After reconstructing or editing words.py, run `python3 tools/words_contract.py`. Expect WORDS CONTRACT PASS, exit 0, no videos/ writes.
- After the human saves PATH/draft.md, run `python3 tools/words.py PATH` before apply --write. Read Result, Delta, Hook Delta, Beats, Thin, and Grow or Cut. `--strict` exits 2 when the draft is not IN BAND. It does not fail on hook length, thin headings, Grow, or Cut alone.
- After reconstructing write-path tools, run `python3 tools/verify_write_path.py` instead of inventing a two-command order from memory.
- Do not add another printer line to words.py unless a new heading-choice guess is observed. Runs 071-076 already cover band, Delta, Hook Delta, Beats, Thin, Grow, and Cut.
- Do not map words.py, words_contract.py, or placeholder_guard.py.
- Do not treat Delta, Hook Delta, Beats, Thin, Grow, Cut, WORDS CONTRACT PASS, or PLACEHOLDER GUARD PASS as permission to invent filler or to apply --write.
- Remaining high-value work is still human-owned: scaffold Q1, paste idea fields, land WORDS in band, apply --write --refresh, set_status ready_for_vo.
