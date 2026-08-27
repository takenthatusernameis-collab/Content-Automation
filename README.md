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
python3 tools/validate_packet.py --all
python3 tools/validate_packet.py videos/sample-001-why-systems-beat-motivation
```

`new_idea.py` fills `idea.md` and names script beats. It does not write spoken WORDS. Use `prompts/script_writer.md` for that.

Video packets live in `videos/`. The contract is described in `docs/production_rules.md`.
