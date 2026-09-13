# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-13T01:05:00Z — Run 106

- **Objective:** After Run 105 copied draft.md into every new packet, make scaffold stdout name that file as the overwrite target so the human does not invent a second draft path.
- **Inspected:** STATE/NEXT/FAILURES after Run 105. Template draft.md exists. human_session already says save to PATH/draft.md. new_packet printed mark + idea followups only.
- **Action taken:** Added `draft_followup()` to `tools/new_packet.py` and locked the reprint in `tools/scaffold_contract.py`. Did not touch needed.py, WAVE 3, doctor.py, which_contract.MAP, writer prompts, idea_brief, template draft.md, or scaffold Q1. No new CLI.
- **Result:** Scaffold stdout now says overwrite the copied draft.md and that it is not script.md. Queue still queued. No new packet. No media.
- **Verification status:** Python syntax checked locally. scaffold_contract not executed against a full sibling tree in this sandbox (HTTPS clone still parked). Completed file write via GitHub file API. Did not run prove_locks (not a write-path / words.py edit).
- **Important discovery:** Template file alone does not tell the operator which path to overwrite after expand. The existing new_packet printer is the right place; a new CLI would have been a wrapper.
- **Blocker:** Human-owned non-fixture draft still missing. HTTPS clone unavailable; do not retry it first.
- **Recommended next action:** Human follows docs/human_session.md on Q1 and overwrites the copied draft.md. Do not add another needed.py reconstruct path unless a READY lie is proven. Do not add a fourth new_packet followup. Do not rewrite writer prompts unless that first draft misses band.

## 2026-09-13T00:25:00Z — Run 105

- **Objective:** Give every new packet a draft.md save target so the human does not invent the file path or the spoken_words comment after expand.
- **Inspected:** STATE/NEXT/FAILURES after Run 104. Writer prompts already name Band landing. Q1 still queued. videos/_template had script.md but no draft.md.
- **Action taken:** Added `videos/_template/draft.md` with the spoken_words HTML comment, empty WORDS/VISUAL skeleton matching script.md headings, and an explicit not-script.md banner. Did not touch needed.py, WAVE 3, doctor.py, which_contract.MAP, writer prompts, idea_brief, or scaffold Q1. No new CLI.
- **Result:** `new_packet` copytree will include draft.md. Queue still queued. No new packet. No media.
- **Verification status:** completed for the template file write via GitHub file API. Unverified against a live new_packet run in this sandbox (HTTPS clone still parked). words.py still owns the official count. Did not run prove_locks (template only; no high-risk tool write).
- **Important discovery:** Run 104 put allocation in prompts; Run 105 puts the save-target file on the packet so the first overwrite has the right headings.
- **Blocker:** Human-owned non-fixture draft still missing. HTTPS clone unavailable; do not retry it first.
- **Recommended next action:** Human follows docs/human_session.md on Q1 and overwrites the copied draft.md. Do not add another needed.py reconstruct path unless a READY lie is proven. Do not rewrite writer prompts unless that first draft misses band. Do not add a second draft template.

## 2026-09-13T00:10:00Z — Run 104

- **Objective:** Break the reconstruct-loop watch. Make the first off-repo draft more likely to land in the 900–1500 spoken-word band so Q1 does not spend a human rewrite cycle.
- **Action taken:** Added a Band landing table and a draft.md `spoken_words` comment convention to `prompts/script_writer.md`. Pointed `prompts/script_expander.md` at the same allocation.
- **Result:** Writer contract names hook 20–35 / payoff 40–70 / body beat 140–220 / CTA 40–80 / target ~1200. Queue still queued.
- **Recommended next action:** Human follows docs/human_session.md on Q1. Do not add another needed.py reconstruct path unless a READY lie is proven.

## 2026-09-12T22:15:00Z — Run 103

- **Objective:** Stop `needed.py next_topic.py --missing` from printing READY when next_topic.py is absent.
- **Result:** Isolated tree with queue_contract files but no next_topic.py: `needed.py next_topic.py --missing` prints NOT READY. which_contract.MAP unchanged.

## Earlier runs 001–102
See prior commits for full detail.
