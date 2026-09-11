# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-11T12:04:00Z — Run 071

- **Objective:** Give the operator a one-command spoken-word band check on PATH/draft.md so they do not have to apply a draft to learn it is BELOW/ABOVE the 900–1500 band.
- **Inspected:** STATE/NEXT/RUNS/FAILURES after Run 070. Next already forbids another shape-lock file. Remaining labor is still human Q1 scaffold + WORDS in band. apply_script dry-run already reports counts, but only after a packet folder and a --from path exist.
- **Action taken:** Added tools/words.py. Read-only. Prefers PATH/draft.md over script.md. Reuses validate_packet counters. Prints IN BAND / BELOW / ABOVE / EMPTY / EXPAND PROMPT. --strict exits 2 when not IN BAND or when the text looks like expand_prompt stdout. Did not edit write_path_contract.py, apply_script.py, set_status.py, contract_shape.py, verify_write_path.py, or needed.py. Did not scaffold Q1. Did not write idea.md. Did not map words.py.
- **Result:** Band printer committed. Local compile OK. Runtime count requires sibling validate_packet.py on disk. Queue rows remain queued. No new packet folder. No media.
- **Verification status:** completed for committed words.py syntax. Runtime band numbers unverified in this sandbox (no sibling validate_packet.py). Did not claim WRITE PATH CONTRACT PASS or CONTRACT SHAPE PASS this run.
- **Important discovery:** Runs 068–070 already cover reconstruct order. The leftover human loop is expand → guess length → apply → duration WARN → expand again. A printer that reads draft.md cuts that loop without another lock file.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After saving PATH/draft.md, run `python3 tools/words.py PATH` before apply --write. After a tools reconstruct, run `python3 tools/verify_write_path.py`. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1. Do not add another shape-lock file unless a new emptied-file failure is observed. Do not map words.py.

## 2026-09-11T11:10:00Z — Run 070

- **Objective:** Stop a reconstructed tree from running write_path_contract.py alone while contract_shape.py was never fetched. Make the advertised shape-then-contract order one command.
- **Action taken:** Added tools/verify_write_path.py.
- **Result:** Order wrapper committed.
- **Recommended next action:** Human follows `docs/human_session.md`.

## 2026-09-11T10:05:00Z — Run 069

- **Objective:** Trio shape lock for apply_script / set_status.
- **Result:** contract_shape.py witnesses the write-path trio.
- **Recommended next action:** Human follows `docs/human_session.md`.

## Earlier runs 001–68
See prior commits for full detail.
