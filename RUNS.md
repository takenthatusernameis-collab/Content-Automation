# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-11T18:10:00Z — Run 077

- **Objective:** Run 076 restored words.py after placeholder GitHub writes. Add an unmapped lock so a future emptied or placeholder words.py fails before the next expand pass, without another printer line or a needed.py mapping.
- **Inspected:** STATE/NEXT/RUNS/FAILURES after Run 076. words.py already prints band, Delta, Hook Delta, Beats, Thin, Grow, and Cut. Remaining labor is still human Q1 scaffold + WORDS in band. Adding another printer line would be drift.
- **Action taken:** Added tools/words_contract.py. It checks words.py exists, is at least 8000 bytes, contains Grow/Cut/Hook Delta markers, and is not a placeholder. It subprocess-runs words.py --strict on two temp drafts: BELOW must print Grow and not Cut; ABOVE must print Cut and not Grow; both must exit 2. Writes nothing under videos/. Did not edit words.py, write_path_contract.py, apply_script.py, set_status.py, contract_shape.py, verify_write_path.py, or needed.py. Did not scaffold Q1. Did not write idea.md. Did not map words.py or words_contract.py.
- **Result:** Local contract logic PASS against a padded stub words.py (exit 0). Small stub (576 bytes) FAIL as designed. Runtime against committed words.py still requires both files on disk together (HTTPS clone blocked). Queue rows remain queued. No new packet folder. No media.
- **Verification status:** completed for contract source + stub runtime. partial for live words.py subprocess (no private-repo checkout of words.py in this sandbox). Did not claim WRITE PATH CONTRACT PASS this run.
- **Important discovery:** Printer-line inflation on words.py has diminishing returns. The documented failure mode is placeholder overwrite, which a second-file size+marker+subprocess lock can catch.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After saving PATH/draft.md, run `python3 tools/words.py PATH` and use Grow or Cut on the next edit. After reconstructing words.py, run `python3 tools/words_contract.py`. After a write-path reconstruct, run `python3 tools/verify_write_path.py`. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1. Do not add another words.py printer line unless a new heading-choice guess appears. Do not map words.py or words_contract.py.

## 2026-09-11T17:05:00Z — Run 076

- **Objective:** After words.py prints Grow for short drafts, an ABOVE draft still has no named heading to trim. Print one Cut line without adding another lock file.
- **Action taken:** Extended tools/words.py with ceiling_for and cut_line. Two intermediate GitHub writes used placeholders; restored words.py to 14879 bytes in the same run and recorded that in FAILURES.md.
- **Result:** Temp BELOW draft printed Grow and no Cut; temp ABOVE draft printed Cut and no Grow.

## 2026-09-11T16:25:00Z — Run 075

- **Objective:** Grow line for one heading to expand first.

## 2026-09-11T15:19:00Z — Run 074

- **Objective:** Beats + Thin printer.

## Earlier runs 001–73
See prior commits for full detail.
