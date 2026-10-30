# PROGRESS

- Reusable capability: tools/pipeline_entry_contract.py locks the stage-guide selection logic (scaffold → early, idea → early, draft → script promotion, script/VO → media, upload → after-upload) on tempfile packets. Agents or humans can run the contract to confirm the pointer still works. No invented content. Improves reliability of the stage guide for every future video. Aligns with no-invent rule.
- Small new production tool only. No packet content writes, no secrets polled.
- Human labor reduction: lower risk of broken stage selection; one command verifies the lock.
- Videos published remain 0. Stall continues. Preferred list still complete. Pre-upload path stable. Next high-value action is the human OAuth step or another truly new production capability.

- Reusable capability: tools/pipeline_entry.py inspects packet file presence (idea.md, draft.md, script.md, selected take, upload_state.json) and prints the matching existing sequence-printer command. Agents or humans run one command to enter the correct stage instead of rediscovering which sequence tool applies. No invented content. Reduces stage-selection labor on every future video. Aligns with no-invent rule.
- Small new production tool only. No packet content writes, no secrets polled.
- Human labor reduction: lower time spent selecting the correct anti-rediscovery sequence; one command produces the pointer.
- Videos published remain 0. Stall continues. Preferred list still complete. Pre-upload path stable. Next high-value action is the human OAuth step or another truly new production capability.

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.
