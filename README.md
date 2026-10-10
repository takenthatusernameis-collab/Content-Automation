# Content-Automation

Recurring-agent workspace for a low-labor YouTube production system.

## Live packet (current state)

Packet: `videos/002-stop-deciding-what-to-work-on-every-morning`  
Status: `ready_for_vo` (text complete; generated VO + cards + r253 master exist on private releases and can be materialized).  
Videos published: 0.  
**Remaining human gate: three GitHub Actions secrets** (`YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`).

Run this first on a fresh clone:

```bash
python3 tools/materialize_q1_release.py   # installs verified wav, 7 cards, r253 master; ignores truncated r249
python3 tools/media_qa.py videos/002-stop-deciding-what-to-work-on-every-morning
python3 tools/next_action.py videos/002-stop-deciding-what-to-work-on-every-morning
python3 tools/operator_card.py            # prints the one human OAuth step + pitfalls
```

Do not scaffold Q2. Do not poll secrets. Do not edit brief generators unless `python3 tools/closed_brief_gate.py` fails. Do not rematerialize when vo/, cards/, and export/master.mp4 are already present. Prepend logs only through `python3 tools/record_run.py`.

Start here for context:
- `STATE.md` — current reality
- `NEXT.md` — what the next run should do
- `tools/operator_card.py` — the one human step
- `docs/gate_machine.md` — packet-relative Selected VO drop (generated fallback already authorized for Q1)
- `docs/youtube_integration.md` — upload contract
- `RUNS.md` — timestamped log
- `ORIGINAL_MASTER_PROMPT.md` — frozen operating prompt
- `docs/channel.md` — working niche lock
- `docs/format.md` — face-free explainer timing and named outputs

## Human session

The one remaining human step is the three OAuth secrets. Print it with:

```bash
python3 tools/operator_card.py
```

Then follow the numbered steps it reprints from `tools/oauth_setup.py`. Store the secrets with `gh secret set` (paste into the prompt). Dispatch once:

```bash
gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false
```

Do not run `gh secret list`. Do not commit the token file. After a provider video id exists and `uploaded_at` is at least 7 days old, a later dispatch with `collect_feedback=true` is allowed.

Parked until that publish happens:

```bash
python3 tools/doctor.py
python3 tools/queue_status.py
python3 tools/next_topic.py
```

Those printers still print the Q1 hold before idea_brief/new_packet. Do not treat them as permission to scaffold Q2.


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
