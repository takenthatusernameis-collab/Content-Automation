# STATE

2026-11-03T20:15:00Z (Run 1004)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Added tools/post_publish_sequence.py: fail-closed ordered reminder of the full post-video-id path (7-day window, collect_feedback dispatch, experiment baseline check, experiment_loop). Combines and extends the previous next_after_publish and experiment_readiness helpers into one command. Reduces rediscovery after the human OAuth step succeeds. Still no media invent, no ffmpeg execute, no secrets. Pre-upload path remains complete. STALL_OAUTH_IDLE primary. Prefer human OAuth step (docs/human_oauth_checklist.md or python3 tools/human_one_pager.py) or further truly new media/QA capability that does not require credentials. Do not add another consistency printer.

2026-11-03T19:15:00Z (Run 1003)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Added tools/experiment_readiness.py: fail-closed check of experiment_baseline.json presence and completeness (numeric baseline + non-placeholder source). Reduces rediscovery of the experiment setup path after a provider_video_id exists. Still no media invent, no ffmpeg execute, no secrets. Pre-upload path remains complete. STALL_OAUTH_IDLE primary. Prefer human OAuth step (docs/human_oauth_checklist.md or python3 tools/human_one_pager.py) or further truly new media/QA capability that does not require credentials. Do not add another consistency printer.

(Older state notes remain below or in docs/state_archive.md. Do not paste the archive back.)
