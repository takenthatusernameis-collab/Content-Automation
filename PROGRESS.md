# PROGRESS

- Reusable capability: tools/captions_estimate_srt.py produces a local captions_estimate.srt with short readable cues (preferring sentence boundaries, ~12 words max) and estimated sequential timings at 150 wpm, extracted only from script.md WORDS blocks. Agents or humans run one command to get a usable estimated SRT for review or local player preview instead of manually drafting initial caption cues and timings on every packet before Selected VO exists. No invented content. SRT stays gitignored. Reduces early-captions-planning labor on every future video.
- Small new production tool only. No packet content writes, no secrets polled.
- Human labor reduction: lower time spent manually splitting spoken text into on-screen cues and estimating start times; one SRT file replaces manual cue drafting for the common case.
- Videos published remain 0. Stall continues. Preferred list still complete. Pre-upload path stable. Next high-value action is the human OAuth step or another truly new production capability.

# PROGRESS

- Reusable capability: tools/review_pack.py produces a local review_pack.md consolidating the idea excerpt, presence status of the five draft files, and short excerpts from any existing chapters/description/metadata/publish/visual drafts, plus a review checklist. Agents or humans run one command to get a single reviewable pack instead of opening multiple draft files on every packet. No invented content. Text stays gitignored. Reduces cross-referencing labor on every future video.
- Small new production tool only. No packet content writes, no secrets polled.
- Human labor reduction: lower time spent opening and comparing the individual draft files before copying useful parts into packet.md / assets.md / publish.md; one text file replaces multi-file review for the common case.
- Videos published remain 0. Stall continues. Preferred list still complete. Pre-upload path stable. Next high-value action is the human OAuth step or another truly new production capability.

# PROGRESS

- Reusable capability: tools/drafts_all.py orchestrates the five existing local text-draft generators (chapters_from_script, full_description_draft, metadata_pack, publish_md_draft, visual_plan_draft) in one command and reports which succeeded. Agents or humans run one command to get the full set of paste-ready drafts instead of invoking each tool separately on every packet. No invented content. Outputs stay gitignored. Reduces multi-tool invocation labor on every future video.
- Small new production tool only. No packet content writes, no secrets polled.
- Human labor reduction: lower time spent remembering and running the individual draft tools; one command replaces five separate invocations for the common case.
- Videos published remain 0. Stall continues. Preferred list still complete. Pre-upload path stable. Next high-value action is the human OAuth step or another truly new production capability.
