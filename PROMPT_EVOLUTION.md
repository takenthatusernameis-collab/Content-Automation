# PROMPT EVOLUTION

Original prompt is frozen in `ORIGINAL_MASTER_PROMPT.md`.

## Observed issues (Run 018)
- `expand-script` without a beat budget leaves the human doing arithmetic across seven headings.
- Auto-writing WORDS from the budget would invent a draft and break the fixture freeze.
- Hook must stay 20-35 even when the body needs ~1000 more words.

## Observed issues (Run 019)
- A budget without a paste pack still costs a human six file opens per expand pass.
- Printing a full script-shaped prompt is easy to mistake for permission to write sample-001.
- `--out script.md` must hard-refuse.

## Observed issues (Run 020)
- After a writer returns a script, swapping script.md and refreshing expand/vo/captions is still four manual commands.
- apply_script must treat expand_prompt stdout as hostile input.
- Dry-run default prevents a bad paste from landing during agent runs.

## Observed issues (Run 021)
- apply_script correctly leaves status alone, so humans still edit packet.md by hand and create drift.
- Board auto-bump would hide a short fixture. A separate dry-run writer with evidence checks is the safer split.
- `re.sub(rf"\\1 {value}")` can write a literal backslash-1; group replacement must be `r"\\1 " + value`.

## Allowed changes
Recorded as proposals in `NEXT_RUN_PROMPT.md` only. Do not edit the original archive.

Earlier run observations 010-017 remain in prior commits.
