# Human session

One page. Follow this instead of scanning `tools/`.

`videos/sample-001-*` is a fixture. Never apply WORDS to it. Never promote it.

Agents without a checkout: `docs/agent_session.md`.

## Start every session

```bash
python3 tools/doctor.py
python3 tools/queue_status.py
```

Read the doctor block. Run only the printed Command (dry-run first). Doctor writes nothing. queue_status writes nothing. Default queue_status exit is 0. Use `--strict` only when you want a non-zero exit on mark-needed or missing-folder.

If you still need a first real title:

```bash
python3 tools/next_topic.py
```

That command writes nothing. It prints a queued title, a predicted `videos/NNN-slug`, and a dry-run `mark_topic` line.

## First real video (not the fixture)

1. Scaffold the printed queue title (or your own)

```bash
python3 tools/queue_status.py
python3 tools/next_topic.py
python3 tools/new_packet.py "Working title that states the viewer job"
python3 tools/doctor.py videos/002-slug
python3 tools/queue_status.py
```

`new_packet` reprints the matching `mark_topic --id QN` dry-run after the folder is created. It does not mark the row used. After scaffold, queue_status should show `mark-needed` for that id and the PACKET column from packet.md.

```bash
python3 tools/mark_topic.py --id Q1
# python3 tools/mark_topic.py --id Q1 --write
```

`mark_topic` writes nothing until `--write` and a matching non-fixture folder exist.

Then follow expand_prompt -> apply_script (non-fixture) -> set_status dry-run as in prior versions of this page.

## Stop

- Do not pad the fixture to clear Duration WARN.
- Do not treat the topic queue as a finished script.
- Do not mark a queue row used without a matching `videos/` folder.
- Do not expect `new_packet.py` or `queue_status.py` to write the queue.
