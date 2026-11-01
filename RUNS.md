# RUNS
## Run 944 — 2026-11-01T06:15:00Z
- Objective: Reduce recurring labor of crafting concise on-card install language by integrating short idea.md mechanism text directly into the card generator for CTA/install cards.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Updated tools/card_generator.py to call idea_utils.extract + phrase_utils.shorten for CTA or install-related text-cards when idea.md exists; fallback to existing need-based title. No secrets polled, no dispatch, no media committed, no packet writes.
- Result: Videos published stay 0. Card generation now automatically prefers short, mechanism-aligned install text for relevant cards on every future packet. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Code committed and importable; uses shared shorten and idea_extract helpers. No file writes. Existing non-CTA cards unchanged.
- Discovery: Suggestor tools improve consistency only when humans remember to run them; baking the short-text preference into the generator compounds the gain across all future packets without extra steps.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

## Run 943 — 2026-11-01T05:13:00Z
- Objective: Reduce recurring labor of crafting concise on-card text for the same-day install default by adding a reusable suggester grounded in idea.md.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Added tools/install_card_suggest.py which extracts mechanism/problem, applies phrase_utils.shorten, and prints 2-3 short candidate phrases for cards or end-cards. No secrets polled, no dispatch, no media committed, no packet writes.
- Result: Videos published stay 0. New tool available for every future packet to generate preferred short install language for better visual consistency with the channel promise. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Code committed and importable; uses shared shorten and idea_extract helpers. No file writes.
- Discovery: Channel promise language for cards was previously manual or scattered across other generators; a dedicated short-text helper improves consistency without invention.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)
