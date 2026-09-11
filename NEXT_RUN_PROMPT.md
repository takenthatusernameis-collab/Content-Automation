# NEXT RUN PROMPT

Keep the original master prompt unchanged.

Targeted addition from Run 076:

- After the human saves PATH/draft.md, run `python3 tools/words.py PATH` before apply --write. Read Result, Delta, Hook Delta, Beats, Thin, and Grow or Cut. `--strict` exits 2 when the draft is not IN BAND. It does not fail on hook length, thin headings, Grow, or Cut alone.
- After reconstructing write-path tools, run `python3 tools/verify_write_path.py` instead of inventing a two-command order from memory.
- Do not add another witness file unless a new emptied-file failure is observed. Runs 068–070 already cover shape, trio, and order.
- Do not map words.py. It is a printer, not a lock.
- Do not treat Delta, Hook Delta, Beats, Thin, Grow, or Cut as permission to invent filler.
- Remaining high-value work is still human-owned: scaffold Q1, paste idea fields, land WORDS in band, apply --write --refresh, set_status ready_for_vo.
