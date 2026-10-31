- Run 926 enhancement: tools/speaking_time_estimate.py now defaults to 190 wpm for generated VO (from vo_origin) and reports observed duration + WPM when Selected VO exists. Q1 observed 199 wpm (308.4 s). Agents or humans get tighter timeline and end-screen estimates on every future generated packet without manual calculation. No invented content. Reduces rediscovery and mis-planning labor. Aligns with no-invent rule.
- Small reliability calibration of existing duration estimator only. No packet content writes, no secrets polled. Local verification of observed rate on materialized Q1 take.
- Human labor reduction: lower chance of agents over-reserving end-screen time or mis-planning assembly from a 140 wpm assumption that does not match generated speech.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 925 enhancement: shared phrase_utils.extract_sections and count_spoken_words now exist and are used by end_screen_reserve_check, minimum_timeline_estimate, and speaking_time_estimate. Latent false zero-word bug in minimum_timeline_estimate fixed (no longer re-applies spoken_words to section text). Contract extended and PASS. Agents or humans get consistent section boundaries and word counts across duration tools on every future packet. No invented content. Reduces rediscovery and inconsistency labor. Aligns with no-invent rule.
- Small reliability centralization + bug fix only. No packet content writes, no secrets polled. Local contract verification PASS.
- Human labor reduction: lower chance of agents treating diverging or zero word counts as reasons to re-inspect or rewrite; one shared path for section extraction and spoken-word totals.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.
