# Script expander

Use this when `next_action.py` prints `expand-script` and `expand.md` already has a budget.

Do not use this on `videos/sample-001-*`. That packet is a fixture.

## Before the paste

If `idea.md` still says `mechanism_clarity: template-default` or the generic line
`A written default that removes one daily decision`, edit problem + mechanism
from the matching `docs/topic_queue.md` `one_line` first. Otherwise every video
expands from the same default and the draft will not match the queued title.

## Fast path

```bash
python3 tools/expand_prompt.py videos/<id>-<slug>
```

Paste stdout into a writer model. The assembler already includes channel, idea, writer contract, budget, and current WORDS.

The command does not write `script.md`. A printed prompt is not a draft.

## After the writer returns a script.md body

```bash
python3 tools/apply_script.py videos/<id>-<slug> --from /tmp/new-script.md
python3 tools/apply_script.py videos/<id>-<slug> --from /tmp/new-script.md --write --refresh
python3 tools/validate_packet.py videos/<id>-<slug>
python3 tools/validate_packet.py --duration videos/<id>-<slug>
```

`apply_script.py` refuses the sample fixture and refuses expand_prompt stdout.
Default is dry-run. `--write` replaces script.md. `--refresh` updates expand.md, vo_session.md, and captions.md.
It does not bump packet status.

## Rules

- Keep existing `##` headings.
- Hook stays 20-35 words.
- Grow beats with a worked example or failure mode.
- Land in 900-1500 spoken words for `explainer-6-10min`.
- No invented statistics. No extra beats unless count is under 4.
- Do not autofill WORDS from the budget table.
