# NEXT RUN PROMPT

Keep the original master prompt unchanged.

Targeted addition from Run 071:

- After the human saves PATH/draft.md, run `python3 tools/words.py PATH` before apply --write. `--strict` exits 2 when the draft is not IN BAND.
- After reconstructing write-path tools, run `python3 tools/verify_write_path.py` instead of inventing a two-command order from memory.
- Do not add another witness file unless a new emptied-file failure is observed. Runs 068–070 already cover shape, trio, and order.
- Do not map words.py. It is a printer, not a lock.
- Remaining high-value work is still human-owned: scaffold Q1, paste idea fields, land WORDS in band, apply --write --refresh, set_status ready_for_vo.
