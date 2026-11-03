# PROGRESS

## 2026-11-03 Run 991
- Added tools/title_thumbnail_consistency.py. Read-only check that thumbnail On-image text is short and shares significant words with the primary title. Surfaces visual/metadata drift early. Estimated savings: ~1 minute per packet. No credentials or media invent required. Does not extend the readiness aggregator.

# PROGRESS

## 2026-11-03 Run 990
- Added tools/timeline_continuity_check.py. Read-only check (via timeline.plan) of continuous sequential coverage (no gaps/overlaps), sum of section durations equals spoken estimate, and export equals spoken + 20s end-screen reserve. Complements the order, pacing, and budget checks. Estimated savings: ~1 minute per packet by surfacing continuity/arithmetic drift early. No credentials or media invent required. Does not extend the readiness aggregator.

## 2026-11-03 Run 989
- Added tools/section_budget_consistency.py. Read-only check (via phrase_utils.extract_sections + count_spoken_words) of section spoken-word counts against locked format bands (hook 20-35, payoff 40-70, beats 140-220, CTA 40-80). Complements the duration-based pacing and order checks. Estimated savings: ~1 minute per packet by surfacing word-budget drift early. No credentials or media invent required. Does not extend the readiness aggregator.

(Older progress notes remain in docs/progress_archive.md.)
