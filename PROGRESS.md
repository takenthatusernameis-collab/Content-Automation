# PROGRESS

- Reusable capability: tools/drafts_all.py orchestrates the five existing local text-draft generators (chapters_from_script, full_description_draft, metadata_pack, publish_md_draft, visual_plan_draft) in one command and reports which succeeded. Agents or humans run one command to get the full set of paste-ready drafts instead of invoking each tool separately on every packet. No invented content. Outputs stay gitignored. Reduces multi-tool invocation labor on every future video.
- Small new production tool only. No packet content writes, no secrets polled.
- Human labor reduction: lower time spent remembering and running the individual draft tools; one command replaces five separate invocations for the common case.
- Videos published remain 0. Stall continues. Preferred list still complete. Pre-upload path stable. Next high-value action is the human OAuth step or another truly new production capability.

# PROGRESS

- Reusable capability: tools/visual_plan_draft.py produces a local visual_plan_draft.md with section-tied estimated start times (at 150 wpm), suggested short card texts, and b-roll/card-file slots from script.md ## sections + spoken text. Agents or humans run one command to get a paste-ready visual plan instead of manually extracting sections and inventing card texts on every packet. No invented content. Text stays gitignored. Reduces visual-planning labor on every future video.
- Small new production tool only. No packet content writes, no secrets polled.
- Human labor reduction: lower time spent planning section visuals and short card texts for assets.md or editor notes; one text file replaces manual section extraction and card phrasing for the common case.
- Videos published remain 0. Stall continues. Preferred list still complete. Pre-upload path stable. Next high-value action is the human OAuth step or another truly new production capability.

# PROGRESS

- Reusable capability: tools/publish_md_draft.py produces a local publish_draft.md with a title candidate, operational description (summary from early spoken sections + cumulative chapters estimate at 150 wpm), tags, and CTA candidate from idea.md plus (when script.md present) script structure. Agents or humans run one command to get a paste-ready full publish draft instead of manually assembling from multiple suggestors for Studio or publish.md on every packet. No invented content. Text stays gitignored. Reduces publish-assembly labor on every future video.
- Small new production tool only. No packet content writes, no secrets polled.
- Human labor reduction: lower time spent collecting and formatting title, description, tags, and CTA into a publish.md; one text file replaces multiple tool runs and manual copy-paste for the common case.
- Videos published remain 0. Stall continues. Preferred list still complete. Pre-upload path stable. Next high-value action is the human OAuth step or another truly new production capability.
