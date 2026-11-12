## Run 1217 — 2026-11-12T21:20:00Z
Evidence: Inspected after Run 1216 (format checker added). Pre-upload path remains reliable. STALL_OAUTH_IDLE continues at 1000+ runs with published=0 and no human progress. Pure verification and state recording have low compounding effect at this duration. Lesson: after extreme stall (1000+ runs), treat further pure inspection/recording as low-leverage; agents should flag HIGH suspicion explicitly and prefer the human OAuth step or any remaining unblocked production capability. Do not add another consistency printer, aggregator, or contract lock while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 1163 — 2026-11-10T14:30:00Z
Evidence: Inspected after Run 1162. contracts_suite.py remains UNIFIED RESULT: PASS (92/92) by prior confirmation. STALL_OAUTH_IDLE continues at 1000+ runs with published=0 and no human progress. Pure verification and state recording have low compounding effect at this duration. Lesson: after extreme stall (1000+ runs), treat further pure inspection/recording as low-leverage; agents should flag HIGH suspicion explicitly and prefer the human OAuth step or any remaining unblocked production capability. Do not add another consistency printer, aggregator, or contract lock while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 1162 — 2026-11-10T13:32:00Z
Evidence: Inspected after Run 1161 entry-point fix. contracts_suite.py remains UNIFIED RESULT: PASS (92/92). STALL_OAUTH_IDLE continues at 1000+ runs with published=0 and no human progress. Pure verification and state recording have low compounding effect at this duration. Lesson: after extreme stall (1000+ runs), treat further pure inspection/recording as low-leverage; agents should flag HIGH suspicion explicitly and prefer the human OAuth step or any remaining unblocked production capability. Do not add another consistency printer, aggregator, or contract lock while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 1137 — 2026-11-09T10:20:00Z
Evidence: Inspected after Run 1136 status_report parser fix. contracts_suite.py remains UNIFIED RESULT: PASS (90/90). STALL_OAUTH_IDLE continues at 1000+ runs with published=0 and no human progress. Pure verification and state recording have low compounding effect at this duration. Lesson: after extreme stall (1000+ runs), treat further pure inspection/recording as low-leverage; agents should flag HIGH suspicion explicitly and prefer the human OAuth step or any remaining unblocked production capability. Do not add another consistency printer, aggregator, or contract lock while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 1108 — 2026-11-08T05:16:31Z
Evidence: Fresh-clone materialize + media_qa PASS + selftest PASS reconfirmed. Added experiment_decision.template.json (pairs with baseline template) to reduce post-publish human error. STALL_OAUTH_IDLE continues at 1000+ runs with published=0 and no human progress. Pure verification runs remain low-leverage. Lesson: continue treating extreme stall as HIGH suspicion; agents should prefer the human OAuth step over further pure state recording unless a genuine regression or new unblocked capability is identified. Small reusable templates for the post-publish phase are acceptable when they reduce future human labor. Do not add another consistency printer, aggregator, or contract lock while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 1085 — 2026-11-07T06:25:00Z
Evidence: Fresh-clone materialize + media_qa PASS reconfirmed (VO + 7 cards + r253). STALL_OAUTH_IDLE continues at 1000+ runs with published=0 and no human progress. Pure verification runs remain low-leverage. Lesson: continue treating extreme stall as HIGH suspicion; agents should prefer the human OAuth step over further pure state recording unless a genuine regression or new unblocked capability is identified. Do not add another consistency printer, aggregator, or contract lock while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

# PROMPT EVOLUTION

## Run 1084 — 2026-11-07T05:20:00Z
Evidence: Runs 1081-1083 (and 1000+ prior) each recorded the same STALL_OAUTH_IDLE with published=0 and pre-upload complete, updating state files without new capabilities while the human OAuth step remained undone. Pure verification and state recording have zero compounding effect at this duration. Lesson: after extreme stall (1000+ runs), treat further pure inspection/recording as low-leverage; agents should flag HIGH suspicion explicitly and prefer any remaining unblocked production capability or stop at the human step. Do not add another consistency printer, aggregator, or contract lock while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 1051 — 2026-11-05T20:20:00Z
Evidence: Runs 1044-1050 each added a new *contract.py locking a fail-closed path of an existing tool (timeline, youtube_feedback, complete, youtube_upload, assemble, experiment_loop, media_qa) while videos published stayed 0 and STALL_OAUTH_IDLE continued. The reliability locks are useful but the streak is saturating. Lesson: added tools/contract_streak_detector.py to make the pattern machine-visible (threshold 5). Prefer the human OAuth step or a true new production capability over further pure contract locks. Do not add another consistency printer, aggregator, or contract lock while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 1028 — 2026-11-04T20:13:00Z
Evidence: Runs 1024-1027 successively added and aggregated soft pre-upload checks (length, format, sections, end-screen) while videos published stayed 0 and STALL_OAUTH_IDLE continued. The aggregator is now mature. Adding another soft check would be low-leverage activity. Lesson: soft advisory aggregation has reached practical completeness for pre-upload rediscovery reduction; further printers have diminishing returns. Prefer the human OAuth step or a true post-publish/experiment capability that does not invent data. Do not add another consistency printer while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 1027 — 2026-11-04T19:15:00Z
Evidence: Run 1026 integrated a new soft sections check into the aggregator. Integrating an existing soft end-screen reserve check into the same aggregator further reduces sequential rediscovery without new hard gates or pure consistency printers. Lesson: continue preferring small reusable soft structural checks that fit the aggregator, or true media/QA capability, over additional standalone printers. Prefer human OAuth step while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 1026 — 2026-11-04T18:15:00Z
Evidence: Run 1025 aggregated soft length/format tools. Adding a soft sections-presence check and integrating it into the same aggregator further reduces sequential rediscovery without new hard gates or pure consistency printers. Lesson: continue preferring small reusable soft structural checks that fit the aggregator, or true media/QA capability, over additional standalone printers. Prefer human OAuth step while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 1025 — 2026-11-04T17:20:00Z
Evidence: Runs 1023-1024 added individual soft length match tools while OAuth stall continued. Aggregating them into one soft_pre_upload_report.py reduces command surface without new hard gates or another pure consistency printer. Lesson: when soft advisory tools accumulate, prefer a single aggregator over more individual printers. Prefer human OAuth step or true media/QA capability. Do not add another consistency printer while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 996 — 2026-11-03T12:30:00Z
Evidence: Runs 992-995 each added a small read-only consistency or tags-hygiene printer (cta_end_screen_consistency, chapters_description_consistency, title_publish_consistency, tags_hygiene) while videos published stayed 0 and the OAuth stall continued. Prose notes mentioned saturation risk but did not stop the next printer. Lesson: strengthen the stall_watch detector for this pattern; prefer the human OAuth step or a true production capability that advances a packet toward completion. Do not add another consistency printer while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 983 — 2026-11-02T21:13:00Z
Evidence: Runs 976-982 each extended tools/production_readiness.py with additional local QA signals (thumbnail size, VO duration, card counts, script presence, timeline estimates, caption CPS, metadata limits) while videos published stayed 0 and the OAuth stall continued. The aggregator now covers media_qa + assemble + captions presence/CPS + thumbnail + VO + cards + script + timeline + publish/timeline + metadata limits. Lesson: incremental report-field additions to the readiness aggregator are approaching saturation (similar to prior brief/candidates/sequence-printer patterns); strengthen the stall_watch detector and prefer the human OAuth step or a true production capability that advances a packet toward completion. Do not further extend production_readiness.py while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

Keep ORIGINAL_MASTER_PROMPT.md archival and unchanged.

## Evidence-based additions (do not silently rewrite the master)

(Older evolution notes remain below or in archive if present.)
