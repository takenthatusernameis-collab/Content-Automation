# PROGRESS

## 2026-11-03 Run 985
- Added tools/card_timeline_consistency.py. Read-only check (via timeline.plan) of card holds >=1.5s, card presence on disk, and CTA coverage of the 20s end-screen reserve. Complements the VO timing check. Estimated savings: ~1 minute per packet by surfacing visual/hold/reserve drift early. No credentials or media invent required. Does not extend the readiness aggregator.

## 2026-11-02 Run 984
- Added tools/vo_timeline_consistency.py. Read-only comparison of timeline spoken estimate vs actual Selected VO duration (stdlib). Flags large mismatches for future packets. Estimated savings: ~1 minute per packet by surfacing spoken-vs-actual drift early. No credentials or media invent required. Does not extend the readiness aggregator.

(Older progress notes remain in docs/progress_archive.md.)
