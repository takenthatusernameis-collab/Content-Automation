# Content-Automation

Recurring-agent workspace for a low-labor YouTube production system.

Start here:
- `STATE.md` — current reality
- `NEXT.md` — what the next run should do
- `RUNS.md` — timestamped log
- `ORIGINAL_MASTER_PROMPT.md` — frozen operating prompt
- `docs/channel.md` — working niche lock

## Local tools

```bash
python3 tools/new_packet.py "Working title here"
python3 tools/new_idea.py "Stop deciding what to work on every morning"
python3 tools/new_idea.py "Topic" --no-generate
python3 tools/asset_brief.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/caption_brief.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/publish_brief.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/qa_checklist.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/validate_packet.py --all
python3 tools/validate_packet.py videos/sample-001-why-systems-beat-motivation
```

`new_idea.py` fills `idea.md` and names script beats. It does not write spoken WORDS. Default scaffold writes titles/thumbs when empty, then `publish.md`, `captions.md`, `assets.md`, `research.md`, then `qa.md` via `tools/after_scaffold.py`. Pass `--no-generate` to leave the template copies untouched.

`asset_brief.py` writes `assets.md`: planned cards from script VISUAL lines. It does not download stock or write PNGs. Will not overwrite a filled assets file unless `--force`.

`caption_brief.py` writes `captions.md` from WORDS at 150 wpm. Not Whisper / SRT.
`publish_brief.py` writes description/tags/first comment. Not YouTube.
`qa_checklist.py` rewrites `qa.md` mechanical boxes from files. It does not mark VO/cards done.

Video packets live in `videos/`. Contract: `docs/production_rules.md`. Editor: `docs/editor.md`. VO: `docs/narration.md`. Cards: `docs/assets.md`.
