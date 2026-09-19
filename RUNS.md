# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

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
- **Inspected:** STATE, NEXT, ROADMAP, OPERATOR_HOLD, FAILURES, gate_machine, human_session, narration_adapter. Confirmed `--print-words` exists on HEAD. Confirmed `tools/vo_session.py` exists. Q1 still `ready_for_vo`. No git-visible Selected VO.
- **Action taken:** Extended `docs/gate_machine.md` with optional already-installed TTS one-liners that write only to the packet DROP path (cp existing file, espeak-ng+ffmpeg, macOS say+ffmpeg). Did not add a TTS CLI under tools/. Did not invent a wav or mp4. Did not retry HTTPS clone. Did not scaffold Q2.
- **Result:** Operator can paste a TTS command instead of designing one. Automated steps stay 94. Videos produced stay 0. Estimated human minutes 4.7 → 4.6.
- **Verification status:** File API commit of gate_machine.md and state pages. Commands themselves were not executed (no gate-machine checkout; HTTPS clone parked). espeak-ng/say/ffmpeg presence on the operator machine is unverified.
- **Important discovery:** The drop page after Run 228 still said "any local TTS you already have" with no command. That leftover invention step can stall the authorized generated fallback even when espeak-ng or say is already installed.
- **Blocker:** Packet-relative Selected VO still absent from any persistent machine the next agent can see. HTTPS clone parked. No OAuth env. No local master. No provider_video_id. No metrics.
- **Recommended next action:** On the gate machine, follow `docs/gate_machine.md` including one optional TTS block if needed. Do not add a TTS wrapper. Do not write a dummy mp4. Do not git add -f. Do not scaffold Q2.

## 2026-09-19T21:10:00Z — Run 228

- **Objective:** Reduce operator reconstruction of the Selected VO drop step without adding a 95th adapter.
- **Inspected:** STATE, NEXT, ROADMAP, OPERATOR_HOLD, FAILURES, human_session, agent_session, narration_adapter, Q1 vo_origin. Q1 still `ready_for_vo`. No git-visible Selected VO. Generated fallback already authorized. human_session Stop line still treated TTS as unauthorized unless a human named the policy, which contradicted OPERATOR_HOLD.
- **Action taken:** Added `docs/gate_machine.md` with the copy-paste DROP path, WORDS extract via existing `narration_adapter.py --print-words`, and the existing gate sequence. Pointed NEXT item 1 at that page. Did not add a TTS CLI. Did not invent a wav or mp4. Did not retry HTTPS clone. Did not scaffold Q2.
- **Result:** Operator drop recipe is one page. Automated steps stay 94. Videos produced stay 0. Estimated human minutes 4.8 → 4.7 (less hunting across NEXT/STATE/narration).
- **Verification status:** File API commit of `docs/gate_machine.md` and state pages. Full packet selftest against a clone was not executed (HTTPS clone still parked).
- **Important discovery:** The live contradiction was policy vs operator page: generated fallback is authorized, but human_session still told the operator not to treat TTS as selected. That mismatch can keep the take from landing even after the deadline.
- **Blocker:** Packet-relative Selected VO still absent from any persistent machine the next agent can see. HTTPS clone parked. No OAuth env. No local master. No provider_video_id. No metrics.
- **Recommended next action:** On the gate machine, follow `docs/gate_machine.md`. Do not add another adapter. Do not write a dummy mp4. Do not git add -f. Do not scaffold Q2.

## 2026-09-19T18:20:00Z — Run 227

- **Objective:** Inspect HEAD after Run 226 and take the smallest compound step that does not add another dry-run adapter.
- **Action taken:** No new CLI, no new selftest fixture, no invented wav or mp4. Recorded the hold-honor and flagged the 213–226 adapter/lock treadmill in FAILURES.md.
- **Result:** System state unchanged in capability. Human-minute estimate stays 4.8. Automated steps stay 94. Videos produced stay 0.
- **Blocker:** Packet-relative Selected VO still absent.

## 2026-09-19T15:05:00Z — Run 226

- **Objective:** Land the youtube_upload fail-closed selftest fixture that Run 225 recommended and did not add.
- **Result:** A dummy export can no longer look upload-READY without a selftest lock. Human-minute estimate 4.9 → 4.8. Automated steps stay 94.
- **Blocker:** Packet-relative Selected VO still absent.

## 2026-09-19T13:05:00Z — Run 225

- **Result:** youtube_upload requires ftyp. Human-minute estimate 5.0 → 4.9.

## 2026-09-19T12:10:00Z — Run 224

- **Result:** media_qa/assemble/complete reject junk export/master.mp4 without ftyp.

## 2026-09-19T11:12:00Z — Run 223

- **Result:** Silent or clipped takes fail before ffmpeg.

## 2026-09-19T10:10:00Z — Run 222

- **Result:** experiment/complete selftest lock on HEAD.

## 2026-09-16 — Runs 138–221

See prior commits. Summary: late-pipeline printers landed; Q1 remains ready_for_vo without an on-disk take.
