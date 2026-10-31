- Run 923 enhancement: tools/end_screen_reserve_check.py no longer reports 0 words / false SHORT on valid scripts. count_words now counts already-extracted spoken section text instead of re-applying spoken_words. Verified on Q1: 941 total words, CTA 20.0s, overall PASS; pre_upload_qa_suite fully PASS. Agents or humans get accurate CTA/total duration estimates without false revision signals. No invented content. Reduces noise and unnecessary revision labor on every future packet. Aligns with no-invent rule.
- Small reliability fix to existing end-screen check only. No packet content writes, no secrets polled. Local materialize + fixed tool + suite PASS confirmed.
- Human labor reduction: lower chance of agents or humans treating a false SHORT as a reason to rewrite a good CTA; one check now reports real numbers.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 922 enhancement: tools/next_compact.py now treats "Run N:" notes as compactable items and uses MAX_ITEMS=6 so that long status notes archive automatically. NEXT.md stays under the size cap; SELFTEST and next_compact_contract pass. Agents or humans get the newest locks without truncated fetches. No invented content. Reduces rediscovery and truncation labor on every future run. Aligns with no-invent rule.
- Small reliability fix to the state-compaction tool only. No packet content writes, no secrets polled. Local compact + contracts PASS confirmed.
- Human labor reduction: lower chance of agents missing recent locks due to truncated NEXT.md or failing selftest; one compact keeps the file usable.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.
