# Human session

One page. Follow this instead of scanning `tools/`.

`videos/sample-001-*` is a fixture. Never apply WORDS to it. Never promote it.

Agents without a checkout: `docs/agent_session.md`.

## Start every session

```bash
python3 tools/doctor.py
```

Read the block. Run only the printed Command (dry-run first). Doctor writes nothing.

Agents changing tools also run:

```bash
python3 tools/selftest.py
```

That check is not a second human start command.

## First real video (not the fixture)

1. Scaffold

```bash
python3 tools/new_packet.py "Working title that states the viewer job"
python3 tools/doctor.py videos/NNN-slug
```

2. Lock the idea if the card is still a template

```bash
python3 tools/new_idea.py "one-line topic"
```

3. Expand spoken WORDS off-repo (900–1500 for `explainer-6-10min`). Use:

```bash
python3 tools/expand_prompt.py videos/NNN-slug
```

Paste that pack into a writer. Save the result as a local file, not onto `sample-001`.

4. Apply the pasted draft (dry-run, then write)

```bash
python3 tools/apply_script.py videos/NNN-slug --from /tmp/draft.md
python3 tools/apply_script.py videos/NNN-slug --from /tmp/draft.md --write --refresh
python3 tools/doctor.py videos/NNN-slug
```

5. If doctor shows no Duration WARN and Code is `record-vo`:

```bash
python3 tools/set_status.py videos/NNN-slug --to ready_for_vo
# only after the dry-run looks right:
python3 tools/set_status.py videos/NNN-slug --to ready_for_vo --write
```

6. Record the take named in `vo_session.md`. Do not invent a wav in git. Put the file on disk, then doctor again.

7. Later statuses need disk evidence. Use `set_status.py` dry-run first. Never skip-ahead.

## Stop

- Do not pad the fixture to clear Duration WARN.
- Do not treat `expand.md` or expand_prompt stdout as WORDS.
- Do not treat `vo_session.md` as recorded audio.
- Do not run `--write` as the first command doctor/hint print.
- Do not call YouTube, TTS, Whisper, stock, or ffmpeg from this page.

## After a take exists

Doctor will move the Code off `record-vo`. Follow that Code. Still dry-run writes.
