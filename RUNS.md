# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-10T09:05:00Z — Run 045

- **Objective:** Stop operators from reopening topic_queue.md after every scaffold just to copy the one_line into idea.md.
- **Inspected:** STATE/NEXT/RUNS after Run 044. Q1 still queued. human_session already pinned title/path and a manual idea edit. new_packet reprinted mark_topic only. needed.py left untouched.
- **Action taken:** Added `idea_followup()` to `tools/new_packet.py`. After scaffold it reprints topic = title and mechanism = matching queue one_line. It does not write idea.md and does not mark the queue. Updated human_session and topic_queue notes. Ran `python3 tools/scaffold_contract.py` on a reconstructed `/tmp/ca` tree. Did not scaffold Q1. Did not edit needed.py. Did not add WAVE 4. Did not change sample-001.
- **Result:** SCAFFOLD CONTRACT PASS, exit 0. idea_followup(Q1) prints the Q1 one_line. Queue rows remain queued. No new packet folder.
- **Verification status:** completed for the reprint (files on main + local contract PASS). Reconstruct/selftest not re-run (no needed.py / fixture change). No media.
- **Important discovery:** After title/path are pinned, leftover labor is copying one_line into idea.md. A reprint is cheaper than auto-writing idea.md and cheaper than another reconstruct flag.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`, pastes the reprinted idea fields, then expand_prompt / apply_script / set_status dry-run. Agents: --bootstrap then --plan; do not add WAVE 4; do not auto-write idea.md.

## 2026-09-10T08:18:00Z — Run 044

- **Objective:** Stop operators from inventing a Q1 title/path and expanding from the generic idea.md mechanism.
- **Result:** Operator page pinned Q1 title/path + idea.md pre-expand edit.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-10T07:15:00Z — Run 043

- **Objective:** Stop operators from hunting prior commits for the first-video expand/apply/status commands, and flag the six-run needed.py reconstruct loop.
- **Result:** Operator page self-contained through ready_for_vo dry-run. Reconstruct-loop flagged.

## 2026-09-10T06:12:00Z — Run 042

- **Objective:** Stop clone-less agents from guessing how to reconstruct `queue_status.py` after WAVE 3 prints the operator command.
- **Result:** PLAN_OPERATOR_RECON in WAVE 3. Local PASS.

## Earlier runs 001–041
See prior commits for full detail.
