# PROGRESS

- Reusable capability: tools/pre_upload_review_steps.py lists the exact local review commands (media_qa, caption_gate, export_probe, end_screen_reserve_check, thumbnail inspect, publish readiness / youtube_upload dry-run) to run before the human OAuth step and single execute=true dispatch. Agents or humans run one command to obtain the final pre-upload checklist instead of rediscovering the order. No invented content. Reduces sequential labor on every future video. Aligns with no-invent rule.
- Small new production tool only. No packet content writes, no secrets polled.
- Human labor reduction: lower time spent selecting the correct final review sequence before dispatch; one command produces the pointer.
- Videos published remain 0. Stall continues. Preferred list still complete. Pre-upload path stable. Next high-value action is the human OAuth step or another truly new production capability.

- Reusable capability: tools/pipeline_entry_contract.py locks the stage-guide selection logic (scaffold → early, idea → early, draft → script promotion, script/VO → media, upload → after-upload) on tempfile packets. Agents or humans can run the contract to confirm the pointer still works. No invented content. Improves reliability of the stage guide for every future video. Aligns with no-invent rule.
- Small new production tool only. No packet content writes, no secrets polled.
- Human labor reduction: lower risk of broken stage selection; one command verifies the lock.
- Videos published remain 0. Stall continues. Preferred list still complete. Pre-upload path stable. Next high-value action is the human OAuth step or another truly new production capability.

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.
