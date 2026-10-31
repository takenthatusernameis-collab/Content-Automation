# STATE

2026-10-31T11:21:00Z (Run 929)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Added effective_rate / observed_wpm to tools/phrase_utils.py. Duration tools (speaking_time_estimate.py, end_screen_reserve_check.py, minimum_timeline_estimate.py) now call effective_rate so they automatically prefer the real observed WPM from a Selected VO when present (sanity-bounded), falling back to the 190/140 select_rate otherwise. Eliminates remaining manual rate override labor once a take exists. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T10:17:00Z (Run 928)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Extracted the generated/human WPM rate selection (190/140) into a shared select_rate helper in tools/phrase_utils.py and updated speaking_time_estimate.py, end_screen_reserve_check.py, and minimum_timeline_estimate.py to use it. Eliminates remaining local duplication so future duration tools cannot diverge. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T09:17:00Z (Run 927)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Aligned tools/end_screen_reserve_check.py and tools/minimum_timeline_estimate.py to the same rate logic as speaking_time_estimate.py (190 wpm when vo_origin marks generated, 140 wpm otherwise). Reduces future divergent duration estimates across planning tools for generated narration packets. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T08:20:00Z (Run 926)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Enhanced tools/speaking_time_estimate.py to use a 190 wpm default when vo_origin marks generated, and to report observed duration + WPM whenever a packet-relative Selected VO exists (Q1 observed 199 wpm on 308.4s take). Reduces future timeline/end-screen misestimation for generated narration. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

(Older state notes remain below or in docs/state_archive.md. Do not paste the archive back.)
