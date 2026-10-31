- Run 924 enhancement: tools/end_screen_reserve_check.py total word count now uses the shared phrase_utils.spoken_words extractor (section counts also use shared normalize). Duration estimates stay consistent with quality_scan, claim_scan, and other scanners. Agents or humans get one less source of silent drift on every future packet. No invented content. Reduces rediscovery and inconsistency labor. Aligns with no-invent rule.
- Small reliability alignment to existing end-screen check only. No packet content writes, no secrets polled. Shared helpers already locked by phrase_utils_contract.py.
- Human labor reduction: lower chance of agents treating a diverging word count as a reason to re-inspect or rewrite; one shared path for spoken-word totals.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 923 enhancement: tools/end_screen_reserve_check.py no longer reports 0 words / false SHORT on valid scripts. count_words now counts already-extracted spoken section text instead of re-applying spoken_words. Verified on Q1: 941 total words, CTA 20.0s, overall PASS; pre_upload_qa_suite fully PASS. Agents or humans get accurate CTA/total duration estimates without false revision signals. No invented content. Reduces noise and unnecessary revision labor on every future packet. Aligns with no-invent rule.
- Small reliability fix to existing end-screen check only. No packet content writes, no secrets polled. Local materialize + fixed tool + suite PASS confirmed.
- Human labor reduction: lower chance of agents or humans treating a false SHORT as a reason to rewrite a good CTA; one check now reports real numbers.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.
