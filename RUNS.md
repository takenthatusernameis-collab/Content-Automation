# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-11T11:10:00Z — Run 070

- **Objective:** Stop a reconstructed tree from running write_path_contract.py alone while contract_shape.py was never fetched. Make the advertised shape-then-contract order one command.
- **Inspected:** STATE/NEXT/RUNS/FAILURES after Run 069. contract_shape.py already witnesses the trio. write_path_contract.py / apply_script.py / set_status.py unchanged. Remaining labor is still human Q1 scaffold + WORDS in band.
- **Action taken:** Added tools/verify_write_path.py. It subprocess-runs contract_shape.py then write_path_contract.py, stops on first non-zero, writes nothing, imports neither lock. Did not edit write_path_contract.py, apply_script.py, set_status.py, contract_shape.py, or needed.py. Did not scaffold Q1. Did not write idea.md.
- **Result:** Order wrapper committed. Local compile OK. Local run in this sandbox FAILs as expected (no sibling tools tree; missing contract_shape.py). Queue rows remain queued. No new packet folder. No media.
- **Verification status:** completed for committed verify_write_path.py syntax and missing-sibling FAIL. Runtime VERIFY WRITE PATH PASS requires contract_shape.py + write_path_contract.py + the trio they inspect, on disk. Did not claim WRITE PATH CONTRACT PASS or CONTRACT SHAPE PASS this run.
- **Important discovery:** Two correct locks still fail if the operator only runs the second one after a partial reconstruct.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After a tools reconstruct, run `python3 tools/verify_write_path.py`. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1. Do not add another shape-lock file unless a new emptied-file failure is observed.

## 2026-09-11T10:05:00Z — Run 069

- **Objective:** Stop a missing or emptied apply_script.py / set_status.py from looking healthy when only write_path_contract.py is shape-checked.
- **Inspected:** STATE/NEXT/RUNS/FAILURES after Run 068. contract_shape.py only inspected write_path_contract.py. apply_script.py 8332 bytes, set_status.py 6222 bytes, write_path_contract.py 13919 bytes still present in tree.
- **Action taken:** Extended tools/contract_shape.py to also fail if apply_script.py or set_status.py is missing, under size floor (4000 / 3000), docstring-only, or missing CLI markers (--from, draft.md, --write, --refresh, sample-001, ready_for_vo, --to). Did not edit write_path_contract.py, apply_script.py, or set_status.py. Did not scaffold Q1. Did not write idea.md.
- **Result:** Trio shape lock committed. Local compile OK. Local run in this sandbox FAILs as expected (no sibling tools tree). Queue rows remain queued. No new packet folder. No media.
- **Verification status:** completed for committed contract_shape.py syntax and sibling marker list. Runtime CONTRACT SHAPE PASS requires the three sibling files on disk. Did not claim WRITE PATH CONTRACT PASS this run.
- **Important discovery:** A second-file witness that only watches one of three executables still cannot see a deleted sibling that the first file subprocess-runs.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After a tools reconstruct, run `python3 tools/contract_shape.py` then `python3 tools/write_path_contract.py`. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1.

## 2026-09-11T09:15:00Z — Run 068

- **Objective:** Prevent the Run 066 failure mode (STATE PASS while write_path_contract.py is docstring-only) from recurring. A lock that lives inside write_path_contract.py cannot catch its own deletion.
- **Inspected:** STATE/NEXT/RUNS/FAILURES after Run 067. write_path_contract.py already contains def main and the 062–067 subprocess locks (13919 bytes).
- **Action taken:** Added tools/contract_shape.py. It fails if write_path_contract.py is missing, under 8000 bytes, or lacks required markers. Did not edit write_path_contract.py, apply_script, or set_status. Did not scaffold Q1. Did not write idea.md.
- **Result:** Separate shape lock committed. Queue rows remain queued. No new packet folder. No media.
- **Verification status:** completed for committed contract_shape.py syntax and marker list. Runtime CONTRACT SHAPE PASS requires the sibling write_path_contract.py on disk.
- **Important discovery:** The executable under test cannot be the only witness that it still exists. Shape checks belong in a second file.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band.
- **Recommended next action:** Human follows `docs/human_session.md`.

## 2026-09-11T08:10:00Z — Run 067

- **Objective:** Restore `tools/write_path_contract.py` from a docstring-only file and lock the advertised in-band non-fixture `set_status.py --to ready_for_vo` success path.
- **Result:** Contract source restored in-repo. Runtime PASS requires sibling apply_script/set_status.
- **Recommended next action:** Human follows `docs/human_session.md`.

## 2026-09-11T07:25:00Z — Run 066

- **Objective:** Lock non-fixture apply --write / --refresh.
- **Result:** STATE claimed PASS, but the committed write_path_contract.py was docstring-only (Run 067 restored the body).
- **Recommended next action:** Human follows `docs/human_session.md`.

## Earlier runs 001–65
See prior commits for full detail.
