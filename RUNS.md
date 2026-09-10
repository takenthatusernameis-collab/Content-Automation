# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-10T08:18:00Z — Run 044

- **Objective:** Stop operators from inventing a Q1 title/path and expanding from the generic idea.md mechanism.
- **Inspected:** STATE/NEXT/RUNS after Run 043. human_session used placeholder `"Working title that states the viewer job"` and `videos/002-slug`. script_expander had no pre-expand idea.md gate. Queue Q1 still queued. needed.py left untouched.
- **Action taken:** Pinned Q1 working title and predicted folder on `docs/human_session.md`. Added an idea.md problem/mechanism edit from the Q1 one_line before expand_prompt. Same pre-expand note on `prompts/script_expander.md`. Did not scaffold Q1. Did not edit needed.py. Did not add WAVE 4. Did not change sample-001. Did not retry clone as the first action.
- **Result:** Operator page is copy-paste through Q1 scaffold + mark + idea edit + expand/apply/status dry-run. Queue rows remain queued. No new tool runtime. No new packet folder.
- **Verification status:** completed for the operator-page pin (files on main). Reconstruct/contract runtimes not re-run (no tool-body change). No media.
- **Important discovery:** After first-video commands exist, leftover labor is title/path guessing and expanding from the scaffold default mechanism. Pinning those two items is cheaper than another printer.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` using the pinned Q1 title, edits idea.md, then expand_prompt / apply_script / set_status dry-run. Agents: --bootstrap then --plan; do not add WAVE 4; do not edit needed.py unless a new guess appears after WAVE 3 READY.

## 2026-09-10T07:15:00Z — Run 043

- **Objective:** Stop operators from hunting prior commits for the first-video expand/apply/status commands, and flag the six-run needed.py reconstruct loop.
- **Result:** Operator page self-contained through ready_for_vo dry-run. Reconstruct-loop flagged.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-10T06:12:00Z — Run 042

- **Objective:** Stop clone-less agents from guessing how to reconstruct `queue_status.py` after WAVE 3 prints the operator command.
- **Result:** PLAN_OPERATOR_RECON in WAVE 3. Local PASS.

## 2026-09-10T05:12:00Z — Run 041

- **Objective:** Stop clone-less agents from guessing the first operator command after reconstruct is READY.
- **Result:** WAVE 3 operator line. Local PASS.

## 2026-09-10T04:10:00Z — Run 040

- **Objective:** Stop clone-less agents from guessing the command after the first-fetch set is READY.
- **Result:** `--plan` WAVE 1 + WAVE 2. Local PASS.

## 2026-09-10T03:10:00Z — Run 039

- **Objective:** Stop clone-less agents from guessing the first files to fetch before needed.py can resolve names.
- **Result:** `--bootstrap`. Local PASS.

## 2026-09-10T02:05:00Z — Run 038

- **Objective:** Let clone-less agents see which reconstruct files are still absent, and resolve edited-tool names before which_contract is fetched.
- **Result:** `--missing` + FALLBACK_ALIAS. Local PASS.

## 2026-09-10T00:16:00Z — Run 037

- **Objective:** Stop clone-less agents from reconstructing the wrong file set from memory.
- **Result:** needed.py reconstruct list. Unmapped. Local PASS.

## Earlier runs 001–036
See prior commits for full detail.
