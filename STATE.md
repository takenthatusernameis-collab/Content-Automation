# STATE

2026-10-31T23:13:00Z (Run 937)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Aligned tools/captions_estimate_srt.py to shared effective_rate (prefers observed WPM from Selected VO, else 190/140) and extract_sections / count_spoken_words. Removed hardcoded 150 wpm and local extraction. Pre-VO caption timing estimates now stay consistent with speaking-time, end-screen, timeline, and minimum-timeline tools on every future packet. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T20:12:00Z (Run 936)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Extended tools/pre_upload_qa_suite.py to also run title_length_check.py, description_length_check.py, tags_length_check.py, and chapters_suggest.py. One command now covers core media gates plus the recent metadata length and chapter-timestamp aids before the human OAuth step. Reduces sequential tool-running labor on every future packet that has local media. No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

2026-10-31T18:30:00Z (Run 935)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Added tools/chapters_suggest.py: extracts ## sections from draft/script.md, estimates cumulative spoken time via shared effective_rate (observed WPM preferred), and prints ready-to-paste YouTube chapter lines starting at 0:00 with gap and count flags. Reduces recurring manual timestamp arithmetic for description chapters on every future packet. Complements chapters_scan (quality of existing lines). No packet content edits, no secrets polled. Text stays local. STALL_OAUTH_IDLE primary. Prefer human OAuth step or a truly new production capability (not status printer, brief, candidates, sequence printer, suite, suggest, signals, starter, package, or pure confirmation).

(Older state notes remain below or in docs/state_archive.md. Do not paste the archive back.)
