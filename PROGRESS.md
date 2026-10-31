- Run 925 enhancement: shared phrase_utils.extract_sections and count_spoken_words now exist and are used by end_screen_reserve_check, minimum_timeline_estimate, and speaking_time_estimate. Latent false zero-word bug in minimum_timeline_estimate fixed (no longer re-applies spoken_words to section text). Contract extended and PASS. Agents or humans get consistent section boundaries and word counts across duration tools on every future packet. No invented content. Reduces rediscovery and inconsistency labor. Aligns with no-invent rule.
- Small reliability centralization + bug fix only. No packet content writes, no secrets polled. Local contract verification PASS.
- Human labor reduction: lower chance of agents treating diverging or zero word counts as reasons to re-inspect or rewrite; one shared path for section extraction and spoken-word totals.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 924 enhancement: tools/end_screen_reserve_check.py total word count now uses the shared phrase_utils.spoken_words extractor (section counts also use shared normalize). Duration estimates stay consistent with quality_scan, claim_scan, and other scanners. Agents or humans get one less source of silent drift on every future packet. No invented content. Reduces rediscovery and inconsistency labor. Aligns with no-invent rule.
- Small reliability alignment to existing end-screen check only. No packet content writes, no secrets polled. Shared helpers already locked by phrase_utils_contract.py.
- Human labor reduction: lower chance of agents treating a diverging word count as a reason to re-inspect or rewrite; one shared path for spoken-word totals.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.
