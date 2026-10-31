# STATE

2026-10-31T20:12:00Z (Run 936)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Extended tools/pre_upload_qa_suite.py to also run title_length_check.py, description_length_check.py, tags_length_check.py, and chapters_suggest.py. One command now covers core media gates plus the recent metadata length and chapter-timestamp aids before the human OAuth step. Reduces sequential tool-running labor on every future packet that has local media. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T18:30:00Z (Run 935)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Added tools/chapters_suggest.py: extracts ## sections from draft/script.md, estimates cumulative spoken time via shared effective_rate (observed WPM preferred), and prints ready-to-paste YouTube chapter lines starting at 0:00 with gap and count flags. Reduces recurring manual timestamp arithmetic for description chapters on every future packet. Complements chapters_scan (quality of existing lines). No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T17:15:00Z (Run 934)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Added tools/tags_length_check.py: reports tag count, per-tag lengths, and estimated YouTube-counted total characters (tags joined by commas + 2 for each multi-word tag's quotes) against the 500 hard limit. Reduces recurring manual length review for tags before publish on every future packet. Complements tags_scan (quality patterns). No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T16:15:00Z (Run 933)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Added tools/description_length_check.py: reports total character count and first-line visible length against YouTube best practices (first ~150 chars pre-"show more" for search/CTR; hard max 5000). Reduces recurring manual length review for descriptions before publish on every future packet. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T16:17:00Z (Run 932)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Added tools/title_length_check.py: reports character counts and flags titles outside the 40-70 ideal band (YouTube search truncates ~60). Reduces recurring manual length review before publish on every future packet. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T13:25:00Z (Run 931)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Aligned tools/timeline.py to the shared effective_rate (prefers observed WPM from Selected VO, else 190/140). Replaced hardcoded 150 wpm and local extract/word-count with phrase_utils helpers. Cut lists now stay consistent with speaking-time and end-screen estimates on every future packet. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T12:23:00Z (Run 930)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Enhanced tools/end_screen_reserve_check.py to print the estimated absolute start time of the last-20s end-screen reserve (total_duration - 20s) using the shared effective_rate. Updated docs/format.md clock-source note to prefer observed WPM via effective_rate when a Selected VO exists. Makes end-screen planning more precise without manual arithmetic. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T11:21:00Z (Run 929)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Added effective_rate / observed_wpm to tools/phrase_utils.py. Duration tools (speaking_time_estimate.py, end_screen_reserve_check.py, minimum_timeline_estimate.py) now call effective_rate so they automatically prefer the real observed WPM from a Selected VO when present (sanity-bounded), falling back to the 190/140 select_rate otherwise. Eliminates remaining manual rate override labor once a take exists. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T10:17:00Z (Run 928)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Extracted the generated/human WPM rate selection (190/140) into a shared select_rate helper in tools/phrase_utils.py and updated speaking_time_estimate.py, end_screen_reserve_check.py, and minimum_timeline_estimate.py to use it. Eliminates remaining local duplication so future duration tools cannot diverge. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T09:17:00Z (Run 927)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Aligned tools/end_screen_reserve_check.py and tools/minimum_timeline_estimate.py to the same rate logic as speaking_time_estimate.py (190 wpm when vo_origin marks generated, 140 wpm otherwise). Reduces future divergent duration estimates across planning tools for generated narration packets. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

(Older state notes remain below or in docs/state_archive.md. Do not paste the archive back.)
