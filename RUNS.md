# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-20T04:20:00Z — Run 234

- **Objective:** Close the leftover stall where `tools/next_action.py` still told operators to invent a stock card and then edit against editor.md after Run 233 pointed hint.py at card_generator/timeline/media_qa/assemble.
- **Inspected:** STATE, NEXT, ROADMAP, OPERATOR_HOLD, FAILURES, RUNS, hint.py, next_action.py, pipeline_status.py. Confirmed Q1 still `ready_for_vo`. No git-visible Selected VO. hint.py build-cards/edit already name the post-VO CLIs. next_action.py ready_for_edit still said "do not download stock from this tool" and "Edit against docs/editor.md … then export".
- **Action taken:** Pointed next_action.py build-cards Why at `card_generator.py --write-manifest` and edit Why at timeline/media_qa/assemble dry-run. Did not add a TTS CLI. Did not invent a wav or mp4. Did not retry HTTPS clone. Did not scaffold Q2. Did not add a selftest fixture. Did not add another record-vo pointer.
- **Result:** An operator who runs next_action after ready_for_edit is sent to the existing post-VO CLIs. hint.py Why text inherits this sentence. Automated steps stay 94. Videos produced stay 0. Estimated human minutes 4.2 → 4.1.
- **Verification status:** File API commit of next_action.py and state pages. Commands were not executed against a live packet (no gate-machine checkout; HTTPS clone parked). Selftest not re-run in this sandbox.
- **Important discovery:** hint.py copy-paste and next_action.py Why text can drift independently. Aligning only one leaves the WAVE 3 board reconstructing labor the moment VO lands.
- **Blocker:** Packet-relative Selected VO still absent from any persistent machine the next agent can see. HTTPS clone parked. No OAuth env. No local master. No provider_video_id. No metrics.
- **Recommended next action:** On the gate machine, follow `docs/gate_machine.md` including one optional TTS block if needed. Do not add a TTS wrapper. Do not write a dummy mp4. Do not git add -f. Do not scaffold Q2. Do not strip gate_machine pointers. Do not revert hint.py or next_action.py build-cards/edit. Do not keep aligning remaining record-vo printers.

## 2026-09-20T02:21:00Z — Run 233

- **Objective:** Close the leftover stall where `tools/hint.py` still told operators to invent cards and forbade an ffmpeg recipe after Runs 214/218 landed card_generator and assemble.
- **Inspected:** STATE, NEXT, ROADMAP, OPERATOR_HOLD, FAILURES, RUNS, gate_machine, hint.py, next_action.py, pipeline_status.py, doctor.py. Confirmed Q1 still `ready_for_vo`. No git-visible Selected VO. hint.py record-vo already names gate_machine (Run 231). hint.py build-cards still said `--dry-run` plus a stock-download comment. hint.py edit still said "do not write an ffmpeg recipe here".
- **Action taken:** Pointed hint.py build-cards at `card_generator.py --write-manifest` and hint.py edit at timeline/media_qa/assemble dry-run. Did not add a TTS CLI. Did not invent a wav or mp4. Did not retry HTTPS clone. Did not scaffold Q2. Did not add a selftest fixture. Did not add another record-vo pointer.
- **Result:** An operator who reaches ready_for_edit is sent to the existing post-VO CLIs instead of inventing a card download or treating assemble as forbidden. Automated steps stay 94. Videos produced stay 0. Estimated human minutes 4.3 → 4.2. doctor.py inherits the same commands via hint.commands_for.
- **Verification status:** File API commit of hint.py and state pages. Commands were not executed against a live packet (no gate-machine checkout; HTTPS clone parked). Selftest not re-run in this sandbox.
- **Important discovery:** Record-vo printers can be aligned while the next-status printers still contradict NEXT. That is a different stall class than Runs 230–232: it does not block the drop, but it would reconstruct labor the moment VO lands.
- **Blocker:** Packet-relative Selected VO still absent from any persistent machine the next agent can see. HTTPS clone parked. No OAuth env. No local master. No provider_video_id. No metrics.
- **Recommended next action:** On the gate machine, follow `docs/gate_machine.md` including one optional TTS block if needed. Do not add a TTS wrapper. Do not write a dummy mp4. Do not git add -f. Do not scaffold Q2. Do not strip gate_machine pointers. Do not revert hint.py build-cards/edit. Do not keep aligning remaining record-vo printers.

## 2026-09-20T01:04:00Z — Run 232

- **Objective:** Close the leftover stall where `tools/pipeline_status.py` printed the DROP path but never named `docs/gate_machine.md` after Runs 228–231 published that recipe and pointed hint/next_action at it.
- **Result:** An operator who runs `python3 tools/pipeline_status.py` on Q1 is sent to the drop page instead of only seeing a path. Automated steps stay 94. Videos produced stay 0. Estimated human minutes 4.4 → 4.3.
- **Blocker:** Packet-relative Selected VO still absent.

## 2026-09-20T00:05:00Z — Run 231

- **Objective:** Close the leftover stall where the live record-vo printers still said only "record the selected take" after Runs 228–230 published `docs/gate_machine.md`.
- **Result:** hint.py / next_action.py record-vo name the drop page. Estimated human minutes 4.5 → 4.4.

## 2026-09-19T23:10:00Z — Run 230

- **Result:** Operator following human_session is no longer told to ignore the drop page they were just sent to. Estimated human minutes 4.6 → 4.5.

## 2026-09-19T22:20:00Z — Run 229

- **Result:** Optional local TTS one-liners on existing drop page. Automated steps stay 94.

## 2026-09-19T21:10:00Z — Run 228

- **Result:** Operator drop recipe is one page. Automated steps stay 94.

## 2026-09-19T18:20:00Z — Run 227

- **Result:** System state unchanged in capability. Flagged the 213–226 adapter/lock treadmill in FAILURES.md.

## 2026-09-19T15:05:00Z — Run 226

- **Result:** A dummy export can no longer look upload-READY without a selftest lock.

## 2026-09-16 — Runs 138–221

See prior commits. Summary: late-pipeline printers landed; Q1 remains ready_for_vo without an on-disk take.
