# NEXT_RUN_PROMPT

Use the original master prompt unchanged, plus these targeted additions:

## Bootstrap rule
If STATE.md exists, trust it over memory. Clone-less agents print needed.py --bootstrap and --plan. Do not treat those as a contract.

## Scope cap
Ship at most one new reusable capability per run. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1. Do not replace write_path_contract.py with a docstring-only file. If the file has no def main, restore the body before adding a new lock. Do not drop tools/contract_shape.py.

## Evidence rule
Do not record WRITE PATH CONTRACT PASS unless python3 tools/write_path_contract.py printed that line and the committed file contains def main. Run python3 tools/contract_shape.py first; do not treat STATE PASS as a substitute for CONTRACT SHAPE PASS. After apply_script or set_status edits, run contract_shape.py then write_path_contract.py. HTTPS clone fails; do not retry after one failure. Push via GitHub file APIs.

## Status-write rule
set_status dry-runs by default. Refuse fixture promotion and duration WARN. When WORDS are in band on a non-fixture draft, dry-run exits 0 and --write sets ready_for_vo only.

## Apply-script rule
Dry-run default. Refuse sample-001. --refresh only after --write on a non-fixture packet.

## Private repo
Push via GitHub file APIs. Do not retry HTTPS clone after it fails once in the run.
