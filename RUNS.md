# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-10T07:15:00Z — Run 043

- **Objective:** Stop operators from hunting prior commits for the first-video expand/apply/status commands, and flag the six-run needed.py reconstruct loop.
- **Inspected:** STATE/NEXT/RUNS/PROGRESS after Run 042. needed.py --plan already prints WAVE 1 + WAVE 2 command + WAVE 3 reconstruct + operator. docs/human_session.md ended at mark_topic and said "follow expand_prompt -> apply_script as in prior versions."
- **Action taken:** Restored the first-video expand_prompt / apply_script / validate / set_status / vo_session commands on docs/human_session.md. Recorded the 037-042 reconstruct-loop in FAILURES.md. Did not edit needed.py. Did not add WAVE 4. Did not map needed.py. Did not scaffold Q1. Did not change sample-001. Did not retry clone as the first action.
- **Result:** Operator page is self-contained through ready_for_vo dry-run. Queue rows remain queued. No new tool runtime. needed.py body unchanged.
- **Verification status:** completed for the operator-page restore (file on main). Reconstruct/contract runtimes not re-run (no tool-body change). No media. No new packet folder.
- **Important discovery:** After WAVE 3 reconstruct + operator exist, more needed.py flags do not reduce human minutes. The missing labor was on the human page, not another fetch wave.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1 through scaffold, mark_topic, expand_prompt, apply_script, and set_status dry-run. Agents: --bootstrap then --plan; do not add WAVE 4; do not edit needed.py unless a new guess appears after WAVE 3 READY.

## 2026-09-10T06:12:00Z — Run 042

- **Objective:** Stop clone-less agents from guessing how to reconstruct `queue_status.py` after WAVE 3 prints the operator command.
- **Result:** PLAN_OPERATOR_RECON in WAVE 3. Local PASS.
- **Recommended next action:** Human runs queue_status then human_session.

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
