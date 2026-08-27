# Production rules

Apply to every video packet. QA checks what can be checked mechanically.

## Packet
- One video = one folder `videos/NNN-slug/`
- Required files: `packet.md`, `idea.md`, `script.md`, `titles.md`, `thumbnail.md`, `qa.md`
- Optional: `research.md`, `assets.md`, `narration.md`, `publish.md`
- Status in `packet.md` must be one of: `draft`, `ready_for_vo`, `ready_for_edit`, `ready_to_publish`, `published`, `abandoned`
- Field values stay on the same line as the key

## Script
- Hook in the first 8–12 seconds of spoken words (about 20–35 words)
- State the viewer payoff before beat 2
- 4–7 beats after the hook
- One primary CTA
- No unverifiable statistics; if a number is used, cite source in `research.md`
- Working-niche tone: specific, calm, operational. No hustle slogans.

## Research
- `python3 tools/research_brief.py PATH` writes the stub (topic seed, source slots, spoken-number scan).
- Listing a URL is not verification. Do not scrape pages into Facts.
- `--source "line"` adds a human-provided pointer. `--force` is required to replace a filled file.
- Digit scan looks only at WORDS blocks (not `0:00` / `Beat 1` headings).

## Titles
- Provide at least 5 options
- One must be under 50 characters
- No ALL CAPS words except a single acronym

## Thumbnail
- One sentence of on-image text, max 5 words
- Describe subject, contrast, and what *not* to include
- Must match the chosen title promise

## QA gates
- `python3 tools/validate_packet.py PATH` — publish/completeness. Empty WORDS fail.
- `python3 tools/validate_packet.py --draft PATH` — intake/structure. Empty WORDS/titles/thumb are incomplete, not fail.
- `python3 tools/qa_checklist.py PATH` — writes `qa.md` mechanical boxes from files + human ticks from editor conventions. Never invents scores or auto-checks VO/cards/export.
- A hook that has words but is outside 20–35 still fails in both validate gates.

## Human handoff
Anything a human must still do is listed under `Remaining human work` in `packet.md`.
Editing conventions: `docs/editor.md`.
Human visual/audio ticks live in `qa.md` under **Human**.
