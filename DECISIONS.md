# DECISIONS

Format: date | decision | why | revisit when

- 2026-08-27 | Store system memory in markdown at repo root, not a database | Fast for agents; git is the log | If files become noisy
- 2026-08-27 | One folder per video (`videos/<id>-<slug>/`) with a fixed file contract | Eliminates “where is the script” labor | If format splits (shorts vs long)
- 2026-08-27 | QA is structural first (files + required fields), taste later | Reliability before aesthetics | After first real draft
- 2026-08-27 | No publishing integrations in foundation phase | Missing credentials; would stall the run | When a human adds setup notes + keys elsewhere
- 2026-08-27 | Temporary working niche: focused-work systems explainers | Unblocks template specialization without pretending the channel exists | Human override
- 2026-08-27 | Sample video packet is a fixture, not a publish candidate | Need a validator target | Keep sample-001 frozen unless schema changes
- 2026-08-27 | Idea intake is deterministic structure, not LLM generation | Runs must work with no model/API | If a writer model is later wired, keep structure CLI as fallback
- 2026-08-27 | Working niche lives in `docs/channel.md` | Single place for prompts and tools to read | Human override via DECISIONS.md
