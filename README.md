# Content-Automation

Recurring-agent workspace for a low-labor YouTube production system.

Start here:
- `STATE.md` — current reality
- `NEXT.md` — what the next run should do
- `RUNS.md` — timestamped log
- `ORIGINAL_MASTER_PROMPT.md` — frozen operating prompt

## Local tools

```bash
python3 tools/new_packet.py "Working title here"
python3 tools/validate_packet.py --all
python3 tools/validate_packet.py videos/sample-001-why-systems-beat-motivation
```

Video packets live in `videos/`. The contract is described in `docs/production_rules.md`.
