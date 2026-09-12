# NEXT RUN PROMPT

Keep the original master prompt unchanged.

Targeted addition from Run 103:

- `needed.py next_topic.py --missing` must list the queue_contract reconstruct paths plus `tools/next_topic.py`.
- READY only when that asked alias file exists. Exit stays 0.
- `needed.py queue_status.py` must not grow that list to include next_topic.py.
- Do not add next_topic.py to which_contract.MAP need. Do not add WAVE 4.

Targeted addition from Run 102:

- `needed.py doctor.py` must keep listing doctor.py plus hint.py, next_action.py, pipeline_status.py, queue_lib.py, queue_status.py, validate_packet.py, next_topic.py, and docs/topic_queue.md.
- `--missing` READY only when those nine paths exist. Exit stays 0.
- --plan WAVE 3 must still print only `needed.py doctor.py --missing`, not that file dump.
- Do not add doctor.py to which_contract.MAP. Do not add WAVE 4.

Targeted addition from Run 101:

- `needed.py doctor.py` must keep listing doctor.py plus hint.py, next_action.py, pipeline_status.py, queue_lib.py, queue_status.py, validate_packet.py, and docs/topic_queue.md.
- `--missing` READY only when those eight paths exist. Exit stays 0.
- --plan WAVE 3 must still print only `needed.py doctor.py --missing`, not that file dump.
- Do not add doctor.py to which_contract.MAP. Do not add WAVE 4.

Targeted addition from Run 099:

- needed.py --plan WAVE 3 must keep printing `python3 tools/doctor.py` then `python3 tools/queue_status.py` then `python3 tools/next_topic.py` after the queue_status reconstruct line.
- `needed.py doctor.py` may print the unmapped operator hint. It must not add doctor.py to which_contract.MAP.
- router_contract must keep failing if doctor.py is mapped.
- Do not wrap doctor in start.py. Do not add WAVE 4.

Targeted addition from Run 098:

- doctor.py with no packet argument must keep appending queue_next_footer after packet blocks.
- queue_next_footer must print idea_brief --queue for the first ok-queued row only.
- queue_contract must keep footer assertions: --queue Q2 when Q1 is mark-needed; --queue Q1 when folders are empty.
- Do not print Queue next when doctor is given a single packet path.
- Do not print --queue for a mark-needed row. Do not add another idea_brief flag.

Targeted addition from Run 097:

- queue_status.py and next_topic.py must keep printing `idea_brief.py --queue ID` for the first ok-queued topic before scaffold.
- queue_contract.py must keep the tempfile assertion that the board prints `--queue Q2` and not `--queue Q1` when Q1 is mark-needed.
- Do not print --queue for a mark-needed row. Do not add another idea_brief flag.

Targeted addition from Run 096:

- idea_brief_contract.py must keep queue_locks for --queue Q1 / missing id / --queue --check.
- Do not map idea_brief.py or idea_brief_contract.py.
- Do not add another idea_brief flag unless --queue regresses.
- Do not auto-scaffold Q1. Do not write idea.md from idea_brief.

Targeted addition from Run 095:

- idea_brief.py --queue ID must keep reprinting paste_block from topic_queue without a folder and without writing idea.md.
- --check must still require a packet folder.

Targeted addition from Run 094:

- words_contract.py must keep an IN BAND tempfile case. --strict must exit 0 on that case even when INFO prints.
- Do not add another words.py printer fold or wrapper CLI.

Targeted addition from Run 093:

- words.py must keep printing apply_script.idea_lock_notes() after the band / Grow / Cut / Next lines.
- Those INFO lines must not change --strict. Keep the import fallback.

Targeted addition from Run 081:

- After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py` first.
- Do not map words.py, words_contract.py, placeholder_guard.py, or prove_locks.py.
- Remaining high-value work is still human-owned: scaffold Q1, paste idea fields, land WORDS in band, apply --write --refresh, set_status ready_for_vo.
