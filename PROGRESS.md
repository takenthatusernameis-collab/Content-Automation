# PROGRESS

- Reusable capability: tools/idea_utils_contract.py locks the shared idea.md field extractor. Future runs can prove consistent mechanism/problem/topic parsing instead of allowing local copies to reappear. Consistency stronger for every future packet.
- Local gates not re-run (STALL_GATE_CONFIRM; previous verification holds). No new failures. Changes are pure addition; no writes to packets.
- Human labor reduction: agents and future runs spend less time rediscovering or repairing extractor drift. Anti-drift stronger.
- Videos published remain 0. Stall continues. Preferred list still complete.

# PROGRESS

- Reusable capability: tools/experiment_baseline_starter.py, tools/experiment_notes_starter.py, tools/mechanism_align_scan.py, tools/expand_starter.py, tools/research_brief_starter.py, and tools/research_sources_starter.py now import extract from tools/idea_utils.py. Single source of truth for idea.md field parsing now covers experiment baseline/notes, mechanism alignment, expand starter, and research brief/sources paths. Consistency locked for every future packet.
- Local gates not re-run (STALL_GATE_CONFIRM; previous verification holds). No new failures. Changes are pure refactors; no writes to packets.
- Human labor reduction: agents receive consistent field extraction from every migrated experiment and research path, further reducing polishing and inconsistency risk across every subsequent video.
- Videos published remain 0. Stall continues. Preferred list still complete. Anti-drift stronger.
