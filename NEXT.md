# NEXT

Updated: 2026-10-30T04:00:00Z (Run 899)

Run 899: added tools/media_pipeline_steps.py (grounded sequence from ready_for_vo through media QA and publish readiness; no invent, no write). Preferred list complete. Next: human step (docs/human_oauth_checklist.md quick sequence or python3 tools/human_next_action.py / operator_card.py / oauth_exchange.py then secrets + single execute=true dispatch). Optional: python3 tools/media_pipeline_steps.py videos/NNN-... (after ready_for_vo). Or python3 tools/early_pipeline_steps.py (after scaffold). Or python3 tools/script_promotion_steps.py (after a draft). Or python3 tools/next_packet_prep.py (after Q1 ships). Do not refresh banner solely for timestamp. Upload blocked on secrets. Media: do not rematerialize if present. Logs via record_run.py. Do not scaffold Q2. Do not poll secrets. STALL_OAUTH_IDLE primary blocker. Prefer human OAuth step or a truly new production capability (not another status/polish/inspection/suggest-contract, brief, or candidates tool). Avoid additional status printers, briefs, or candidates generators.

Older next actions live in `docs/next_archive.md`. Do not paste the archive back.
