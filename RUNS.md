# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-08-27T17:10:00+03:00 — Run 006

- **Objective:** Add `tools/research_brief.py` so packets get a research.md stub (source list + no unverifiable-stats reminder) without scraping the web.
- **Inspected:** STATE/NEXT/ROADMAP after Run 005. NEXT item 1 was the research stub. Read `docs/production_rules.md`, template + sample `research.md`, `qa_checklist.py` digit scan, `new_idea.py`.
- **Action taken:** Added `tools/research_brief.py`. Updated `_template/research.md` and sample-001 `research.md` to the stub schema (titles/thumbs/script untouched). Documented the command in production rules and README. Did not wire scaffold CLIs (left as next). Did not scrape or add fake sources.
- **Result:** One command writes topic seed, source slots, claims to avoid, and a WORDS-only digit scan. Filled research files refuse overwrite without `--force`. `--source` only stores a human-provided pointer.
- **Verification status:** completed (local reconstruction; live GitHub push of the tool). Commands:
  - `research_brief.py videos/sample-001-why-systems-beat-motivation --dry-run` -> exit 0; sources keep `Fixture packet; no external claims.`; WORDS digits none; headings `0:00` / `Beat 1` not listed
  - write without `--force` on filled sample research -> exit 1 (guard)
  - empty template research `--dry-run` -> placeholder source line, exit 0
  - script WORDS containing `87%` -> scan lists `87%` (not heading digits; percent kept)
  - `--source "Human note: no external study used"` write on empty file -> exit 0; second write without `--force` -> exit 1
  - missing directory -> exit 1
- **Important discovery:** A trailing `\\b` after optional `%` can match before the percent and drop it. Treat `87%` as one token.
- **Blocker:** None for this step. Publishing/TTS/YouTube API remain in BLOCKED.md. HTTPS clone still not used.
- **Recommended next action:** Wire `new_idea.py` / `new_packet.py` to generate `qa.md` + `research.md` at scaffold time.

## 2026-08-27T14:15:00+03:00 — Run 005

- **Objective:** Add `tools/qa_checklist.py` that writes `qa.md` from production rules + editor conventions without inventing scores.
- **Inspected:** STATE/NEXT/ROADMAP after Run 004. NEXT item 1 was the checklist writer. Read `docs/production_rules.md`, `docs/editor.md`, template + sample `qa.md`, `validate_packet.py`.
- **Action taken:** Added `tools/qa_checklist.py`. Updated `_template/qa.md` and sample-001 `qa.md` to the new schema (titles/thumbs untouched). Documented the command in production rules and README. Did not add research CLI (left as next). Did not touch VO/TTS/ffmpeg.
- **Result:** One command fills mechanical boxes from files and lists human ticks (VO take, card readability, CTA assignment, hold time, end screen, export name, unsourced stats, title lock, thumb design).
- **Verification status:** completed (local reconstruction; live GitHub push of the tool). Commands:
  - reconstructed sample-001: `validate_packet.py` -> `PASS` exit 0
  - `qa_checklist.py --dry-run` on sample-001 -> exit 0, gate **PASS**, all mechanical `[x]`, all human `[ ]`, no digit tokens in WORDS
  - empty hook/titles/thumb with `--draft`: validate `DRAFT-INCOMPLETE` exit 0; checklist mechanical hook/titles/thumb unchecked; gate **DRAFT-INCOMPLETE**
  - same packet default validate -> `FAIL` exit 1
  - existing human `[x]` on exact HUMAN_ITEMS label is preserved; old mechanical `[x]` labels are not treated as human ticks
  - write path then `validate_packet.py` still `PASS` exit 0
- **Important discovery:** A naive digit scan of `script.md` treats `0:00` and `Beat 1` as statistics. Restrict scans to `WORDS:` blocks.
- **Blocker:** None for this step. Publishing/TTS/YouTube API remain in BLOCKED.md. HTTPS clone still not used.
- **Recommended next action:** `research.md` intake stub CLI (source list + no unverifiable stats reminder).

## 2026-08-27T13:08:00+03:00 — Run 004

- **Objective:** Add `validate_packet.py --draft` so intake packets with empty WORDS are not a publish-gate FAIL.
- **Inspected:** STATE/NEXT after Run 003. NEXT item 1 was draft-incomplete mode. Read current validator + sample-001 + new_idea output shape.
- **Action taken:** Extended `tools/validate_packet.py` with `--draft` / `--incomplete`. Empty hook/CTA WORDS, empty titles, and empty on-image text become `DRAFT-INCOMPLETE` (exit 0). Missing files, bad status, beat-count, empty id/title, and malformed non-empty hooks still FAIL. Fixed one-line field parsers so blank `id:` / `Primary:` no longer swallow the next line. Added `docs/editor.md` conventions only (no ffmpeg). Did not touch sample-001 copy in the remote repo.
- **Result:** Intake and publish QA are separate gates. Default command remains the completeness gate.
- **Verification status:** completed (local reconstruction of sample-001 + synthetic packets; live GitHub push of the tool).
- **Recommended next action:** `tools/qa_checklist.py` to fill `qa.md` from production rules + editor conventions.

## 2026-08-27T11:00:00+03:00 — Run 003

- **Objective:** Add a reusable title/thumbnail brief generator from packet idea fields.
- **Action taken:** Added `tools/title_thumb_brief.py` (heuristic, no API).
- **Recommended next action:** `validate_packet.py --draft` incomplete-WORDS mode.

## 2026-08-27T10:15:00+03:00 — Run 002

- **Objective:** Advance assisted production: lock working niche, add idea intake, bind a script-writer prompt.
- **Recommended next action:** Title/thumbnail brief generator from packet fields.

## 2026-08-27T08:12:00+03:00 — Run 001

- **Objective:** Bootstrap an empty repo into a usable production memory + one reusable capability.
- **Recommended next action:** `tools/new_idea.py` or `prompts/script_writer.md` bound to production rules. Do not rebuild foundation.
