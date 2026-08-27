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
python3 tools/title_thumb_brief.py videos/002-stop-deciding-what-to-work-on-every --dry-run
python3 tools/title_thumb_brief.py videos/002-stop-deciding-what-to-work-on-every
python3 tools/research_brief.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/research_brief.py videos/002-stop-deciding-what-to-work-on-every
python3 tools/research_brief.py videos/002-stop-deciding-what-to-work-on-every --source "Human pointer: cite X before using a number"
python3 tools/qa_checklist.py videos/sample-001-why-systems-beat-motivation --dry-run
python3 tools/qa_checklist.py videos/sample-001-why-systems-beat-motivation
python3 tools/validate_packet.py --all
python3 tools/validate_packet.py --draft videos/002-stop-deciding-what-to-work-on-every
python3 tools/validate_packet.py videos/sample-001-why-systems-beat-motivation
```

`new_idea.py` fills `idea.md` and names script beats. It does not write spoken WORDS. Use `prompts/script_writer.md` for that. After intake, `--draft` should be `DRAFT-INCOMPLETE` (structure ok, WORDS empty), not `FAIL`. Default scaffold writes titles/thumbs when empty, then `research.md`, then `qa.md` via `tools/after_scaffold.py`. Pass `--no-generate` to leave the template copies untouched.

`title_thumb_brief.py` writes five-plus titles and a ≤5-word on-image line from idea/packet fields. Heuristic only. Will not overwrite filled titles unless `--force`. Scaffold calls the same writer.

`research_brief.py` writes `research.md`: source slots, claims to avoid, and a WORDS-only digit scan. It does not fetch URLs. Will not overwrite a filled research file unless `--force`.

`qa_checklist.py` rewrites `qa.md`: mechanical boxes from packet files, human ticks from `docs/editor.md`. It does not score taste or mark VO/cards done.

Default `validate_packet.py` is the publish/completeness gate. `--draft` / `--incomplete` is the intake gate.

Video packets live in `videos/`. The contract is described in `docs/production_rules.md`. Editor naming is in `docs/editor.md`.
