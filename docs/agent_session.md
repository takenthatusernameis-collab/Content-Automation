# Agent session

One page for recurring agents when there is no local git checkout.

Humans follow `docs/human_session.md`. This page is not a second start command for humans.

## Clone

HTTPS clone of this private repo fails in the agent sandbox. Do not retry after the first failure in a run. Push via GitHub file APIs.

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

## Last verified runtime

- When: 2026-09-09T12:22:00Z (Run 026)
- How: reconstructed tree at `/tmp/ca` from GitHub download_url tokens at commit `ceecc84`
- Result: SELFTEST PASS, exit 0
- Spoken: 153 words (~01:01)

Queue contract:

- When: 2026-09-09T19:20:00Z (Run 032)
- How: `/tmp/ca/tools` with queue_lib + queue_status + mark_topic + queue_contract
- Result: QUEUE CONTRACT PASS, exit 0

If a later run cannot reconstruct, record FAIL with the missing file. Do not leave runtime as "unverified" after a successful reconstruct.

## Stop

- Do not retry clone after one failure.
- Do not write reconstructed files back onto sample-001.
- Do not invent WORDS, wav, cards, or ffmpeg recipes.
- Do not wrap doctor in start.py.
