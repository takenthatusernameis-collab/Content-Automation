# NEXT_RUN_PROMPT

Use the original master prompt unchanged, plus these targeted additions:

## Bootstrap rule
If STATE.md exists, trust it over memory. If the repo only has a README, create the memory files and one reusable production artifact before anything else.

## Scope cap
Ship at most one new reusable capability per run after foundation exists. Prefer extending `tools/` and `videos/_template/` over new top-level concepts.

## Evidence rule
If you add a script, run it against `videos/sample-001-*` and paste the command output into RUNS.md.

## Niche rule
Do not reopen niche debate unless a human changed DECISIONS.md. Specialize prompts toward the working niche.
