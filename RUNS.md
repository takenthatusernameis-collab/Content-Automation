# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-10T10:20:00Z — Run 046

- **Objective:** Stop expanding a just-scaffolded packet while idea.md still has a blank / template-default mechanism.
- **Inspected:** STATE/NEXT/RUNS after Run 045. Q1 still queued. new_packet reprints idea fields but expand_prompt still assembled a pack from blank idea.md. needed.py left untouched.
- **Action taken:** `expand_prompt.py` now exits 2 when the idea.md mechanism is empty, `template-default`, `generic`, `tbd`, or `todo`. It still does not write idea.md or script.md. `scaffold_contract.py` now locks `idea_followup` reprint of Q1 topic + one_line and the no-write-idea banner. Unit-tested the gate on template vs filled vs template-default text. Ran `python3 tools/scaffold_contract.py` on `/tmp/ca`. Did not scaffold Q1. Did not edit needed.py. Did not add WAVE 4. Did not change sample-001.
- **Result:** IDEA GATE UNIT PASS. SCAFFOLD CONTRACT PASS, exit 0. Queue rows remain queued. No new packet folder.
- **Verification status:** completed for the refuse + contract lock (local unit + contract PASS). Full expand_prompt assembler not re-run (depends on caption_brief/expand_brief/docs reconstruct). No media.
- **Important discovery:** After the reprint exists, leftover labor is skipping the paste. A refuse is cheaper than auto-writing idea.md and cheaper than another reconstruct flag.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`, pastes the reprinted idea fields, then expand_prompt (should print a pack only after the paste) / apply_script / set_status dry-run. Agents: --bootstrap then --plan; do not add WAVE 4; do not auto-write idea.md.

## 2026-09-10T09:05:00Z — Run 045

- **Objective:** Stop operators from reopening topic_queue.md after every scaffold just to copy the one_line into idea.md.
- **Result:** idea_followup reprint. SCAFFOLD CONTRACT PASS.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-10T08:18:00Z — Run 044

- **Objective:** Stop operators from inventing a Q1 title/path and expanding from the generic idea.md mechanism.
- **Result:** Operator page pinned Q1 title/path + idea.md pre-expand edit.

## Earlier runs 001–043
See prior commits for full detail.
