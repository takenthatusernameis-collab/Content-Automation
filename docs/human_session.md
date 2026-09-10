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

That command writes nothing. It prints a queued title, a predicted `videos/NNN-slug`, and a dry-run `mark_topic` line. Prefer the printed title over inventing a new one.

## First real video (not the fixture)

1. Scaffold the printed queue title (Q1 today)

```bash
python3 tools/queue_status.py
python3 tools/next_topic.py
python3 tools/new_packet.py "Stop deciding what to work on every morning"
python3 tools/doctor.py videos/002-stop-deciding-what-to-work-on-every-morning
python3 tools/queue_status.py
```

Use the exact Q1 working title from `docs/topic_queue.md` unless a human replaced that row. `new_packet` reprints the matching `mark_topic --id Q1` dry-run after the folder is created. It also reprints suggested `idea.md` topic + problem + mechanism (problem from the operator pin, mechanism from the queue `one_line`). It does not mark the row used and does not write idea.md. After scaffold, queue_status should show `mark-needed` for that id and the PACKET column from packet.md. Doctor Code should be `fill-idea` until idea.md is pasted.

If scaffold stdout is gone, reprint the same three fields without writing:

```bash
python3 tools/idea_brief.py videos/002-stop-deciding-what-to-work-on-every-morning
python3 tools/idea_brief.py videos/002-stop-deciding-what-to-work-on-every-morning --block
```

`idea_brief.py` writes nothing. It prints current idea.md fields and the suggested paste. `--block` prints only the paste-ready idea.md body. Still does not write idea.md.

```bash
python3 tools/mark_topic.py --id Q1
# python3 tools/mark_topic.py --id Q1 --write
```

`mark_topic` writes nothing until `--write` and a matching non-fixture folder exist.

2. Replace the template mechanism before expanding

Scaffolded `idea.md` still uses blank template fields. Paste the reprint from `new_packet` or `idea_brief` (or the `--block` body, or write these if you skipped the reprint):

- topic: Stop deciding what to work on every morning
- problem: they reopen the whole work list every morning instead of starting
- mechanism: Install a written next-action default so the morning does not reopen the whole list.

Do not treat that edit as spoken WORDS. Do not invent statistics. Do not leave the template-default / blank mechanism. `expand_prompt.py` exits 2 until that paste exists. It does not write idea.md. `next_action.py` / `hint.py` / `doctor.py` stay on `fill-idea` until that paste exists; they will not lead with expand_prompt.

3. Expand off-repo, then paste back only onto the new packet

```bash
python3 tools/expand_prompt.py videos/002-stop-deciding-what-to-work-on-every-morning
# paste that pack into an off-repo writer; do not treat stdout as script.md
python3 tools/apply_script.py videos/002-stop-deciding-what-to-work-on-every-morning --from FILE
# after dry-run OK:
python3 tools/apply_script.py videos/002-stop-deciding-what-to-work-on-every-morning --from FILE --write --refresh
python3 tools/validate_packet.py videos/002-stop-deciding-what-to-work-on-every-morning
```

If expand_prompt prints `refusing expand: idea.md mechanism is blank or template-default`, or doctor prints `Code: fill-idea`, go back to step 2. Do not run `apply_script.py --write` on `videos/sample-001-*`. Do not auto-write WORDS. Do not pad the fixture.

4. Promote only when spoken WORDS sit in the 900-1500 band

```bash
python3 tools/set_status.py videos/002-stop-deciding-what-to-work-on-every-morning --to ready_for_vo
# after dry-run OK and no duration WARN:
python3 tools/set_status.py videos/002-stop-deciding-what-to-work-on-every-morning --to ready_for_vo --write
python3 tools/vo_session.py videos/002-stop-deciding-what-to-work-on-every-morning
```

Then record the selected take at the named path in `vo_session.md`. Do not invent a wav. Do not write an ffmpeg recipe.

If unsure of the next command after any step, re-run `python3 tools/doctor.py videos/002-stop-deciding-what-to-work-on-every-morning` and use the printed Command.

## Stop

- Do not pad the fixture to clear Duration WARN.
- Do not treat the topic queue as a finished script.
- Do not mark a queue row used without a matching `videos/` folder.
- Do not expect `new_packet.py`, `idea_brief.py`, or `queue_status.py` to write the queue or idea.md.
- Do not treat `expand_prompt.py` stdout as a rewritten script.
- Do not promote while duration WARN is present.
- Do not expand while idea.md still says `template-default` / generic or blank mechanism.
