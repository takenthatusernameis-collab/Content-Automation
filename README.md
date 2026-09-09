# Content-Automation

Recurring-agent workspace for a low-labor YouTube production system.

Start here:
- `docs/human_session.md` — operator path (doctor first; never write the fixture)
- `docs/agent_session.md` — agent path when clone fails (reconstruct + selftest)
- `docs/topic_queue.md` — next working titles (not drafts)
- `STATE.md` — current reality
- `NEXT.md` — what the next run should do
- `RUNS.md` — timestamped log
- `ORIGINAL_MASTER_PROMPT.md` — frozen operating prompt
- `docs/channel.md` — working niche lock
- `docs/format.md` — face-free explainer timing and named outputs

## Human session

```bash
python3 tools/doctor.py
python3 tools/next_topic.py
```

Then follow `docs/human_session.md`. Do not scan the tool list below unless doctor printed a command you do not recognize.

After a tool change (agents):

```bash
python3 tools/selftest.py
```

If there is no checkout, reconstruct the minimum tree in `docs/agent_session.md`. Do not retry HTTPS clone after one failure.

## Local tools

```bash
python3 tools/doctor.py
python3 tools/next_topic.py
python3 tools/mark_topic.py --id Q1
python3 tools/selftest.py
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

`next_topic.py` is read-only. It prints the first unused row in `docs/topic_queue.md`, a predicted `videos/NNN-slug`, and scaffold commands. It does not create packets or WORDS. Numeric ids treat `sample-001-*` as 001.

`mark_topic.py` dry-runs a queue status change. It refuses `used` until a matching non-fixture `videos/` folder exists. `--write` is required to edit `docs/topic_queue.md`. It does not scaffold packets.

`selftest.py` is read-only. It asserts the sample-001 contract (PASS + duration WARN + expand-script + fixture lock + apply/set_status refuse). Runtime PASS recorded 2026-09-09 (Run 026) on a reconstructed tree. It is for agents after tool edits, not a second human start command.

`doctor.py` is read-only. It prints gate, drift, duration WARN, next-action code, and the hint CLI in one block. It does not write files. `--strict` exits 1 on FAIL gate or status drift. Duration WARN is not FAIL.

`hint.py` is read-only. It turns the `next_action.py` code into a copy-paste CLI. It never writes files. `--write` appears only as a commented follow-up after a dry-run line. On `sample-001-*` it prints a fixture lock instead of apply_script --write.

`set_status.py` dry-runs a status change. It refuses promoting `sample-001-*`, skip-ahead, `ready_for_vo` while duration WARN is present, and later statuses without Selected VO / Master export on disk. `--write` is required to change `packet.md`. It does not create media. `pipeline_status.py`, `next_action.py`, `hint.py`, `doctor.py`, `selftest.py`, and `next_topic.py` stay read-only.

`apply_script.py` dry-runs a pasted `script.md` body. It refuses `sample-001-*` and `expand_prompt.py` stdout. `--write` is required to replace `script.md` on a non-fixture packet. `--refresh` then rewrites `expand.md`, `vo_session.md`, and `captions.md`. It does not bump status and does not invent WORDS.

`expand_prompt.py` prints a paste-ready expansion brief from channel + idea + budget + current WORDS. It does not write `script.md`. On `sample-001-*` it prints a fixture lock banner. Refuses `--out script.md`.

`expand_brief.py` writes `expand.md` per-beat Have/Target/Add. It does not rewrite `script.md`.

`next_action.py` is read-only. If spoken WORDS sit outside the format band, the code is `expand-script`, not `record-vo`.

`validate_packet.py` default publish gate stays structural. Duration misses print `WARN`. Do not pad the sample fixture.

Video packets live in `videos/`. Contract: `docs/production_rules.md`. Format: `docs/format.md`. Operator path: `docs/human_session.md`. Agent reconstruct: `docs/agent_session.md`. Topic list: `docs/topic_queue.md`.
