# PROGRESS

## 2026-11-02 Run 984
- Added tools/vo_timeline_consistency.py. Read-only comparison of timeline spoken estimate vs actual Selected VO duration (stdlib). Flags large mismatches for future packets. Estimated savings: ~1 minute per packet by surfacing spoken-vs-actual drift early. No credentials or media invent required. Does not extend the readiness aggregator.

## 2026-11-02 Run 983
- Added STALL_READINESS_AGGREGATOR to tools/stall_watch.py. Detects repeated extensions of production_readiness.py while videos published stay 0. Makes the pattern of incremental local QA aggregator fields machine-visible so future runs can avoid it. The aggregator already covers all major pre-upload signals. Estimated savings: reduces low-leverage runs that only add report fields. No credentials or media invent required.

(Older progress notes remain in docs/progress_archive.md.)
