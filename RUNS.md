# RUNS

## Run 1117 — 2026-11-08T14:30:00Z
- Objective: Reduce future human setup labor on the script stage for every subsequent video by providing a grounded outline skeleton from the topic queue without requiring a packet.
- Action: Created tools/queued_outline_starter.py (prints Hook/Payoff/body beats/CTA structure, word targets, mechanism alignment notes grounded in queue data only; no invented scenes/WORDS). No secrets polled, no dispatch. Updated state files.
- Result: Outline starter available. Complements queued_research_starter.py (research) and idea_brief.py --queue (idea). All local gates remain PASS. Videos published stay 0. Pre-upload path unchanged. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch; new tool reduces rediscovery of outline structure for Q2+.
- Verification: File created, syntax checked with py_compile, pushed. Soft only; no hard gates changed.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Research and idea stages already had queue-based starters; script outline was the remaining early-stage gap.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py. For future videos: python3 tools/queued_outline_starter.py --id Q2 (or queued_research_starter.py).

## Run 1115 — 2026-11-08T12:25:00Z
- Objective: Reduce tool-switching and rediscovery on the remaining human OAuth step by providing a single self-contained guide.
- Action: Created tools/oauth_complete_guide.py (deep links + ordered checklist + copy-paste commands + recovery notes + success criteria in one output). Linked from human_starter.py, oauth_step_checklist.py, and docs/HUMAN_PRIORITY.md. No secrets polled, no dispatch. Updated state files.
- Result: Complete guide available. Starter, checklist, and priority doc now point to it. All local gates remain PASS. Videos published stay 0. Pre-upload path unchanged. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch; complete guide reduces rediscovery and tool-switching.
- Verification: File created, syntax checked with py_compile, executable, runs cleanly and prints the expected guide. References inserted and syntax-checked. Soft only; no hard gates changed.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Prior tools (checklist, recovery, starter) existed but required switching between them.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)

Permanent log. Newest first.
