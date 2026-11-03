# PROGRESS

## 2026-11-03 Run 986
- Added tools/caption_timeline_consistency.py. Read-only check (via timeline.plan + SRT parse) of caption start lag, end overrun vs spoken estimate, and uncovered timeline sections. Complements the VO and card timing checks. Estimated savings: ~1 minute per packet by surfacing caption/timeline drift early. No credentials or media invent required. Does not extend the readiness aggregator.

## 2026-11-03 Run 985
- Added tools/card_timeline_consistency.py. Read-only check (via timeline.plan) of card holds >=1.5s, card presence on disk, and CTA coverage of the 20s end-screen reserve. Complements the VO timing check. Estimated savings: ~1 minute per packet by surfacing visual/hold/reserve drift early. No credentials or media invent required. Does not extend the readiness aggregator.

(Older progress notes remain in docs/progress_archive.md.)
