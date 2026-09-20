# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-20T14:10:00Z — Run 237

- **Objective:** Close the leftover stall where Run 236 added a Q1 hold *after* WAVE 3 still led with idea_brief/new_packet copy-paste, so an agent who follows the first printed command still scaffolds Q2.
- **Inspected:** STATE, NEXT, ROADMAP, FAILURES, RUNS, queue_status.py, next_topic.py, queue_contract.py, doctor.py, needed.py. Confirmed Q1 still `ready_for_vo`. No git-visible Selected VO. Hold string existed but sat under scaffold commands. queue_contract required those --queue strings and "not the fixture" but did not lock hold order.
- **Action taken:** Printed Q1_HOLD first in `queue_next_footer`, `queue_status.report`, and `next_topic.py`. Labeled remaining scaffold lines parked until Q1 ships. Locked hold-before-scaffold order in `queue_contract.py`. Recorded do-not-reorder as NEXT item 85. Did not add a TTS CLI. Did not invent a wav or mp4. Did not retry HTTPS clone. Did not scaffold Q2. Did not add a selftest fixture. Did not realign hint/next_action. Did not grow bootstrap.
- **Result:** An agent who copy-pastes the first WAVE 3 line now sees the gate-machine hold, not Q2 scaffold. Automated steps stay 94. Videos produced stay 0. Estimated human minutes 3.9 → 3.8.
- **Verification status:** File API commits of queue_status.py, next_topic.py, queue_contract.py, and state pages. queue_contract was not executed against a live checkout in this sandbox (HTTPS clone parked). Selftest not re-run.
- **Important discovery:** A hold comment after copy-paste is still a scaffold prompt. Order is the stall, not missing text.
- **Blocker:** Packet-relative Selected VO still absent from any persistent machine the next agent can see. HTTPS clone parked. No OAuth env. No local master. No provider_video_id. No metrics.
- **Recommended next action:** On the gate machine, follow `docs/gate_machine.md` including one optional TTS block if needed. Do not add a TTS wrapper. Do not write a dummy mp4. Do not git add -f. Do not scaffold Q2. Do not move scaffold copy-paste above the Q1 hold. Do not strip the Q1 hold. Do not strip gate_machine from bootstrap or doctor reconstruct. Do not keep aligning remaining record-vo printers. Do not grow bootstrap further without a proven omission.

## 2026-09-20T08:22:00Z — Run 236

- **Objective:** Close the leftover stall where WAVE 3 board printers still presented Q2 scaffold commands as the live next action after Run 235 made clone-less reconstruct fetch `docs/gate_machine.md`.
- **Result:** Hold text landed on queue_status/next_topic. Automated steps stay 94. Estimated human minutes 4.0 → 3.9.
- **Verification status:** File API commits. Printers were not executed against a live checkout.
- **Important discovery:** Fetching the drop page in bootstrap can complete while the WAVE 3 board still sells scaffold as the job.
- **Blocker:** Packet-relative Selected VO still absent.
- **Recommended next action:** Follow `docs/gate_machine.md`. Do not strip the Q1 hold.

## 2026-09-20T05:23:00Z — Run 235

- **Result:** needed.py bootstrap + doctor reconstruct fetch docs/gate_machine.md. Estimated human minutes 4.1 → 4.0.

## 2026-09-20T04:20:00Z — Run 234

- **Result:** next_action after ready_for_edit names existing post-VO CLIs. Estimated human minutes 4.2 → 4.1.

## 2026-09-20T02:21:00Z — Run 233

- **Result:** hint.py build-cards/edit name existing post-VO CLIs. Estimated human minutes 4.3 → 4.2.

## 2026-09-16 — Runs 138–232

See prior commits. Summary: late-pipeline printers landed; Q1 remains ready_for_vo without an on-disk take.
