# PROGRESS

## 2026-11-03 Run 987
- Added tools/section_pacing_consistency.py. Read-only check (via timeline.plan) of hook duration (8-12s), CTA-is-last, beat count (4-7), and overall spoken band (6-10 min). Complements the VO, card, and caption timing checks. Estimated savings: ~1 minute per packet by surfacing format pacing drift early. No credentials or media invent required. Does not extend the readiness aggregator.

## 2026-11-03 Run 986
- Added tools/caption_timeline_consistency.py. Read-only check (via timeline.plan + SRT parse) of caption start lag, end overrun vs spoken estimate, and uncovered timeline sections. Complements the VO and card timing checks. Estimated savings: ~1 minute per packet by surfacing caption/timeline drift early. No credentials or media invent required. Does not extend the readiness aggregator.

(Older progress notes remain in docs/progress_archive.md.)
