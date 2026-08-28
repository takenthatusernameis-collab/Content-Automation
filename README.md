# Content-Automation

Recurring-agent workspace for a low-labor YouTube production system.

Start here:
- `STATE.md` — current reality
- `NEXT.md` — what the next run should do
- `RUNS.md` — timestamped log
- `ORIGINAL_MASTER_PROMPT.md` — frozen operating prompt
- `docs/channel.md` — working niche lock
- `docs/format.md` — face-free explainer timing and named outputs

## Local tools

```bash
python3 tools/new_packet.py "Working title here"
python3 tools/new_idea.py "Stop deciding what to work on every morning"
python3 tools/pipeline_status.py
python3 tools/next_action.py
python3 tools/validate_packet.py --all
python3 tools/validate_packet.py videos/sample-001-why-systems-beat-motivation
python3 tools/validate_packet.py --duration videos/sample-001-why-systems-beat-motivation
python3 tools/expand_brief.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/expand_prompt.py videos/sample-001-why-systems-beat-motivation
python3 tools/apply_script.py videos/sample-001-why-systems-beat-motivation --from /tmp/new-script.md
python3 tools/set_status.py videos/sample-001-why-systems-beat-motivation --to ready_for_vo
python3 tools/vo_session.py videos/sample-001-why-systems-beat-motivation --dry-run
```

`set_status.py` dry-runs a status change. It refuses promoting `sample-001-*`, skip-ahead, `ready_for_vo` while duration WARN is present, and later statuses without Selected VO / Master export on disk. `--write` is required to change `packet.md`. It does not create media. `pipeline_status.py` and `next_action.py` stay read-only.

`apply_script.py` dry-runs a pasted `script.md` body. It refuses `sample-001-*` and `expand_prompt.py` stdout. `--write` is required to replace `script.md` on a non-fixture packet. `--refresh` then rewrites `expand.md`, `vo_session.md`, and `captions.md`. It does not bump status and does not invent WORDS.

`expand_prompt.py` prints a paste-ready expansion brief from channel + idea + budget + current WORDS. It does not write `script.md`. On `sample-001-*` it prints a fixture lock banner. Refuses `--out script.md`.

`expand_brief.py` writes `expand.md` per-beat Have/Target/Add. It does not rewrite `script.md`.

`next_action.py` is read-only. If spoken WORDS sit outside the format band, the code is `expand-script`, not `record-vo`.

`validate_packet.py` default publish gate stays structural. Duration misses print `WARN`. Do not pad the sample fixture.

Video packets live in `videos/`. Contract: `docs/production_rules.md`. Format: `docs/format.md`.
