# Content Quality Contract

Goal: specific, original, useful editorial writing. Prefer concrete mechanisms, evidence, and viewer-useful structure over generic AI filler.

## Anti-slop system (single source of truth)

- Canonical high-precision phrases live in `tools/phrase_utils.py` as `ANTI_SLOP_PATTERNS` (word-boundary, case-insensitive matching).
- Shared `phrase_utils.normalize` converts curly apostrophes/quotes and en/em dashes to straight equivalents. Both `quality_scan.py` and `claim_scan.py` call it before matching, so one straight entry covers common variants. Do not re-add curly duplicates or local normalize copies.
- Shared `phrase_utils.spoken_words` extracts and normalizes WORDS blocks. quality_scan, claim_scan, and cadence_repetition_scan use it instead of local WORD_RE + spoken copies.
- Shared `phrase_utils.context_snippet` produces the short actionable context around matches. quality_scan, claim_scan, title_scan, and thumbnail_scan use it instead of local window logic.
- A hit is a revision signal, not an authorship claim. The tool does not rewrite scripts. Default exit is 0 (frozen packets cannot fail the build); `--strict` exits 1 on remaining hits. `set_status.py` refuses `ready_for_vo` while hits remain.
- List expansion is approaching saturation. Prefer structure detectors, claim hygiene, or true capability work over further exact-phrase additions.

## Claim hygiene (single source of truth)

- Canonical high-precision hedge phrases live in `tools/phrase_utils.py` as `HEDGE_PATTERNS` (word-boundary, case-insensitive matching). Extracted from claim_scan for DRY consistency with the anti-slop list.
- claim_scan normalizes input and uses shared context_snippet and spoken_words. Digits and hedges require a non-placeholder source citation.
- Do not maintain a local hedge list or spoken extractor in claim_scan.

## Title / thumbnail / chapter weak patterns (single source of truth)

- Canonical high-precision weak/clickbait patterns live in `tools/phrase_utils.py` as `TITLE_WEAK_PATTERNS`, `THUMBNAIL_WEAK_PATTERNS`, and `CHAPTER_WEAK_PATTERNS` (word-boundary, case-insensitive matching). Extracted for DRY consistency.
- title_scan, thumbnail_scan, and chapters_scan normalize input (curly apostrophes/quotes/dashes) before matching so one straight entry covers common variants. Do not re-add curly duplicates or local pattern lists.
- These scanners also use shared context_snippet where applicable.

## Description / end-screen / first-comment patterns (single source of truth)

- description_scan uses the full shared `ANTI_SLOP_PATTERNS` plus `DESCRIPTION_EXTRA_PATTERNS` (don't forget to, leave a comment, let me know). Both live in phrase_utils.py.
- Canonical high-precision weak/engagement-bait patterns for end-screen/CTA live in `phrase_utils.END_SCREEN_WEAK_PATTERNS`.
- Canonical high-precision engagement-bait/reply-prompt patterns for first comment live in `phrase_utils.FIRST_COMMENT_BAIT_PATTERNS`.
- description_scan, end_screen_scan, and first_comment_scan normalize input and use shared context_snippet. Do not re-add local pattern lists, curly duplicates, or window logic.
- These cover publish.md sections. A hit remains a revision signal only.

## Rules for new or rewritten content

- Do not add fake anecdotes, testimonials, personal mistakes, slang, or unverifiable experience.
- Do not pad word count. Land in the spoken-word band (900–1500 for primary scripts).
- Before promoting a script: run `python3 tools/quality_scan.py` (and related QA tools), then read aloud for repetitive phrasing and cadence.
- Factual claims that matter must have a source or be rewritten qualitatively (see claim_scan tools).
- Prefer whole-word / first-clause shortening from `phrase_utils.shorten` for any generated starters or suggestions.

## Related tools

- `tools/quality_scan.py` — reports hits with context snippets. Uses shared spoken_words, normalize, context_snippet, and ANTI_SLOP_PATTERNS.
- `tools/claim_scan.py` — factual/hedge signals. Uses shared spoken_words, normalize, context_snippet, and HEDGE_PATTERNS so one hedge entry covers common variants.
- `tools/cadence_repetition_scan.py` — cadence and repetition signals. Uses shared spoken_words.
- `tools/title_scan.py` — shouted titles, weak patterns, thumbnail mismatch. Uses shared context_snippet, normalize, and TITLE_WEAK_PATTERNS.
- `tools/thumbnail_scan.py` — weak/clickbait/long thumbnail text. Uses shared context_snippet, normalize, and THUMBNAIL_WEAK_PATTERNS.
- `tools/chapters_scan.py` — chapter structure and weak titles. Uses shared normalize and CHAPTER_WEAK_PATTERNS.
- `tools/description_scan.py` — anti-slop in Description. Uses shared ANTI_SLOP_PATTERNS + DESCRIPTION_EXTRA_PATTERNS, normalize, and context_snippet.
- `tools/end_screen_scan.py` — weak/engagement-bait end-screen/CTA. Uses shared END_SCREEN_WEAK_PATTERNS, normalize, and context_snippet.
- `tools/first_comment_scan.py` — engagement-bait in First comment. Uses shared FIRST_COMMENT_BAIT_PATTERNS, normalize, and context_snippet.
- Shared helpers in `phrase_utils.py` (normalize, shorten, context_snippet, spoken_words, ANTI_SLOP_PATTERNS, HEDGE_PATTERNS, TITLE_WEAK_PATTERNS, THUMBNAIL_WEAK_PATTERNS, CHAPTER_WEAK_PATTERNS, DESCRIPTION_EXTRA_PATTERNS, END_SCREEN_WEAK_PATTERNS, FIRST_COMMENT_BAIT_PATTERNS) and `idea_utils.py` keep starters, suggestors, and scanners consistent.

This page is the human-readable overview. The code is the lock.
