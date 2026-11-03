# PROGRESS

## 2026-11-03 Run 989
- Added tools/section_budget_consistency.py. Read-only check (via phrase_utils.extract_sections + count_spoken_words) of section spoken-word counts against locked format bands (hook 20-35, payoff 40-70, beats 140-220, CTA 40-80). Complements the duration-based pacing and order checks. Estimated savings: ~1 minute per packet by surfacing word-budget drift early. No credentials or media invent required. Does not extend the readiness aggregator.

## 2026-11-03 Run 988
- Added tools/structure_order_consistency.py. Read-only check (via timeline.plan classification) of section order (hook first, payoff before any numbered beat, sequential beats, CTA last). Complements the pacing and VO/card/caption timing checks. Estimated savings: ~1 minute per packet by surfacing structural order drift early. No credentials or media invent required. Does not extend the readiness aggregator.

(Older progress notes remain in docs/progress_archive.md.)
