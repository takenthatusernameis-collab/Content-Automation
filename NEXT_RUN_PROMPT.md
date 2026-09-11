# NEXT RUN PROMPT

Keep the original master prompt unchanged.

Targeted addition from Run 077:

- After reconstructing or editing words.py, run `python3 tools/words_contract.py`. Expect WORDS CONTRACT PASS, exit 0, no videos/ writes. FAIL if words.py is missing, under 8000 bytes, a placeholder, or Grow/Cut stop printing.
- After the human saves PATH/draft.md, run `python3 tools/words.py PATH` before apply --write. Read Result, Delta, Hook Delta, Beats, Thin, and Grow or Cut. `--strict` exits 2 when the draft is not IN BAND. It does not fail on hook length, thin headings, Grow, or Cut alone.
- After reconstructing write-path tools, run `python3 tools/verify_write_path.py` instead of inventing a two-command order from memory.
- Do not add another printer line to words.py unless a new heading-choice guess is observed. Runs 071-076 already cover band, Delta, Hook Delta, Beats, Thin, Grow, and Cut.
- Do not map words.py or words_contract.py.
- Do not treat Delta, Hook Delta, Beats, Thin, Grow, Cut, or WORDS CONTRACT PASS as permission to invent filler or to apply --write.
- Remaining high-value work is still human-owned: scaffold Q1, paste idea fields, land WORDS in band, apply --write --refresh, set_status ready_for_vo.
