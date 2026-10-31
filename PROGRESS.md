# PROGRESS

- Run 938 enhancement: tools/packet_next_step.py inspects key artifact presence and lightweight quality signals then prints the single highest-leverage next action (exact command) for any packet. Agents or humans get a reusable prioritized next step without sequential inspection of stage tools. No invented content. Reduces decision labor on every future packet. Aligns with no-invent rule.
- Small reusable capability addition. No packet content writes, no secrets polled.
- Human labor reduction: lower chance of agents or humans having to manually assemble the next command from multiple status and stage tools for a given packet.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 937 enhancement: tools/captions_estimate_srt.py now uses shared phrase_utils.effective_rate (prefers observed WPM from Selected VO, else 190/140) and shared extract_sections / count_spoken_words. Removed hardcoded 150 wpm. Agents or humans get estimated caption timings that stay consistent with speaking-time, end-screen, timeline, and minimum-timeline estimates on every future packet without manual rate conversion. No invented content. Reduces remaining divergence labor. Aligns with no-invent rule.
- Small reliability alignment of the pre-VO caption estimate tool to the shared duration rate logic. No packet content writes, no secrets polled.
- Human labor reduction: lower chance of agents treating a divergent 150 wpm estimate SRT as a reason to re-inspect or adjust timings by hand before a real take exists.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

(Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.)
