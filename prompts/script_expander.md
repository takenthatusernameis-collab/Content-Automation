# Script expander

Use this when `next_action.py` prints `expand-script` and `expand.md` already has a budget.

Do not use this on `videos/sample-001-*`. That packet is a fixture.

## Fast path

```bash
python3 tools/expand_prompt.py videos/<id>-<slug>
```

Paste stdout into a writer model. The assembler already includes channel, idea, writer contract, budget, and current WORDS.

The command does not write `script.md`. A printed prompt is not a draft.

## After paste-back (human)

```bash
python3 tools/validate_packet.py videos/<id>-<slug>
python3 tools/validate_packet.py --duration videos/<id>-<slug>
python3 tools/expand_brief.py videos/<id>-<slug> --force
python3 tools/vo_session.py videos/<id>-<slug> --force
python3 tools/caption_brief.py videos/<id>-<slug> --force
```

Refresh session/captions only on a real packet after WORDS change.

## Rules

- Keep existing `##` headings.
- Hook stays 20–35 words.
- Grow beats with a worked example or failure mode.
- Land in 900–1500 spoken words for `explainer-6-10min`.
- No invented statistics. No extra beats unless count is under 4.
- Do not autofill WORDS from the budget table.
