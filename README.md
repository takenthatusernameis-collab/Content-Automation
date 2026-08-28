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
python3 tools/new_idea.py "Topic" --no-generate
python3 tools/pipeline_status.py
python3 tools/pipeline_status.py videos/sample-001-why-systems-beat-motivation
python3 tools/pipeline_status.py --strict
python3 tools/next_action.py
python3 tools/next_action.py videos/sample-001-why-systems-beat-motivation
python3 tools/validate_packet.py --all
python3 tools/validate_packet.py videos/sample-001-why-systems-beat-motivation
python3 tools/validate_packet.py --duration videos/sample-001-why-systems-beat-motivation
python3 tools/expand_brief.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/vo_session.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/render_brief.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/asset_brief.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/caption_brief.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/publish_brief.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/qa_checklist.py videos/sample-001-why-systems-beat-motivation --dry-run
```

`pipeline_status.py` is a read-only board: declared status, validate gate, render presence, and status drift. It writes nothing and creates no media. `--strict` exits 1 on FAIL or drift. Duration WARN is not FAIL.

`next_action.py` is a read-only next-step list from the same inspect data. It writes nothing, does not bump status, and does not create media. If spoken WORDS sit outside the format band, the code is `expand-script`, not `record-vo`.

`validate_packet.py` default publish gate stays structural. Duration misses print `WARN`. `--duration` promotes that WARN to FAIL. Do not pad the sample fixture to clear it.

`expand_brief.py` writes `expand.md`: per-beat Have/Target/Add against the 900–1500 band. It does not rewrite `script.md`. Will not overwrite a filled expand file unless `--force`.

`vo_session.py` writes `vo_session.md`: a reading card from script WORDS plus the named selected-take path. It does not run TTS or write wav/flac. Will not overwrite a filled session file unless `--force`.

`new_idea.py` fills `idea.md` and names script beats. It does not write spoken WORDS. Default scaffold writes titles/thumbs when empty, then `publish.md`, `captions.md`, `assets.md`, `render.md`, `vo_session.md`, `expand.md`, `research.md`, then `qa.md` via `tools/after_scaffold.py`. Pass `--no-generate` to leave the template copies untouched.

`render_brief.py` writes `render.md`: exists vs missing for named VO/card/export paths. It does not run ffmpeg or create media. Will not overwrite a filled render file unless `--force`.

`asset_brief.py` writes `assets.md`: planned cards from script VISUAL lines. It does not download stock or write PNGs. Will not overwrite a filled assets file unless `--force`.

`caption_brief.py` writes `captions.md` from WORDS at 150 wpm. Not Whisper / SRT.
`publish_brief.py` writes description/tags/first comment. Not YouTube.
`qa_checklist.py` rewrites `qa.md` mechanical boxes from files. It does not mark VO/cards done.

Video packets live in `videos/`. Contract: `docs/production_rules.md`. Format: `docs/format.md`. Editor: `docs/editor.md`. VO: `docs/narration.md`. Cards: `docs/assets.md`.
