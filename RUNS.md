# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-10T15:05:00Z — Run 051

- **Objective:** Close the leftover paste gap: after scaffold, new_packet reprinted topic + mechanism but not the locked Q1 problem sentence, so the human still had to join two pages.
- **Inspected:** STATE/NEXT/RUNS after Run 050. Q1 still queued. operator_pin already locked Q1_PROBLEM. needed.py left untouched. Frozen doctor/hint/needed not edited.
- **Action taken:** `tools/new_packet.py` idea_followup now reprints `- problem: {Q1_PROBLEM}` for Q1 (import from operator_pin_contract, with a matching fallback string). Other ids print an explicit no-locked-problem placeholder. `tools/scaffold_contract.py` now requires that Q1 problem line in idea_followup. Did not write idea.md. Did not scaffold Q1. Did not add a queue column. Did not edit needed.py. Did not map unmapped locks.
- **Result:** SCAFFOLD CONTRACT PASS on reconstructed tools + docs/topic_queue tree (`python3 tools/scaffold_contract.py`, exit 0). idea_followup printed topic + problem + mechanism and the no-write banner. Queue rows remain queued. No new packet folder.
- **Verification status:** completed for the reprint lock (local PASS, exit 0). Full selftest / doctor against sample-001 not re-run (clone-less). No media.
- **Important discovery:** The operator pin and the scaffold reprint were two sources of truth for the same three idea fields. Sharing Q1_PROBLEM keeps them aligned without widening the queue schema.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After scaffold, paste the three reprinted idea fields. After editing human_session or the Q1 queue row, run `operator_pin_contract.py`. After editing new_packet idea reprint, run `scaffold_contract.py`. Agents: --bootstrap then --plan; do not add WAVE 4; do not auto-write idea.md; do not auto-scaffold Q1.

## 2026-09-10T14:20:00Z — Run 050

- **Objective:** Lock the Q1 idea.md problem sentence on the operator page, and list the two unmapped locks on the agent page so clone-less runs do not scan NEXT for them.
- **Result:** OPERATOR PIN CONTRACT PASS. Queue rows remain queued. No new packet folder.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-10T13:20:00Z — Run 049

- **Objective:** Lock the operator-page Q1 pin so human_session cannot drift off the live topic_queue title, 002-slug, one_line, fill-idea note, or new_packet command while Q1 is still queued.
- **Result:** OPERATOR PIN CONTRACT PASS. Queue rows remain queued. No new packet folder.
- **Recommended next action:** Human runs queue_status then human_session.

## Earlier runs 001–48
See prior commits for full detail.
