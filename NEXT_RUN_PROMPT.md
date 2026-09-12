# NEXT RUN PROMPT

Keep the original master prompt unchanged.

Targeted addition from Run 095:

- idea_brief.py --queue ID must keep reprinting paste_block from topic_queue without a folder and without writing idea.md.
- --check must still require a packet folder.
- Do not auto-scaffold Q1. Do not write idea.md from idea_brief.

Targeted addition from Run 094:

- words_contract.py must keep an IN BAND tempfile case. --strict must exit 0 on that case even when INFO prints.
- Do not add another words.py printer fold or wrapper CLI.
- Do not auto-scaffold Q1.

Targeted addition from Run 093:

- words.py must keep printing apply_script.idea_lock_notes() after the band / Grow / Cut / Next lines.
- Those INFO lines must not change --strict and must not become apply --write.
- Keep the import fallback.

Targeted addition from Run 092:

- tools/idea_lock.py may remain as an optional extra printer. It must stay unmapped and must not block --write.

Targeted addition from Run 091:

- apply_script.py dry-run must keep printing idea-lock INFO. INFO must not become a check() error.
- prompts/script_writer.md must keep saving PATH/draft.md.

Targeted addition from Run 090:

- expand_prompt.py must keep an Idea locks section. Refuse text must name idea_brief --block / --check.

Targeted addition from Run 089:

- idea_brief.py --block must keep printing the full idea.md template. --check still gates three fields.
- Do not spend the run aligning another markdown page to name idea_brief --block/--check.

Targeted addition from Run 081:

- After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py` first.
- Do not map words.py, words_contract.py, placeholder_guard.py, or prove_locks.py.
- Remaining high-value work is still human-owned: scaffold Q1, paste idea fields, land WORDS in band, apply --write --refresh, set_status ready_for_vo.
