# NEXT_RUN_PROMPT

Use the original master prompt unchanged, plus these targeted additions:

## Bootstrap rule
If STATE.md exists, trust it over memory. If the repo only has a README, create the memory files and one reusable production artifact before anything else.

## Scope cap
Ship at most one new reusable capability per run after foundation exists. Prefer extending `tools/` and `videos/_template/` over new top-level concepts.

## Evidence rule
If you add a script, run it against a copy of `videos/sample-001-*` fields (dry-run is enough if write would mutate the fixture) and paste the command output into RUNS.md.
Do not claim `git clone` or `validate_packet.py --all` succeeded unless you actually have a local checkout.

## Niche rule
Do not reopen niche debate unless a human changed DECISIONS.md. Specialize prompts toward `docs/channel.md`.

## Intake vs publish QA
Default `validate_packet.py` is the publish/completeness gate.
`validate_packet.py --draft` (alias `--incomplete`) is the intake gate: empty WORDS/titles/thumb are `DRAFT-INCOMPLETE` (exit 0) unless structure/identity is broken.
Do not weaken hook 20–35 or title-count rules in default mode.
Do not treat a partial hook (1–19 or 36+ words) as draft-incomplete; that is still FAIL.

## Checklist rule
`qa_checklist.py` may mark mechanical boxes from files. It must not mark human VO/card/export boxes done and must not invent numeric quality scores.
Digit notes belong to spoken WORDS only, not headings.

## Fixture freeze
Do not overwrite `videos/sample-001-*` titles or thumbnail unless the packet schema itself changed.
`qa.md` on the fixture may be regenerated when the checklist schema changes; leave human ticks unchecked.

## Private repo
Push via GitHub file APIs. Do not retry HTTPS clone after it fails once in the run.
