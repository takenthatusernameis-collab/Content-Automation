# NEXT RUN PROMPT

Keep the original master prompt unchanged.

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
- Remaining high-value work is still human-owned: scaffold Q1, paste idea fields, land WORDS in band, apply --write --refresh, set_status ready_for_vo.
