# Content-Automation

Recurring-agent workspace for a low-labor YouTube production system.

## Live packet (do this first)

Status `ready_for_vo`. Text paperwork is done. The remaining human gate is a selected take.

- Packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- Reading card: `vo_session.md` (952 words, ~06:21)
- Put the take here (wav or flac): `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`
- Drop recipe: `docs/gate_machine.md` (generated fallback authorized; optional already-installed TTS one-liners). Do not wrap TTS under tools/.
- Repo-root `vo/` is not Selected VO. `.gitignore` keeps the take local. Do not `git add -f` it.
- After the file exists locally: `docs/human_session.md` steps 5–7.

Do not scaffold Q2. Do not start from the sample-001 commands below. Those are contract examples, not the live job.

Start here for context:
- `docs/gate_machine.md` — packet-relative Selected VO drop on the gate machine (do this before doctor/queue/scaffold)
- `docs/human_session.md` — operator path after the take exists (doctor first only when starting a *new* packet; never write the fixture)
- `docs/agent_session.md` — agent path when clone fails (reconstruct + selftest)
- `docs/topic_queue.md` — next working titles (not drafts)
- `STATE.md` — current reality
- `NEXT.md` — what the next run should do
- `RUNS.md` — timestamped log
- `ORIGINAL_MASTER_PROMPT.md` — frozen operating prompt
- `docs/channel.md` — working niche lock
- `docs/format.md` — face-free explainer timing and named outputs

## Human session

On the gate machine, place Selected VO first:

```bash
# Follow docs/gate_machine.md. Do not invent a wav in git. Do not git add -f.
python3 tools/narration_adapter.py videos/002-stop-deciding-what-to-work-on-every-morning
```

Parked until that take exists on disk:

```bash
python3 tools/doctor.py
python3 tools/queue_status.py
python3 tools/next_topic.py
```

Those three printers now print the Q1 hold *before* idea_brief/new_packet. Do not treat the first copy-paste they show after the hold as permission to scaffold Q2.

Then follow `docs/human_session.md` steps 5–7. Do not scan the tool list below unless doctor printed a command you do not recognize.

After Q1 ships and a mark-needed folder exists, those printers, `docs/human_session.md`, and `docs/agent_session.md` WAVE 3 name idea_brief — they are not the live job while Q1 is `ready_for_vo`:

```bash
# PARKED until Q1 has on-disk Selected VO
python3 tools/idea_brief.py PATH --block
# paste idea fields by hand into PATH/idea.md
python3 tools/idea_brief.py PATH --check
```

After scaffold on a *future* live packet, `python3 tools/hint.py PATH` prints idea_brief and words.py lines. After a GitHub write of a high-risk tool:

```bash
python3 tools/prove_locks.py
```

After a tool change (agents):

```bash
python3 tools/selftest.py
```

If there is no checkout, reconstruct the minimum tree in `docs/agent_session.md`. Do not retry HTTPS clone after one failure.

## Local tools

Live job first:

```bash
python3 tools/narration_adapter.py videos/002-stop-deciding-what-to-work-on-every-morning
python3 tools/pipeline_status.py videos/002-stop-deciding-what-to-work-on-every-morning
python3 tools/next_action.py videos/002-stop-deciding-what-to-work-on-every-morning
python3 tools/hint.py videos/002-stop-deciding-what-to-work-on-every-morning
```

Parked board / contract examples (not the live job):

```bash
python3 tools/doctor.py
python3 tools/queue_status.py
python3 tools/next_topic.py
python3 tools/mark_topic.py --id Q1
python3 tools/idea_brief.py PATH --block
python3 tools/idea_brief.py PATH --check
python3 tools/hint.py PATH
python3 tools/words.py PATH
python3 tools/prove_locks.py
python3 tools/selftest.py
python3 tools/queue_contract.py
python3 tools/write_path_contract.py
python3 tools/scaffold_contract.py
python3 tools/new_packet.py "Working title here"
python3 tools/new_idea.py "Stop deciding what to work on every morning"
python3 tools/pipeline_status.py
python3 tools/next_action.py
python3 tools/hint.py
python3 tools/validate_packet.py --all
python3 tools/validate_packet.py videos/sample-001-why-systems-beat-motivation
python3 tools/validate_packet.py --duration videos/sample-001-why-systems-beat-motivation
python3 tools/expand_brief.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/expand_prompt.py videos/sample-001-why-systems-beat-motivation
python3 tools/apply_script.py videos/sample-001-why-systems-beat-motivation --from /tmp/new-script.md
python3 tools/set_status.py videos/sample-001-why-systems-beat-motivation --to ready_for_vo
python3 tools/vo_session.py videos/sample-001-why-systems-beat-motivation --dry-run
```

`queue_status.py` is read-only. It classifies each `docs/topic_queue.md` row against `videos/` (ok-queued, mark-needed, missing-folder, ok-used, parked, fixture-refuse). After a mark-needed folder exists it also prints idea_brief --block / paste / --check. It does not write the queue or scaffold packets. While Q1 is `ready_for_vo` it prints the gate_machine hold before those scaffold lines.

`next_topic.py` is read-only. It prints the first unused row in `docs/topic_queue.md`, a predicted `videos/NNN-slug`, and scaffold commands. After that predicted folder exists it also prints idea_brief --block / paste / --check. It does not create packets or WORDS. Numeric ids treat `sample-001-*` as 001. While Q1 is `ready_for_vo` the Q1 hold prints before scaffold copy-paste.

`idea_brief.py` reprints or checks idea.md. `--block` prints the paste block. `--check` validates pasted fields. It does not write idea.md.

`words.py` is a read-only band printer on PATH/draft.md when present. It is not apply --write.

`prove_locks.py` is the first post-write command after a GitHub write of a high-risk tool. PASS is not apply --write.

`mark_topic.py` dry-runs a queue status change. It refuses `used` until a matching non-fixture `videos/` folder exists. `--write` is required to edit `docs/topic_queue.md`. It does not scaffold packets.

`selftest.py` is read-only. It asserts the sample-001 contract (PASS + duration WARN + expand-script + fixture lock + apply/set_status refuse). Runtime PASS recorded 2026-09-09 (Run 026) on a reconstructed tree. It is for agents after tool edits, not a second human start command.

`queue_contract.py`, `write_path_contract.py`, and `scaffold_contract.py` are read-only agent contracts. Queue: classify codes and `--strict` exits. Write-path: apply/set_status gates on a temp tree. Scaffold: new_packet reprints mark_topic dry-run and does not auto-write the queue.

`doctor.py` is read-only. It prints gate, drift, duration WARN, next-action code, and the hint CLI in one block. It does not write files. `--strict` exits 1 on FAIL gate or status drift. Duration WARN is not FAIL.

`hint.py` is read-only. It turns the `next_action.py` code into a copy-paste CLI. It never writes files. `--write` appears only as a commented follow-up after a dry-run line. On `sample-001-*` it prints a fixture lock instead of apply_script --write. After scaffold, fill-idea prints idea_brief; write-script/expand-script print words.py and PATH/draft.md apply lines.

`set_status.py` dry-runs a status change. It refuses promoting `sample-001-*`, skip-ahead, `ready_for_vo` while duration WARN is present, and later statuses without Selected VO / Master export on disk. `--write` is required to change `packet.md`. It does not create media. `pipeline_status.py`, `next_action.py`, `hint.py`, `doctor.py`, `selftest.py`, `next_topic.py`, and `queue_status.py` stay read-only.

`apply_script.py` dry-runs a pasted `script.md` body. It refuses `sample-001-*` and `expand_prompt.py` stdout. `--write` is required to replace `script.md` on a non-fixture packet. `--refresh` then rewrites `expand.md`, `vo_session.md`, and `captions.md`. It does not bump status and does not invent WORDS.

`expand_prompt.py` prints a paste-ready expansion brief from channel + idea + budget + current WORDS. It does not write `script.md`. On `sample-001-*` it prints a fixture lock banner. Refuses `--out script.md`.

`expand_brief.py` writes `expand.md` per-beat Have/Target/Add. It does not rewrite `script.md`.

`next_action.py` is read-only. If spoken WORDS sit outside the format band, the code is `expand-script`, not `record-vo`. fill-idea Why names idea_brief --block / paste / --check.

`validate_packet.py` default publish gate stays structural. Duration misses print `WARN`. Do not pad the sample fixture.

Video packets live in `videos/`. Contract: `docs/production_rules.md`. Format: `docs/format.md`. Operator path: `docs/human_session.md`. Agent reconstruct: `docs/agent_session.md`. Topic list: `docs/topic_queue.md`.
