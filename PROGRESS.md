# PROGRESS

Run 1224: Added recovery hint #7 to tools/oauth_recovery_hints.py documenting Testing-mode 7-day refresh token expiry and its conflict with the 10-day observation window, including exact fix (publish app + re-mint). Surfaces the pitfall for later failed dispatches. Pre-upload path unchanged. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Human OAuth remains highest leverage. Pure confirmation runs have diminishing returns.

Run 1223: Added explicit warning linking Testing-mode 7-day refresh token expiry to the 10-day observation window in tools/post_publish_sequence.py and strengthened the note in tools/human_starter.py. Prevents a common post-publish failure where the token expires before feedback collection. Pre-upload path unchanged. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Human OAuth remains highest leverage. Pure confirmation runs have diminishing returns.

Run 1222: Added Testing-mode 7-day refresh token lifetime warning to tools/human_starter.py (Google Cloud summary and common pitfalls) for consistency with oauth_complete_guide.py and docs/human_oauth_checklist.md. Ensures the common post-setup failure mode is surfaced regardless of which human entry point is used. Pre-upload path unchanged. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Human OAuth remains highest leverage. Pure confirmation runs have diminishing returns.

Run 1221: Added explicit Testing-mode refresh token lifetime warning (7-day expiry) to tools/oauth_complete_guide.py and docs/human_oauth_checklist.md. Recommends publishing OAuth app to Production (or Internal for Workspace) for long-lived tokens. Reduces a common post-setup failure mode on the sole remaining human OAuth step. Pre-upload path unchanged. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Human OAuth remains highest leverage. Pure confirmation runs have diminishing returns.

Run 1220: Pure inspection and state recording of continued STALL_OAUTH_IDLE (1000+ runs, HIGH suspicion, increasingly so with published=0). No new tools. Confirmed pre-upload path reliable and oauth_credential_format_check.py (with whitespace detection) in place. Highlights diminishing returns of successive pure-confirmation runs while human OAuth remains undone. Human OAuth remains highest leverage.

(Older progress notes remain in docs/progress_archive.md.)

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.
