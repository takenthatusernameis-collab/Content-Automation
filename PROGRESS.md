# PROGRESS

Run 1221: Added explicit Testing-mode refresh token lifetime warning (7-day expiry) to tools/oauth_complete_guide.py and docs/human_oauth_checklist.md. Recommends publishing OAuth app to Production (or Internal for Workspace) for long-lived tokens. Reduces a common post-setup failure mode on the sole remaining human OAuth step. Pre-upload path unchanged. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Human OAuth remains highest leverage. Pure confirmation runs have diminishing returns.

Run 1220: Pure inspection and state recording of continued STALL_OAUTH_IDLE (1000+ runs, HIGH suspicion, increasingly so with published=0). No new tools. Confirmed pre-upload path reliable and oauth_credential_format_check.py (with whitespace detection) in place. Highlights diminishing returns of successive pure-confirmation runs while human OAuth remains undone. Human OAuth remains highest leverage.

Run 1219: Enhanced tools/oauth_credential_format_check.py to detect and warn on leading/trailing whitespace (stripped for check; values never printed). Reduces another common copy-paste failure on the sole remaining human OAuth step. Pre-upload path unchanged. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Human OAuth remains highest leverage. Pure confirmation runs have diminishing returns.

(Older progress notes remain in docs/progress_archive.md.)

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.
