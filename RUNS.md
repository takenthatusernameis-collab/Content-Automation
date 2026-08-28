# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-08-28T07:20:00+03:00 — Run 018

- **Objective:** When next_action says `expand-script`, stop leaving the human to guess which beat to grow. No WORDS rewrite, no fixture pad, no wav, no TTS, no ffmpeg, no OAuth.
- **Inspected:** STATE/NEXT/ROADMAP after Run 017. Sample still 153 spoken words (~01:01). Duration routing exists; the missing piece was a packet-local budget.
- **Action taken:** Added `tools/expand_brief.py` (Status short/in-band/long + per-section Have/Target/Add). Wired empty-only write through `after_scaffold.py`. Added `videos/_template/expand.md` and a schema fixture `videos/sample-001-*/expand.md`. Did not change sample-001 script.md. Did not rewrite next_action.py or validate_packet.py.
- **Result:** Local dry-run on a copy of sample fields: Status `short`, 153 words, ~01:01, delta 1047, hook add 0, beats ~245 each. GitHub push of tool + scaffold + template + fixture expand.md + memory.
- **Verification status:** completed for tool logic on a local copy. GitHub push verified by ref update. No media created. Sample WORDS unchanged.
- **Important discovery:** A budget file can look like a draft. Status `short` must stay a plan. Auto-writing WORDS from the budget would violate the fixture freeze and invent content.
- **Blocker:** None for this step. ffmpeg recipe still parked until VO + cards exist. YouTube/TTS/stock remain in BLOCKED.md.
- **Recommended next action:** Wait for a real selected take or card file on a packet whose WORDS already sit in band. Still no OAuth, TTS, stock, ffmpeg recipe, fixture pad, WORDS autofill, or status auto-bump.

## 2026-08-28T06:20:00+03:00 — Run 017

- **Objective:** Stop routing humans to record VO on a structurally PASS script that is far under the locked 6–10 min format.
- **Recommended next action:** Wait for a real selected take or card file. Duration routing closed.

## 2026-08-28T05:24:00+03:00 — Run 016

- **Objective:** Cut recurring VO-prep labor: turn PASS script WORDS into a packet-local reading card and named take path.

## Earlier runs 001–015
See prior commits for full detail.
