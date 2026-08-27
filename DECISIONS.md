# DECISIONS

Format: date | decision | why | revisit when

- 2026-08-27 | Store system memory in markdown at repo root, not a database | Fast for agents; git is the log | If files become noisy
- 2026-08-27 | One folder per video (`videos/<id>-<slug>/`) with a fixed file contract | Eliminates "where is the script" labor | If format splits (shorts vs long)
- 2026-08-27 | QA is structural first (files + required fields), taste later | Reliability before aesthetics | After first real draft
- 2026-08-27 | No publishing integrations in foundation phase | Missing credentials; would stall the run | When a human adds setup notes + keys elsewhere
- 2026-08-27 | Temporary working niche: focused-work systems explainers | Unblocks template specialization without pretending the channel exists | Human override
- 2026-08-27 | Sample video packet is a fixture, not a publish candidate | Need a validator target | Keep sample-001 frozen unless schema changes
- 2026-08-27 | Idea intake is deterministic structure, not LLM generation | Runs must work with no model/API | If a writer model is later wired, keep structure CLI as fallback
- 2026-08-27 | Working niche lives in `docs/channel.md` | Single place for prompts and tools to read | Human override via DECISIONS.md
- 2026-08-27 | Title/thumb briefs are heuristic banks keyed off idea words, not an LLM | Same no-API constraint as intake; must pass validator field rules | If copy quality is the bottleneck after scripts exist
- 2026-08-27 | Packet QA has two gates: default publish completeness, `--draft` intake | Empty WORDS must not pass publish QA and must not block intake | If a third status (ready_for_vo) needs its own gate
- 2026-08-27 | Packet field values are single-line | Empty `id:` was swallowing the next line via `\\s*` | Keep one-line parsers
- 2026-08-27 | qa.md is generated, not scored | Mechanical boxes come from files; human ticks stay human | If a later run can detect VO files or export paths on disk
- 2026-08-27 | research.md is a stub + reminder, never a scrape dump | Unverified URLs look like facts if pasted in | When a human verification checklist exists
- 2026-08-27 | Scaffold writes qa.md + research.md by default | A second command after every new folder is recurring labor | If generate-on-scaffold becomes too slow or surprising; use `--no-generate`
- 2026-08-27 | Title numbered-list values stay on the same line | `\\s` after `1.` ate the next line and forged titles from empty template lists | Keep `[ \\t]+` after `N.`
