# Production rules

Apply to every video packet. QA checks what can be checked mechanically.

## Packet
- One video = one folder `videos/NNN-slug/`
- Required files: `packet.md`, `idea.md`, `script.md`, `titles.md`, `thumbnail.md`, `qa.md`
- Optional: `research.md`, `assets.md`, `narration.md`, `publish.md`, `captions.md`, `render.md`, `vo_session.md`, `expand.md`
- Status in `packet.md` must be one of: `draft`, `ready_for_vo`, `ready_for_edit`, `ready_to_publish`, `published`, `abandoned`
- Field values stay on the same line as the key
- `python3 tools/pipeline_status.py` is the read-only board across packets. It does not write files.
- `python3 tools/next_action.py` is the read-only next human step. It does not write files.

## Script
- Hook in the first 8–12 seconds of spoken words (about 20–35 words)
- State the viewer payoff before beat 2
- 4–7 beats after the hook
- One primary CTA
- Total spoken WORDS should match the locked format band (900–1500 for `explainer-6-10min`)
- Default validate prints WARN when the band is missed; `--duration` fails
- Do not record VO while the duration WARN is present on a real packet
- Do not pad `videos/sample-001-*` to clear the WARN
- `python3 tools/expand_brief.py PATH` writes `expand.md` per-beat Have/Target/Add from current WORDS
- An expand.md budget is not a rewritten script. Do not autofill WORDS from it
- `--force` is required to replace a filled `expand.md`
- Scaffold writes expand.md only when empty
- `python3 tools/expand_prompt.py PATH` prints a paste-ready expander pack. It does not write `script.md`
- A printed prompt is not a draft. Do not write it onto sample-001
- No unverifiable statistics; if a number is used, cite source in `research.md`
- Working-niche tone: specific, calm, operational. No hustle slogans.

## QA gates
- `python3 tools/validate_packet.py PATH` — publish/completeness. Empty WORDS fail. Duration misses print WARN.
- `python3 tools/validate_packet.py --duration PATH` — same as publish gate plus spoken-length FAIL.
- `python3 tools/next_action.py` — read-only: one next human step. Routes `expand-script` before `record-vo` when duration WARN is present.

## Human handoff
Beat budget: packet `expand.md`.
Expand paste pack: `python3 tools/expand_prompt.py PATH`.
