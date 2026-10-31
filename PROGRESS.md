# PROGRESS

- Run 935 enhancement: tools/chapters_suggest.py extracts ## sections, estimates cumulative spoken time with effective_rate, and prints ready-to-paste YouTube chapter lines starting at 0:00 with gap and count flags. Agents or humans get suggested timestamps without manual arithmetic on every future packet. No invented content. Reduces recurring chapter-timestamp labor. Aligns with no-invent rule.
- Small reliability addition of a chapters generation aid complementary to existing chapters_scan. No packet content writes, no secrets polled.
- Human labor reduction: lower chance of agents or humans spending time calculating and formatting chapter timestamps by hand before adding them to descriptions.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 934 enhancement: tools/tags_length_check.py reports tag count, per-tag lengths, and estimated YouTube-counted total characters (join by commas + 2 for each multi-word tag's quotes) against the 500 hard limit. Agents or humans get an immediate length signal without manual counting of the combined tag string on every future packet. No invented content. Reduces recurring tags-review labor. Aligns with no-invent rule.
- Small reliability addition of a length quality check complementary to existing tags_scan. No packet content writes, no secrets polled.
- Human labor reduction: lower chance of shipping tag lists that exceed the 500-character budget or require manual recounting before publish.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 933 enhancement: tools/description_length_check.py reports total character count and first-line visible length against YouTube best practices (first ~150 chars pre-"show more"; hard max 5000). Agents or humans get an immediate length signal without manual counting on every future packet. No invented content. Reduces recurring description-review labor. Aligns with no-invent rule.
- Small reliability addition of a length quality check complementary to existing description_scan. No packet content writes, no secrets polled.
- Human labor reduction: lower chance of shipping descriptions whose key hook is truncated by "show more" or that hit the hard character limit.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 932 enhancement: tools/title_length_check.py reports character counts and flags titles outside the 40-70 ideal band (YouTube search truncates ~60). Agents or humans get an immediate length signal without manual counting on every future packet. No invented content. Reduces recurring title-review labor. Aligns with no-invent rule.
- Small reliability addition of a length quality check complementary to existing title_scan. No packet content writes, no secrets polled.
- Human labor reduction: lower chance of shipping titles that truncate poorly in search or underperform on CTR due to length.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 931 enhancement: tools/timeline.py now uses shared phrase_utils.effective_rate (prefers observed WPM from Selected VO, else 190/140) and shared extract_sections / count_spoken_words. Removed hardcoded 150 wpm. Agents or humans get cut lists whose hold timings stay consistent with speaking-time and end-screen estimates on every future packet without manual rate conversion. No invented content. Reduces remaining divergence labor. Aligns with no-invent rule.
- Small reliability alignment of the core cut-list planner to the shared duration rate logic. No packet content writes, no secrets polled.
- Human labor reduction: lower chance of agents treating a divergent 150 wpm timeline as a reason to re-inspect or adjust card holds and end-screen reserve by hand.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 930 enhancement: tools/end_screen_reserve_check.py now prints the estimated absolute start time of the last-20 s end-screen reserve (total estimated duration minus 20 s) using effective_rate. docs/format.md clock source now names effective_rate as the preferred observed path. Agents or humans get the concrete reserve-begin timestamp without manual arithmetic on every future packet. No invented content. Reduces remaining planning labor. Aligns with no-invent rule.
- Small reliability extension of the shared duration rate logic into an actionable planning number. No packet content writes, no secrets polled.
- Human labor reduction: lower chance of agents mis-calculating where the end-screen window starts relative to the spoken timeline.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 929 enhancement: tools/phrase_utils.py now provides effective_rate (prefers observed WPM from Selected VO within sanity bounds, else select_rate). speaking_time_estimate.py, end_screen_reserve_check.py, and minimum_timeline_estimate.py call it. Agents or humans get automatically calibrated duration estimates on any packet that already has a take, without manual rate conversion or override. No invented content. Reduces remaining calibration labor. Aligns with no-invent rule.
- Small reliability extension of the shared duration rate logic. No packet content writes, no secrets polled.
- Human labor reduction: once a Selected VO exists, duration planning tools no longer need a human or agent to notice the observed rate and re-run or adjust estimates by hand.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 928 enhancement: tools/phrase_utils.py now owns select_rate + HUMAN_WPM/GENERATED_WPM constants. speaking_time_estimate.py, end_screen_reserve_check.py, and minimum_timeline_estimate.py import and call it instead of local copies. Agents or humans get permanently consistent duration estimates across speaking-time, end-screen, and minimum-timeline tools on every future generated packet without risk of re-divergence. No invented content. Reduces rediscovery and inconsistent planning labor. Aligns with no-invent rule.
- Small reliability extraction of existing duration rate logic only. No packet content writes, no secrets polled.
- Human labor reduction: lower chance of agents treating divergent rate assumptions as reasons to re-inspect or adjust reserves by hand.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 927 enhancement: tools/end_screen_reserve_check.py and tools/minimum_timeline_estimate.py now select rate from vo_origin.md (190 wpm generated, 140 wpm human) identically to speaking_time_estimate.py. Agents or humans get consistent duration estimates across speaking-time, end-screen, and minimum-timeline tools on every future generated packet without manual rate conversion. No invented content. Reduces rediscovery and inconsistent planning labor. Aligns with no-invent rule.
- Small reliability alignment of existing duration estimators only. No packet content writes, no secrets polled.
- Human labor reduction: lower chance of agents treating divergent 150 wpm vs 190 wpm estimates as reasons to re-inspect or adjust reserves by hand.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.
