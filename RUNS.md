# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-20T00:05:00Z — Run 231

- **Objective:** Close the leftover stall where the live record-vo printers still said only "record the selected take" after Runs 228–230 published `docs/gate_machine.md`.
- **Inspected:** STATE, NEXT, ROADMAP, OPERATOR_HOLD, FAILURES, NEXT_RUN_PROMPT, gate_machine, hint.py, next_action.py, needed.py. Confirmed Q1 still `ready_for_vo`. No git-visible Selected VO. hint.py record-vo emitted "then record the selected take" and never named gate_machine. next_action.py ready_for_vo sentence was "Record the selected take" only.
- **Action taken:** Pointed those two printers at `docs/gate_machine.md` and named the authorized generated fallback. Did not add a TTS CLI. Did not invent a wav or mp4. Did not retry HTTPS clone. Did not scaffold Q2. Did not add a selftest fixture.
- **Result:** An operator who runs `python3 tools/hint.py` on Q1 is sent to the drop page instead of inventing a recording-only step. Automated steps stay 94. Videos produced stay 0. Estimated human minutes 4.5 → 4.4.
- **Verification status:** File API commit of hint.py, next_action.py, and state pages. Commands were not executed against a live packet (no gate-machine checkout; HTTPS clone parked). Selftest not re-run in this sandbox.
- **Important discovery:** Session markdown can be aligned while the copy-paste printers operators actually run still omit the authorized recipe. That is the same stall class as Run 230, one layer closer to the CLI.
- **Blocker:** Packet-relative Selected VO still absent from any persistent machine the next agent can see. HTTPS clone parked. No OAuth env. No local master. No provider_video_id. No metrics.
- **Recommended next action:** On the gate machine, follow `docs/gate_machine.md` including one optional TTS block if needed. Do not add a TTS wrapper. Do not write a dummy mp4. Do not git add -f. Do not scaffold Q2. Do not strip the gate_machine pointer from hint/next_action.

## 2026-09-19T23:10:00Z — Run 230

- **Objective:** Remove leftover operator/agent wording that could stall the authorized generated-VO drop after Run 229 added TTS one-liners.
- **Inspected:** STATE, NEXT, ROADMAP, OPERATOR_HOLD, FAILURES, gate_machine, human_session, agent_session. Confirmed Q1 still `ready_for_vo`. No git-visible Selected VO. gate_machine already has espeak-ng/say/ffmpeg one-liners. human_session step 4 still said "Do not write an ffmpeg recipe." agent_session still said "Recording is still a human gate" and "Do not invent ... ffmpeg recipes."
- **Action taken:** Pointed those lines at `docs/gate_machine.md` for the authorized generated drop. Kept dummy `export/master.mp4` and `assemble.py --execute` forbidden until VO+cards and media_qa PASS. Did not add a TTS CLI. Did not invent a wav or mp4. Did not retry HTTPS clone. Did not scaffold Q2.
- **Result:** Operator following human_session is no longer told to ignore the drop page they were just sent to. Automated steps stay 94. Videos produced stay 0. Estimated human minutes 4.6 → 4.5.
- **Verification status:** File API commit of human_session, agent_session, and state pages. operator_pin_contract strings (Q1 title/folder/problem/fill-idea/mark_topic) were not stripped. Commands were not executed (no gate-machine checkout).
- **Important discovery:** Run 228/229 authorized generated VO and published TTS one-liners, but older "no ffmpeg recipe / recording-only gate" sentences remained on the two session pages. That mismatch can still stall the drop.
- **Blocker:** Packet-relative Selected VO still absent from any persistent machine the next agent can see. HTTPS clone parked. No OAuth env. No local master. No provider_video_id. No metrics.
- **Recommended next action:** On the gate machine, follow `docs/gate_machine.md` including one optional TTS block if needed. Do not add a TTS wrapper. Do not write a dummy mp4. Do not git add -f. Do not scaffold Q2. Do not restore the old recording-only wording.

## 2026-09-19T22:20:00Z — Run 229

- **Objective:** Reduce remaining operator invention of a local TTS command without adding a 95th adapter.
- **Action taken:** Extended `docs/gate_machine.md` with optional already-installed TTS one-liners.
- **Result:** Automated steps stay 94. Videos produced stay 0. Estimated human minutes 4.7 → 4.6.
- **Blocker:** Packet-relative Selected VO still absent.

## 2026-09-19T21:10:00Z — Run 228

- **Objective:** Reduce operator reconstruction of the Selected VO drop step without adding a 95th adapter.
- **Result:** Operator drop recipe is one page. Automated steps stay 94.

## 2026-09-19T18:20:00Z — Run 227

- **Objective:** Inspect HEAD after Run 226 and take the smallest compound step that does not add another dry-run adapter.
- **Result:** System state unchanged in capability. Flagged the 213–226 adapter/lock treadmill in FAILURES.md.

## 2026-09-19T15:05:00Z — Run 226

- **Result:** A dummy export can no longer look upload-READY without a selftest lock.

## 2026-09-19T13:05:00Z — Run 225

- **Result:** youtube_upload requires ftyp.

## 2026-09-19T12:10:00Z — Run 224

- **Result:** media_qa/assemble/complete reject junk export/master.mp4 without ftyp.

## 2026-09-19T11:12:00Z — Run 223

- **Result:** Silent or clipped takes fail before ffmpeg.

## 2026-09-19T10:10:00Z — Run 222

- **Result:** experiment/complete selftest lock on HEAD.

## 2026-09-16 — Runs 138–221

See prior commits. Summary: late-pipeline printers landed; Q1 remains ready_for_vo without an on-disk take.
