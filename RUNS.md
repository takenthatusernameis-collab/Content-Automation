# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-08-28T00:15:00+03:00 — Run 011

- **Objective:** Add asset/card filename stub from script VISUAL lines plus `docs/assets.md`. No stock shopping, no image download, no binaries.
- **Inspected:** STATE/NEXT/ROADMAP after Run 010. NEXT item 1 was assets stub. Read after_scaffold, caption_brief, qa_checklist, sample script/assets, editor conventions.
- **Action taken:** New `tools/asset_brief.py` builds planned card rows + suggested `cards/{beat}-{slug}.png` names from VISUAL blocks. Empty-file / `--force` guard. `docs/assets.md` names types and paths. Scaffold `after_scaffold.generate` writes assets after captions, before research/qa. Template `assets.md` is a placeholder. sample-001 got a schema fixture `assets.md`; titles/thumbs untouched. QA gained a human assets tick and a presence note. Did not download images. Did not call stock APIs.
- **Result:** Card naming starts from existing script VISUAL lines. Empty-visual packets stay placeholders so later VISUAL can fill them. Card binaries stay out of git.
- **Verification status:** completed (local reconstruction of sample script + tool; live GitHub push of tools/docs). Commands:
  - `asset_brief.py sample-script --dry-run` -> Card count 5; hook `cards/hook-start-cue-problem.png` text-card; beat1/2/4 diagram; beat3 text-card; exit 0
  - first write -> exit 0
  - second write without `--force` -> exit 1 `already filled`
  - empty VISUAL render -> Status placeholder; `assets_is_filled` False
  - template empty table -> `assets_is_filled` False
  - old two-row sample table -> `assets_is_filled` True (keep unless schema rewrite)
- **Important discovery:** Do not commit `cards/*.png` to make Status look `ready`. A filename in `assets.md` is a plan, not a file.
- **Blocker:** None for this step. Publishing/TTS/YouTube API/stock remain in BLOCKED.md. Stock row now points at the filename convention.
- **Recommended next action:** Face-free format timing page or a render checklist that names outputs only. Still no OAuth, TTS, stock, or ffmpeg recipe.

## 2026-08-27T23:10:00+03:00 — Run 010

- **Objective:** Add caption intake stub from script WORDS plus narration path conventions. No Whisper, no SRT, no TTS vendor.
- **Recommended next action:** Asset/card filename stub from script VISUAL lines. Still no OAuth or stock shopping.

## 2026-08-27T22:15:00+03:00 — Run 009

- **Objective:** Add `tools/publish_brief.py` publish metadata stub. No YouTube API.

## 2026-08-27T21:10:00+03:00 — Run 008

- **Objective:** Optional title/thumb brief at scaffold time when those files are still empty.

## 2026-08-27T19:25:00+03:00 — Run 007

- **Objective:** Wire scaffold CLIs so new packets get generated `qa.md` + `research.md`.

## 2026-08-27T17:10:00+03:00 — Run 006

- **Objective:** Add `tools/research_brief.py`.

## 2026-08-27T14:15:00+03:00 — Run 005

- **Objective:** Add `tools/qa_checklist.py`.

## 2026-08-27T13:08:00+03:00 — Run 004

- **Objective:** Add `validate_packet.py --draft`.

## 2026-08-27T11:00:00+03:00 — Run 003

- **Objective:** Add title/thumbnail brief generator.

## 2026-08-27T10:15:00+03:00 — Run 002

- **Objective:** Lock working niche, add idea intake, bind script-writer prompt.

## 2026-08-27T08:12:00+03:00 — Run 001

- **Objective:** Bootstrap production memory + one reusable capability.
