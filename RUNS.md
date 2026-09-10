# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-10T13:20:00Z — Run 049

- **Objective:** Lock the operator-page Q1 pin so human_session cannot drift off the live topic_queue title, 002-slug, one_line, fill-idea note, or new_packet command while Q1 is still queued.
- **Inspected:** STATE/NEXT/RUNS after Run 048. Q1 still queued. idea_gate_contract exists and stays unmapped. needed.py left untouched. which_contract left unmapped.
- **Action taken:** Added `tools/operator_pin_contract.py`. It parses Q1 from `docs/topic_queue.md` and requires `docs/human_session.md` to contain the working title, `videos/002-<slug>`, one_line, fill-idea, no-write-idea note, `mark_topic.py --id Q1`, and the exact `new_packet.py "title"` line. Did not scaffold Q1. Did not edit needed.py. Did not add WAVE 4. Did not write idea.md. Did not map the new file in which_contract.
- **Result:** OPERATOR PIN CONTRACT PASS on a reconstructed docs + queue_lib tree (`python3 tools/operator_pin_contract.py`, exit 0). Queue rows remain queued. No new packet folder.
- **Verification status:** completed for the new contract (local PASS, exit 0). Full selftest / doctor against sample-001 not re-run (clone-less). No media.
- **Important discovery:** The Q1 pin lives only as prose. A later run that retitles Q1 or defers first-video commands again would not fail idea_gate. A two-file string lock is cheaper than another reconstruct wave.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After editing human_session or the Q1 queue row, run `operator_pin_contract.py`. Agents: --bootstrap then --plan; do not add WAVE 4; do not auto-write idea.md; do not auto-scaffold Q1.

## 2026-09-10T12:20:00Z — Run 048

- **Objective:** Lock the Run 047 fill-idea + expand refuse so a later edit cannot restore expand_prompt as the first live command on a blank idea.md.
- **Inspected:** STATE/NEXT/RUNS after Run 047. Q1 still queued. fill-idea exists only as unit notes. needed.py left untouched. which_contract left unmapped.
- **Action taken:** Added `tools/idea_gate_contract.py`. It checks blank/filled mechanism cases, `next_action.recommend` -> `fill-idea`, and `hint.commands_for` first live command = doctor. Uses tempfile only. Did not scaffold Q1. Did not edit needed.py. Did not add WAVE 4. Did not write idea.md. Did not map the new file in which_contract.
- **Result:** IDEA GATE CONTRACT PASS on a reconstructed-min tools tree (stubs matching current source strings + runtime recommend/hint). Queue rows remain queued. No new packet folder.
- **Verification status:** completed for the new contract (local PASS, exit 0). Full selftest / doctor against sample-001 not re-run (clone-less; fixture idea.md is filled so code stays expand-script). No media.
- **Important discovery:** Run 047's fill-idea map is cheap to regress because selftest only covers the filled fixture path. A tempfile contract covers the blank path without scaffolding Q1 or mapping a sixth reconstruct wave.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After scaffold, doctor should print `fill-idea` until the reprint is pasted. Agents: --bootstrap then --plan; run `idea_gate_contract.py` if fill-idea behavior is touched; do not add WAVE 4; do not auto-write idea.md.

## 2026-09-10T11:05:00Z — Run 047

- **Objective:** Stop doctor/hint from leading with `expand_prompt.py` on a just-scaffolded packet whose idea.md mechanism is still blank (that command now exits 2).
- **Result:** HINT FILL-IDEA UNIT PASS. NEXT_ACTION FILL-IDEA UNIT PASS.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-10T10:20:00Z — Run 046

- **Objective:** Stop expanding a just-scaffolded packet while idea.md still has a blank / template-default mechanism.
- **Result:** IDEA GATE UNIT PASS. SCAFFOLD CONTRACT PASS. expand_prompt exit 2 on blank mechanism.

## Earlier runs 001–45
See prior commits for full detail.
