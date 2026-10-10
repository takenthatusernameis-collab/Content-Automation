# Human session

One page. Follow this instead of scanning `tools/`.

`videos/sample-001-*` is a fixture. Never apply WORDS to it. Never promote it.

Agents without a checkout: `docs/agent_session.md`.
Copy-paste drop recipe on the gate machine: `docs/gate_machine.md`.

## Live job (do this first)

Q1 is already scaffolded. Status stays `ready_for_vo` because the wav is gitignored. Text paperwork is done. Generated VO + 7 cards + r253 master exist on private releases.

On a fresh clone, materialize first (local only; does not commit media):

```bash
python3 tools/materialize_q1_release.py
python3 tools/media_qa.py videos/002-stop-deciding-what-to-work-on-every-morning
```

If vo/, cards/, and export/master.mp4 are already present, do not rematerialize.

- Packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- Remaining human step is the three GitHub Actions secrets. Print the exact steps and pitfalls with:
  ```bash
  python3 tools/operator_card.py
  ```
  Then follow the numbered console steps it reprints (Google Cloud project → Desktop OAuth client → oauth_exchange.py → gh secret set → one dispatch with execute=true collect_feedback=false). Do not poll secrets. Do not commit the token file.
- `publish.md` Description edited and First comment approved are already checked. Do not re-open them. Leave No YouTube upload checked until a real video id exists.
- Keep `vo_origin.md` kind=generated. Do not `git add -f` media. Do not scaffold Q2. Do not edit brief generators unless `python3 tools/closed_brief_gate.py` fails.

Do not start this session at `doctor.py` / `queue_status.py` / `new_packet.py`. Those commands are for a *new* packet. Do not record or synthesize another take while HANDOFF checksums match.

## Start every session (new packet only)

```bash
python3 tools/doctor.py
python3 tools/queue_status.py
```

Skip this block while Q1 is `ready_for_vo` with no selected take. Read the Live job section instead.

Read the doctor block. Run only the printed Command (dry-run first). Doctor writes nothing. queue_status writes nothing. Default queue_status exit is 0. Use `--strict` only when you want a non-zero exit on mark-needed or missing-folder.

If a mark-needed folder already exists, `queue_status.py` prints `idea_brief.py PATH --block`, a paste-by-hand line, and `idea_brief.py PATH --check` under that folder. Follow those printed lines. Do not reopen this page to recover the paste.

If you still need a first real title:

```bash
python3 tools/next_topic.py
```

That command writes nothing. It prints a queued title, a predicted `videos/NNN-slug`, and a dry-run `mark_topic` line. After that predicted folder exists, it also prints `idea_brief.py PATH --block`, a paste-by-hand line, and `idea_brief.py PATH --check`. Prefer the printed title over inventing a new one. Prefer the printed idea_brief lines over scanning this page for the paste.

## First real video (not the fixture)

Q1 already exists. Steps 1–4 below are the completed path, kept so a later packet can reuse them. Do not re-scaffold Q1. Do not run them as the live job.

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
