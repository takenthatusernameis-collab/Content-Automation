# DECISIONS

Format: date | decision | why | revisit when

- 2026-08-27 | Store system memory in markdown at repo root, not a database | Fast for agents; git is the log | If files become noisy
- 2026-08-27 | One folder per video (`videos/<id>-<slug>/`) with a fixed file contract | Eliminates "where is the script" labor | If format splits (shorts vs long)
- 2026-08-27 | QA is structural first (files + required fields), taste later | Reliability before aesthetics | After first real draft
- 2026-08-27 | No publishing integrations in foundation phase | Missing credentials; would stall the run | When a human adds setup notes + keys elsewhere
- 2026-08-27 | Temporary working niche: focused-work systems explainers | Unblocks template specialization without pretending the channel exists | Human override
- 2026-08-27 | Sample video packet is a fixture, not a publish candidate | Need a validator target | Keep sample-001 frozen unless schema changes
- 2026-08-28 | pipeline_status.py is read-only; it never writes packet status | Recurring “where is this video” labor should be one command; auto-bump would hide missing VO | When a human wants a promote CLI with an explicit flag
- 2026-08-28 | next_action.py is read-only; one recommended step from inspect data | Recurring “which OPEN box first” labor should not require ranking seven checkboxes | When a human wants a promote CLI with an explicit flag
- 2026-08-28 | vo_session.md is a reading card from WORDS, not a take | Recurring “what do I read and where do I save it” labor should not require opening script + narration docs | When a selected wav exists; then refresh with `--force`
- 2026-08-28 | Scaffold writes vo_session.md only when empty | Same empty-only contract as render | If a human-edited session card should always win
- 2026-08-28 | Spoken duration is WARN on the default gate, FAIL only with `--duration` | sample-001 is a short fixture; making 900 words required would break PASS and `--strict` | When a second real packet exists and the fixture is no longer the board target
- 2026-08-28 | next_action routes `expand-script` before `record-vo` when duration WARN is present | Recording a 1-minute take for an 8-minute format is wasted labor | If a packet format other than explainer-6-10min is added

Earlier 2026-08-27/28 decisions (empty-only scaffold, captions, assets, render, format lock) remain in force; see prior commits if a line was trimmed here.
