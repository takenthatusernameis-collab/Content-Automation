# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-13T00:10:00Z — Run 104

- **Objective:** Break the reconstruct-loop watch. Make the first off-repo draft more likely to land in the 900–1500 spoken-word band so Q1 does not spend a human rewrite cycle.
- **Inspected:** STATE/NEXT/FAILURES after Run 103. Runs 099–103 all changed needed.py reconstruct. FAILURES flags that pattern. Q1 still queued. Writer prompts named the band but gave no per-segment allocation.
- **Action taken:** Added a Band landing table and a draft.md `spoken_words` comment convention to `prompts/script_writer.md`. Pointed `prompts/script_expander.md` at the same allocation. Did not touch needed.py, WAVE 3, doctor.py, which_contract.MAP, idea_brief, or scaffold Q1.
- **Result:** Writer contract now specifies hook 20–35 / payoff 40–70 / body beat 140–220 / CTA 40–80 / target ~1200. Queue still queued. No new packet. No media. No new CLI.
- **Verification status:** completed for prompt file writes via GitHub file API. Unverified against a real draft (no Q1 folder). words.py still owns the official count. Did not run prove_locks (no high-risk tool write).
- **Important discovery:** After five reconstruct runs, the next compounding lever is first-draft size, not another READY printer.
- **Blocker:** Human-owned non-fixture draft still missing. HTTPS clone unavailable; do not retry it first.
- **Recommended next action:** Human follows docs/human_session.md on Q1 and uses the Band landing table when expanding. Do not add another needed.py reconstruct path unless a READY lie is proven. Do not rewrite writer prompts again unless that first draft misses band.

## 2026-09-12T22:15:00Z — Run 103

- **Objective:** Stop `needed.py next_topic.py --missing` from printing READY when next_topic.py is absent. The name aliases to queue_contract, whose need list does not include next_topic.py.
- **Result:** Isolated tree with queue_contract files but no next_topic.py: `needed.py next_topic.py --missing` prints NOT READY. which_contract.MAP unchanged.
- **Recommended next action:** Human follows docs/human_session.md on Q1. Do not add another needed.py reconstruct path unless a READY lie is proven.

## 2026-09-12T21:15:00Z — Run 102

- **Objective:** Stop `needed.py doctor.py --missing` from printing READY when next_topic.py is absent even though WAVE 3 tells the agent to run next_topic after doctor.
- **Result:** Nine-file tree prints READY. Do not map doctor.py. Do not add WAVE 4.

## Earlier runs 001–101
See prior commits for full detail.
