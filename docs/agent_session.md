# Agent session

One page for recurring agents when there is no local git checkout.

Humans follow `docs/human_session.md`. This page is not a second start command for humans.

## Clone

HTTPS clone of this private repo fails in the agent sandbox. Do not retry after the first failure in a run. Push via GitHub file APIs.

## Which contract

After editing a tool, do not scan NEXT for the lock name. Run:

```bash
python3 tools/which_contract.py --after EDITED_FILE.py
```

Then run the printed command if the reconstructed tree has that contract's files. `--run` SKIP means deps were missing, not that the lock passed.

## Reconstruct and prove the fixture

`tools/selftest.py` is the packet contract. Reconstruct only what it imports, plus the sample packet files the publish gate needs.

Minimum tree:

```
tools/selftest.py
tools/validate_packet.py
tools/pipeline_status.py
tools/next_action.py
tools/hint.py
tools/set_status.py
tools/apply_script.py
tools/render_brief.py
tools/caption_brief.py
videos/sample-001-why-systems-beat-motivation/packet.md
videos/sample-001-why-systems-beat-motivation/idea.md
videos/sample-001-why-systems-beat-motivation/script.md
videos/sample-001-why-systems-beat-motivation/titles.md
videos/sample-001-why-systems-beat-motivation/thumbnail.md
videos/sample-001-why-systems-beat-motivation/qa.md
videos/sample-001-why-systems-beat-motivation/assets.md
```

How: list `tools/` and the sample folder with GitHub get_file_contents, then curl each `download_url` into that tree. Do not invent file bodies from memory.

Then:

```bash
python3 tools/selftest.py
```

Expected on current sample-001 (do not pad WORDS to change this):

- Gate PASS
- Status draft
- Code expand-script
- Duration WARN: spoken 153 words (~01:01 at 150 wpm) below explainer-6-10min band 900–1500
- First live command is expand_prompt with no `--write`
- SELFTEST PASS
- Exit 0
- No writes

## Queue board contract

After editing `queue_lib.py`, `queue_status.py`, or `mark_topic.py`, also reconstruct those three files plus `tools/queue_contract.py` and run:

```bash
python3 tools/queue_contract.py
```

Expected: `QUEUE CONTRACT PASS`, exit 0, no writes to `docs/` or `videos/`.

## Write-path contract

After editing `apply_script.py` or `set_status.py`, reconstruct those two plus `validate_packet.py`, `pipeline_status.py`, `caption_brief.py`, `render_brief.py`, and `tools/write_path_contract.py`, then run:

```bash
python3 tools/write_path_contract.py
```

Expected: `WRITE PATH CONTRACT PASS`, exit 0, no writes to `docs/` or `videos/`.

## Scaffold contract

After editing `new_packet.py` or `after_scaffold.py`, reconstruct `new_packet.py`, `queue_lib.py`, `docs/topic_queue.md`, and `tools/scaffold_contract.py` (optional: `after_scaffold.py` for the titles_filled regex check), then run:

```bash
python3 tools/scaffold_contract.py
```

Expected: `SCAFFOLD CONTRACT PASS`, exit 0, no writes to `videos/`, queue status unchanged.

## Last verified runtime

- When: 2026-09-09T12:22:00Z (Run 026)
- How: reconstructed tree at `/tmp/ca` from GitHub download_url tokens at commit `ceecc84`
- Result: SELFTEST PASS, exit 0
- Spoken: 153 words (~01:01)

Queue contract:

- When: 2026-09-09T19:20:00Z (Run 032)
- How: `/tmp/ca/tools` with queue_lib + queue_status + mark_topic + queue_contract
- Result: QUEUE CONTRACT PASS, exit 0

Write-path contract:

- When: 2026-09-09T20:06:00Z (Run 033)
- How: `/tmp/ca/tools` with apply_script + set_status + pipeline_status + validate_packet + caption_brief + render_brief + write_path_contract
- Result: WRITE PATH CONTRACT PASS, exit 0

Scaffold contract:

- When: 2026-09-09T21:12:00Z (Run 034)
- How: `/tmp/ca` with new_packet + queue_lib + docs/topic_queue.md + scaffold_contract
- Result: SCAFFOLD CONTRACT PASS, exit 0

Contract router:

- When: 2026-09-09T22:10:00Z (Run 035)
- How: local `which_contract.py` map and `--after` checks (no videos/ writes)
- Result: map exit 0; `--after new_packet.py` → scaffold_contract; `--after apply_script.py` → write_path_contract

If a later run cannot reconstruct, record FAIL with the missing file. Do not leave runtime as "unverified" after a successful reconstruct.

## Stop

- Do not retry clone after one failure.
- Do not write reconstructed files back onto sample-001.
- Do not invent WORDS, wav, cards, or ffmpeg recipes.
- Do not wrap doctor in start.py.
