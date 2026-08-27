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
`validate_packet.py` is a publish/draft-completeness gate. Idea intake may create packets that fail hook/title checks. Do not weaken hook rules to make empty packets pass. Add a separate incomplete-draft mode if needed.

## Fixture freeze
Do not overwrite `videos/sample-001-*` unless the packet schema itself changed.

## Private repo
Push via GitHub file APIs. Do not retry HTTPS clone after it fails once in the run.
