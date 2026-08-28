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
- 2026-08-27 | Scaffold writes titles/thumbs only when titles.md parses empty | Avoids a second CLI and avoids clobbering human or fixture copy | If heuristic titles become noise; `--no-generate` or filled-file keep
- 2026-08-27 | after_scaffold writes titles before qa.md | Mechanical title/thumb boxes would stay unchecked if qa ran first | Keep this order
- 2026-08-27 | publish.md is metadata only; no YouTube API | Recurring description/tags/comment labor can be drafted from packet fields | When OAuth exists and packet QA is PASS
- 2026-08-27 | Scaffold writes publish.md only when empty | Same empty-only contract as titles | If a human-edited description should always win
- 2026-08-27 | captions.md is a WORDS cue list at 150 wpm, not Whisper and not SRT | Recurring caption typing starts from the script the editor already has | When a selected VO take exists to time against
- 2026-08-27 | Scaffold writes captions.md only when empty | Same empty-only contract as publish | If a human-aligned caption file should always win
- 2026-08-27 | VO lives at `vo/NNN-slug-take-selected.wav` inside the packet | Stops "which take is the one" labor before any TTS choice | When a human adds a real take or a TTS CLI note
- 2026-08-28 | assets.md is a VISUAL card plan, not a media library | Recurring "what cards do I need" labor starts from script notes already written | When a human has local card files or a stock policy
- 2026-08-28 | Scaffold writes assets.md only when empty | Same empty-only contract as captions | If a human-edited card list should always win
- 2026-08-28 | Card binaries stay out of git by default | A committed PNG reads as "ready" even when it is a placeholder | When a packet actually ships and needs locked stills
- 2026-08-28 | Only format in use is face-free `explainer-6-10min` | Stops per-video timing debate; matches packet field already on the template | Human adds a second format in DECISIONS.md
- 2026-08-28 | Named export path is `exports/NNN-slug-vN.mp4`; no ffmpeg recipe yet | Recurring “what file do I hand to upload” labor is a name, not a build | When one packet has selected VO + ready cards
- 2026-08-28 | render.md is presence only; missing is a valid result | Recurring “is the wav/export actually here” labor should not require opening Finder | When a packet has real media; then `--force` refresh is allowed
- 2026-08-28 | Scaffold writes render.md only when empty | Same empty-only contract as assets | If a human-edited presence list should always win
- 2026-08-28 | pipeline_status.py is read-only; it never writes packet status | Recurring “where is this video” labor should be one command; auto-bump would hide missing VO | When a human wants a promote CLI with an explicit flag
- 2026-08-28 | next_action.py is read-only; one recommended step from inspect data | Recurring “which OPEN box first” labor should not require ranking seven checkboxes | When a human wants a promote CLI with an explicit flag
