# PROGRESS

- Reusable capability: tools/idea_utils.py provides the canonical idea.md field extractor (mechanism, problem, topic). tools/hook_suggest.py, tools/title_suggest.py, tools/body_suggest.py, tools/payoff_suggest.py, and tools/cta_suggest.py now import extract from it. Single source of truth reduces drift risk for field parsing across suggestors. Applies to every future packet.
- Local gates not re-run (STALL_GATE_CONFIRM; previous verification holds). No new failures. Changes are pure refactors; no writes to packets.
- Human labor reduction: agents receive consistent field extraction from every migrated suggestor path, further reducing polishing and inconsistency risk across every subsequent video.
- Videos published remain 0. Stall continues. Preferred list still complete. Anti-drift stronger.

# PROGRESS

- Reusable capability: tools/hook_suggest.py, tools/payoff_suggest.py, tools/cta_suggest.py, tools/title_suggest.py, and tools/description_suggest.py now import from the shared tools/phrase_utils.shorten. All remaining local copies eliminated. Single source of truth is complete for natural-phrase logic; consistency and future maintenance locked for every packet.
- Local gates not re-run (STALL_GATE_CONFIRM; previous verification holds). No new failures. Changes are pure refactors; no writes to packets.
- Human labor reduction: agents receive consistent natural-phrase suggestions from every structure and metadata path, further reducing polishing and drift risk across every subsequent video.
- Videos published remain 0. Stall continues. Preferred list still complete. Anti-drift stronger.
