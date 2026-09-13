# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-13T02:10:00Z — Run 107

- **Objective:** First empty-script expand.md hid beat targets, so the off-repo writer only saw Band landing if they opened the writer prompt. Put the same allocation on the budget table that expand_prompt already pastes.
- **Inspected:** STATE/NEXT/FAILURES after Run 106. expand_brief skipped the table when spoken WORDS were 0. Template script already has hook/payoff/4 beats/CTA headings.
- **Action taken:** `tools/expand_brief.py` now builds the budget from headings even when have=0. Beat wants clamp to 140-220 (four empty beats → 220). Hook empty want=28. Did not touch needed.py, WAVE 3, doctor, which_contract.MAP, writer prompts, idea_brief, new_packet, or scaffold Q1. No new CLI.
- **Result:** Dry-run on empty template script prints hook 28 / payoff 60 / beats 220×4 / CTA 50. Queue still queued. No new packet. No media.
- **Verification status:** Local dry-run against videos/_template/script.md completed. expand_brief.py syntax compiled. HTTPS clone still parked. Completed file write via GitHub file API. Did not run prove_locks (not a write-path / words.py edit).
- **Important discovery:** 4 beats capped at 220 plus hook/payoff/CTA cannot reach the 1200 target; they land near 1010, which is still inside 900-1500. Clamping beats is correct; raising beat max would fight the writer contract.
- **Blocker:** Human-owned non-fixture draft still missing. HTTPS clone unavailable; do not retry it first.
- **Recommended next action:** Human follows docs/human_session.md on Q1 and overwrites the copied draft.md using expand.md Target. Do not add another needed.py reconstruct path unless a READY lie is proven. Do not add a fourth new_packet followup. Do not rewrite writer prompts unless that first draft misses band.

## 2026-09-13T01:05:00Z — Run 106

- **Objective:** After Run 105 copied draft.md into every new packet, make scaffold stdout name that file as the overwrite target so the human does not invent a second draft path.
- **Action taken:** Added `draft_followup()` to `tools/new_packet.py` and locked the reprint in `tools/scaffold_contract.py`.
- **Result:** Scaffold stdout now says overwrite the copied draft.md and that it is not script.md. Queue still queued.

## Earlier runs 001–105
See prior commits for full detail.
