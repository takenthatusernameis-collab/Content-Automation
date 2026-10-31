# PROGRESS

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

- Run 926 enhancement: tools/speaking_time_estimate.py now defaults to 190 wpm for generated VO (from vo_origin) and reports observed duration + WPM when Selected VO exists. Q1 observed 199 wpm (308.4 s). Agents or humans get tighter timeline and end-screen estimates on every future generated packet without manual calculation. No invented content. Reduces rediscovery and mis-planning labor. Aligns with no-invent rule.
- Small reliability calibration of existing duration estimator only. No packet content writes, no secrets polled. Local verification of observed rate on materialized Q1 take.
- Human labor reduction: lower chance of agents over-reserving end-screen time or mis-planning assembly from a 140 wpm assumption that does not match generated speech.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.
