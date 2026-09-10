# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-10T11:05:00Z — Run 047

- **Objective:** Stop doctor/hint from leading with `expand_prompt.py` on a just-scaffolded packet whose idea.md mechanism is still blank (that command now exits 2).
- **Inspected:** STATE/NEXT/RUNS after Run 046. Q1 still queued. expand_prompt refuse exists. hint still mapped write-script/expand-script to expand_prompt with no fill-idea code. needed.py left untouched.
- **Action taken:** `next_action.recommend` returns `fill-idea` after drift checks when `expand_prompt.idea_mechanism_blank` is true. `hint.commands_for` maps that code to a paste comment plus `doctor.py`, not expand_prompt. Fixture sample-001 keeps a filled mechanism, so selftest's expected `expand-script` is unchanged. Did not scaffold Q1. Did not edit needed.py. Did not add WAVE 4. Did not change sample-001. Did not write idea.md.
- **Result:** HINT FILL-IDEA UNIT PASS. NEXT_ACTION FILL-IDEA UNIT PASS. Queue rows remain queued. No new packet folder.
- **Verification status:** completed for the recommend + hint map (local unit). Full selftest / doctor against sample-001 not re-run (clone-less; fixture idea.md is filled so code stays expand-script). No media.
- **Important discovery:** After expand_prompt refuses blank mechanisms, leftover labor is following the old hint line into that refuse. Changing the recommended code is cheaper than another reconstruct flag or auto-writing idea.md.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After scaffold, doctor should print `fill-idea` until the reprint is pasted. Agents: --bootstrap then --plan; do not add WAVE 4; do not auto-write idea.md.

## 2026-09-10T10:20:00Z — Run 046

- **Objective:** Stop expanding a just-scaffolded packet while idea.md still has a blank / template-default mechanism.
- **Result:** IDEA GATE UNIT PASS. SCAFFOLD CONTRACT PASS. expand_prompt exit 2 on blank mechanism.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-10T09:05:00Z — Run 045

- **Objective:** Stop operators from reopening topic_queue.md after every scaffold just to copy the one_line into idea.md.
- **Result:** idea_followup reprint. SCAFFOLD CONTRACT PASS.

## Earlier runs 001–044
See prior commits for full detail.
