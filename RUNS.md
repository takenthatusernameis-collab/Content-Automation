# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-08-28T06:20:00+03:00 — Run 017

- **Objective:** Stop routing humans to record VO on a structurally PASS script that is far under the locked 6–10 min format. No wav, no TTS, no ffmpeg, no OAuth, no fixture pad.
- **Inspected:** STATE/NEXT/ROADMAP after Run 016. Discovery: sample-001 is 153 spoken words (~01:01) vs 900–1500 band. NEXT said wait for a take; recording that take would waste labor.
- **Action taken:** Extended `tools/validate_packet.py` with FORMAT_SPOKEN_WORDS, WARN by default, `--duration` FAIL. Routed `tools/next_action.py` to `expand-script` when duration WARN is present on draft/ready_for_vo. Documented band in `docs/format.md`, `docs/production_rules.md`, `prompts/script_writer.md`. Did not change `pipeline_status.py` return contract. Did not rewrite sample-001 WORDS.
- **Result:** Local fixture copy: default validate `PASS` + `WARN spoken 153 words (~01:01 at 150 wpm) below explainer-6-10min band 900–1500` exit 0. `--duration` `FAIL` exit 1. `next_action.py` code `expand-script`. Board 2-tuple still unpacks.
- **Verification status:** completed for tool logic on a local copy of sample fields. GitHub push of tools + docs + memory. No media created. Sample WORDS unchanged.
- **Important discovery:** Duration must stay a WARN on the default gate or the fixture PASS contract breaks and `--strict` board semantics change. Routing lives in next_action, not in making short scripts FAIL.
- **Blocker:** None for this step. ffmpeg recipe still parked until VO + cards exist. YouTube/TTS/stock remain in BLOCKED.md.
- **Recommended next action:** Wait for a real selected take or card file on a packet whose WORDS already sit in band. Still no OAuth, TTS, stock, ffmpeg recipe, fixture pad, or status auto-bump.

## 2026-08-28T05:24:00+03:00 — Run 016

- **Objective:** Cut recurring VO-prep labor: turn PASS script WORDS into a packet-local reading card and named take path.
- **Recommended next action:** Wait for a real selected take or card file.

## 2026-08-28T05:12:00+03:00 — Run 015

- **Objective:** Add a read-only next-action resolver.

## 2026-08-28T04:08:00+03:00 — Run 014

- **Objective:** Add a read-only multi-packet status board.

## 2026-08-28T02:12:00+03:00 — Run 013

- **Objective:** Add packet-local `render.md` presence checklist.

## 2026-08-28T01:12:00+03:00 — Run 012

- **Objective:** Lock face-free explainer timing and name export/VO/card outputs.

## 2026-08-28T00:15:00+03:00 — Run 011

- **Objective:** Add asset/card filename stub from script VISUAL lines.

## 2026-08-27T23:10:00+03:00 — Run 010

- **Objective:** Add caption intake stub from script WORDS.

## Earlier runs 001–009
See prior commits for full detail. Foundation through publish stub.
