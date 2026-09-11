# FAILURES

## 2026-09-11 — write_path_contract committed as docstring only (Run 066)

- **Tried:** Run 066 recorded WRITE PATH CONTRACT PASS after adding tempfile subprocesses.
- **Evidence:** After that commit, tools/write_path_contract.py was 986 bytes and contained only the module docstring. No main(), no subprocess, no PASS printer.
- **Lesson:** A memory-file PASS is not the lock. The executable file has to be in the same commit.
- **Avoid:** Updating STATE/RUNS to PASS without checking the committed byte size of the contract.

## 2026-09-10 — reconstruct-loop on needed.py (Runs 037–042)

- **Tried:** Six consecutive runs added reconstruct list flags.
- **Evidence:** Automated-step count rose while videos produced stayed 0.
- **Lesson:** Remaining labor is scaffolding Q1 and filling WORDS.
- **Avoid:** WAVE 4 or another needed.py flag unless a new clone-less guess appears after WAVE 3 READY.

## 2026-09-09 — treating clone failure as selftest unverified

- Clone failure is an access constraint, not a contract failure. Do not retry HTTPS clone as the first action.
