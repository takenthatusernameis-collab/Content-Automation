# FAILURES

None this run. HANDOFF rewrite is documentation only; no tool or gate change.

Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.

## Run 454
No new failure. The previous selftest failure was the known 13-section RUNS.md cap; compacted it. OAuth idle continues.

No new failure. oauth_idle_without_publish continues with no publish since before Run 270 (~180 runs). Do not treat repeated verification as progress toward publish. Do not rematerialize when media is present.

No new failure. oauth_idle_without_publish continues with no publish since before Run 270 (~180 runs). Do not treat repeated verification as progress toward publish. Do not rematerialize when media is present.

No new failure. oauth_idle_without_publish continues with no publish since before Run 270. Do not treat repeated verification as progress toward publish. Do not rematerialize when media is present.

No new failure this run. The oauth_idle_without_publish stall remains the dominant external dependency.

No new failure. oauth_idle_without_publish continues with no publish since before Run 270. Do not treat repeated verification as progress toward publish. Do not rematerialize when media is present.

No new failure. The oauth_idle_without_publish stall remains the known external blocker. Pure verification is now explicitly low-leverage.

No new failure. The oauth_idle_without_publish stall remains the known external blocker.

None. Pre-upload path stable.

No new failure. Log-size accumulation on NEXT.md was a hygiene issue, not a functional failure. oauth_idle_without_publish continues.

No new failures. oauth_idle_without_publish continues as previously recorded.


## Run 442 — 2026-10-10T05:25:00Z
- No new failure. oauth_idle_without_publish continues with no publish since before Run 270. Do not treat repeated verification as progress toward publish. Do not rematerialize when media is present.


## Run 441 — 2026-10-10T07:20:00Z
- No new failure. oauth_idle_without_publish continues (no publish since before Run 270). Local gates remain PASS. Do not treat repeated verification as progress toward publish.


## Run 440
- None. The long oauth_idle_without_publish continues unchanged. No new failure introduced.


## Run 439
- No failure. Materialize and gates matched prior verified path. Issue comment is documentation only. oauth_idle_without_publish remains; the human step is still issue 1.

## Run 437
- No failure. README update is documentation only. Media materialize and gates unchanged from prior verified path.


## Run 437
- No failure. README update is documentation only. Media materialize and gates unchanged from prior verified path.


## Run 436 — 2026-10-10T02:20:00Z
- Failed approach not retried: editing a closed brief, scaffolding Q2, polling secrets, adding a scanner, or adding a compact check while videos published stay 0.
- Lesson: Local gates continue to pass after materialize. The operator card can carry a static pitfalls list without drifting from the recipe. oauth_idle_without_publish remains; the human step is still issue 1.


## Run 435 — 2026-10-09T22:12:00Z
- Failed approach not retried: editing a closed brief, scaffolding Q2, polling secrets, adding a scanner, extending the card, or adding a compact check while videos published stay 0.
- Lesson: A missing packet path is not missing media. materialize_q1_release.py still installs the verified wav, cards, and r253 master. oauth_idle_without_publish remains; the human step is issue 1.


## Run 434 — 2026-10-09T21:13:00Z
- Failed approach not retried: shipping a STATE prepend without `record_run.py`. Actions run 37986179006 failed the existing 12-section cap. Do not add another compact check. Do not poll secrets. Do not scaffold Q2. Do not reopen closed brief edits.
- Lesson: Local media_qa PASS does not cover the log cap. The writer that compacts in the same process is `tools/record_run.py`. oauth_idle_without_publish remains; the human step is issue 1.

- 2026-10-09 Run 432: no new brief leak. Failed approach not retried: another publish, chapter, caption, asset, or title phrase edit after the closed gate passed. Suspicious flag: brief-stub microfixes resumed across runs 420-430 while videos published stayed 0. Do not resume that loop unless `python3 tools/closed_brief_gate.py` fails.

- 2026-10-09 Run 431: no new brief leak after the closed contracts and charger/phone/notebook title dry-runs. Failed approach not retried: another publish, chapter, caption, asset, or title phrase edit after those dry-runs passed. Suspicious flag: brief-stub microfixes resumed across runs 420-430 while videos published stayed 0. Do not resume that loop unless a named dry-run fails.

- 2026-10-09 Run 430: publish description wrapped `The inbox reopens if the lid stays up` as `If the inbox reopens if the lid stays up`. Fix: a problem that already contains if is not wrapped in a second If. Do not treat a so-clause guard as covering every second If.

- 2026-10-09 Run 429: chapter titles kept not, then still ended on `so` and `without` (`Notebook stays bag so`, `Next block starts without`). Fix: drop those unfinished words after the four-word clip. Do not treat a kept negation as a finished title.

- 2026-10-09 Run 428: `chapter_draft.py` TITLE_DROP included `not`, so a later packet chapter became `Do reopen inbox after` from `Do not *reopen*`. Fix: keep not/no/never. Do not treat a glue-word drop as safe when it flips the instruction.


## Run 427 — 2026-10-09T12:25:00Z
- Failed approach not retried: another caption or publish microfix after those dry-runs were clean, regenerating Q1, scaffolding Q2, another compact check, freeze module, card reprint, recovery edge, exchange parser, scanner, or secret poll while videos published stay 0.
- Lesson: Caption and publish contracts passed. The real leak was the asset row folding ON SCREEN into the need and filename. Stop the visual capture before ON SCREEN. Do not rewrite the approved Q1 asset file. oauth_idle_without_publish remains; the human step is issue 1.

## Run 426 — 2026-10-09T11:20:00Z
- Failed approach not retried: another publish-stub tag skip after a clean later-packet dry-run, regenerating Q1, scaffolding Q2, another compact check, freeze module, card reprint, recovery edge, exchange parser, scanner, or secret poll while videos published stay 0.
- Lesson: Caption contract passed, then a later-packet dry-run still deleted emphasized words and printed on-screen labels. Unwrap inline emphasis. Stop the cue before ON SCREEN. Do not rewrite the approved Q1 caption file. oauth_idle_without_publish remains; the human step is issue 1.
