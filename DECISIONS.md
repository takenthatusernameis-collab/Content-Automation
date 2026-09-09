# DECISIONS

Format: date | decision | why | revisit when

- 2026-09-09 | Human operator path lives in `docs/human_session.md`, not a second start.py | Doctor already prints the next command; another wrapper would add lookup without new evidence | If a human never finds the markdown and asks for a printed checklist from a tool
- 2026-09-08 | doctor.py is read-only and composes board + next_action + hint | Four oversight commands at session start recreate lookup labor | If a second format needs a different health block
- 2026-09-08 | doctor --strict fails only on FAIL gate or drift, not duration WARN | Sample fixture must stay a non-failing health target | When a second real packet exists and the fixture is no longer the board target
- 2026-08-28 | hint.py is read-only and prints dry-run CLI first | next_action sentences still leave humans hunting among 21 tools | If a second format needs different commands
- 2026-08-28 | hint.py must not print --write as the first command | A default write line would land on sample-001 during hurried paste | Keep commented follow-up only
- 2026-08-28 | set_status.py is the only writer of packet.md status; board tools stay read-only | Hand edits cause drift that next_action then has to unwind | If a human wants a --force skip flag (do not add without evidence)
- 2026-08-28 | set_status dry-runs by default and refuses sample-001 promote | The fixture is the QA target; promoting it hides duration WARN | Keep frozen unless schema changes
- 2026-08-28 | set_status refuses ready_for_vo / ready_for_edit while duration WARN is present | Recording a 1-minute take for an 8-minute format is wasted labor | If a second format is added in DECISIONS.md
- 2026-08-28 | apply_script.py dry-runs by default and never writes sample-001 | Recurring paste-back labor should be one gated command; writing the fixture would destroy the QA target | If a human wants an explicit fixture-overwrite flag (do not add one without evidence)
- 2026-08-28 | apply_script refuses expand_prompt stdout | A printed pack looks like a draft and must not land as WORDS | If prompt framing changes, update PROMPT_MARKERS
- 2026-08-28 | apply_script --refresh may overwrite expand/vo_session/captions after a successful write | Derived files go stale the moment WORDS change | If a human-edited captions.md should always win, require a second flag
- 2026-08-28 | apply_script does not bump packet status | Status drift is a human decision; auto-ready_for_vo would hide a short script | set_status now exists with an explicit --write
- 2026-08-28 | expand_prompt.py prints a paste pack and never writes script.md | Recurring “open six files to brief a writer” labor should be one command | If a human wants an in-repo rewriter with an explicit non-fixture flag
- 2026-08-28 | Spoken duration is WARN on the default gate, FAIL only with `--duration` | sample-001 is a short fixture | When a second real packet exists and the fixture is no longer the board target
- 2026-08-28 | next_action routes `expand-script` before `record-vo` when duration WARN is present | Recording a 1-minute take for an 8-minute format is wasted labor | If a packet format other than explainer-6-10min is added
- 2026-08-27 | Store system memory in markdown at repo root, not a database | Fast for agents; git is the log | If files become noisy
- 2026-08-27 | One folder per video with a fixed file contract | Eliminates “where is the script” labor | If format splits
- 2026-08-27 | No publishing integrations in foundation phase | Missing credentials | When a human adds setup notes + keys elsewhere
- 2026-08-27 | Sample video packet is a fixture, not a publish candidate | Need a validator target | Keep sample-001 frozen unless schema changes

Earlier empty-only scaffold and read-only board decisions remain in force.
