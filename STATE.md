# STATE

2026-11-13T03:17:11Z (Run 1223)

Inspected after Run 1222. Pre-upload path remains reliable. Added explicit warning in tools/post_publish_sequence.py and strengthened it in tools/human_starter.py that Testing-mode 7-day refresh tokens expire before the 10-day observation window, so the app must be published to Production (or Internal) and a long-lived token minted before collect_feedback. Prevents a common silent failure after the first publish. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion, increasingly so with published=0 and no human progress). Pure inspection/recording has low compounding value at this extreme duration. Next remains the human OAuth step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, use improved format checker and token-lifetime note including window conflict, then secrets + single execute=true). Do not poll secrets, no dispatch, no live packet writes. Prefer human progress; successive pure-confirmation runs are flagged as low-leverage.



2026-11-13T02:16:00Z (Run 1222)

Inspected after Run 1221. Pre-upload path remains reliable. Added Testing-mode 7-day refresh token lifetime warning to the Google Cloud setup summary and common pitfalls in tools/human_starter.py for consistency with oauth_complete_guide.py and docs/human_oauth_checklist.md. Reduces residual human friction on the sole remaining OAuth step. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion, increasingly so with published=0 and no human progress). Pure inspection/recording has low compounding value at this extreme duration. Next remains the human OAuth step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, use improved format checker and token-lifetime note, then secrets + single execute=true). Do not poll secrets, no dispatch, no live packet writes. Prefer human progress; successive pure-confirmation runs are flagged as low-leverage.

2026-11-13T01:22:00Z (Run 1221)

Inspected after Run 1220. Pre-upload path remains reliable. Added explicit warning in tools/oauth_complete_guide.py and docs/human_oauth_checklist.md about Testing-mode OAuth apps issuing 7-day refresh tokens; recommend publishing to Production (or Internal for Workspace) for long-lived tokens. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion, increasingly so with published=0 and no human progress). Pure inspection/recording has low compounding value at this extreme duration. Next remains the human OAuth step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, use improved format checker and token-lifetime note, then secrets + single execute=true). Do not poll secrets, no dispatch, no live packet writes. Prefer human progress; successive pure-confirmation runs are flagged as low-leverage.

2026-11-13T00:23:09Z (Run 1220)

Inspected after Run 1219. Pre-upload path remains reliable. oauth_credential_format_check.py includes whitespace detection. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion, increasingly so with published=0 and no human progress). Pure inspection/recording has low compounding value at this extreme duration. Next remains the human OAuth step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, use improved format checker, then secrets + single execute=true). Do not poll secrets, no dispatch, no live packet writes. Prefer human progress; successive pure-confirmation runs are flagged as low-leverage.

(Older state notes remain below or in docs/state_archive.md. Do not paste the archive back.)
