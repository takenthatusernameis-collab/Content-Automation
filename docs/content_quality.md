# Content Quality Contract

Goal: specific, original, useful editorial writing. Prefer concrete mechanisms, evidence, and viewer-useful structure over generic AI filler.

## Anti-slop system (single source of truth)

- Canonical high-precision phrases live in `tools/phrase_utils.py` as `ANTI_SLOP_PATTERNS` (word-boundary, case-insensitive matching).
- Shared `phrase_utils.normalize` converts curly apostrophes/quotes and en/em dashes to straight equivalents. Both `quality_scan.py` and `claim_scan.py` call it before matching, so one straight entry covers common variants. Do not re-add curly duplicates or local normalize copies.
- A hit is a revision signal, not an authorship claim. The tool does not rewrite scripts. Default exit is 0 (frozen packets cannot fail the build); `--strict` exits 1 on remaining hits. `set_status.py` refuses `ready_for_vo` while hits remain.
- List expansion is approaching saturation. Prefer structure detectors, claim hygiene, or true capability work over further exact-phrase additions.

## Rules for new or rewritten content

- Do not add fake anecdotes, testimonials, personal mistakes, slang, or unverifiable experience.
- Do not pad word count. Land in the spoken-word band (900–1500 for primary scripts).
- Before promoting a script: run `python3 tools/quality_scan.py` (and related QA tools), then read aloud for repetitive phrasing and cadence.
- Factual claims that matter must have a source or be rewritten qualitatively (see claim_scan tools).
- Prefer whole-word / first-clause shortening from `phrase_utils.shorten` for any generated starters or suggestions.

## Related tools

- `tools/quality_scan.py` — reports hits with context snippets. Uses shared normalize.
- `tools/claim_scan.py` — factual/hedge signals. Uses shared normalize so one hedge entry covers common variants.
- Shared helpers in `phrase_utils.py` (normalize, shorten, ANTI_SLOP_PATTERNS) and `idea_utils.py` keep starters, suggestors, and scanners consistent.

This page is the human-readable overview. The code is the lock.
