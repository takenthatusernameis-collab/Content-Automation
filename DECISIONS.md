# DECISIONS

Format: date | decision | why | revisit when

- 2026-08-28 | apply_script.py dry-runs by default and never writes sample-001 | Recurring paste-back labor should be one gated command; writing the fixture would destroy the QA target | If a human wants an explicit fixture-overwrite flag (do not add one without evidence)
- 2026-08-28 | apply_script refuses expand_prompt stdout | A printed pack looks like a draft and must not land as WORDS | If prompt framing changes, update PROMPT_MARKERS
- 2026-08-28 | apply_script --refresh may overwrite expand/vo_session/captions after a successful write | Derived files go stale the moment WORDS change | If a human-edited captions.md should always win, require a second flag
- 2026-08-28 | apply_script does not bump packet status | Status drift is a human decision; auto-ready_for_vo would hide a short script | When a promote CLI exists with an explicit flag
- 2026-08-28 | expand_prompt.py prints a paste pack and never writes script.md | Recurring “open six files to brief a writer” labor should be one command | If a human wants an in-repo rewriter with an explicit non-fixture flag
- 2026-08-28 | Spoken duration is WARN on the default gate, FAIL only with `--duration` | sample-001 is a short fixture | When a second real packet exists and the fixture is no longer the board target
- 2026-08-28 | next_action routes `expand-script` before `record-vo` when duration WARN is present | Recording a 1-minute take for an 8-minute format is wasted labor | If a packet format other than explainer-6-10min is added
- 2026-08-27 | Store system memory in markdown at repo root, not a database | Fast for agents; git is the log | If files become noisy
- 2026-08-27 | One folder per video with a fixed file contract | Eliminates “where is the script” labor | If format splits
- 2026-08-27 | No publishing integrations in foundation phase | Missing credentials | When a human adds setup notes + keys elsewhere
- 2026-08-27 | Sample video packet is a fixture, not a publish candidate | Need a validator target | Keep sample-001 frozen unless schema changes

Earlier empty-only scaffold and read-only board decisions remain in force.
