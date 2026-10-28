2026-10-28T23:15:00Z (Run 873)

Operator and agent entry point. Primary status: `python3 tools/status_report.py` or `python3 tools/next_suggestion.py`.

**Current state**
- Videos published: 0
- Primary blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Issue #1. Do not poll.
- Media: Q1 VO + cards + r253 master ready after materialize; do not rematerialize if present. Do not regenerate.
- New: tools/install_spoken_lines.py generates install_spoken_lines.md with 3-5 calm operational spoken lines for the same-day install segment from idea.md fields only. Reduces drafting labor for the install CTA.
- Preferred unblocked list: complete. Next is the human step or a truly new production capability (not another status/polish/inspection/brief/candidates tool).
