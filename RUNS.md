# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-12T13:30:00Z — Run 094

- **Objective:** Lock the documented rule that words.py --strict keys off the total band only, including an IN BAND draft that still prints idea-lock INFO.
- **Inspected:** STATE/NEXT after Run 093. words_contract proved BELOW/ABOVE exit 2 and that INFO prints, but never proved --strict exit 0 on IN BAND.
- **Action taken:** Added IN_BAND_DRAFT (~1048 spoken words) to tools/words_contract.py. Assert Result: IN BAND, INFO present, --strict exit 0. Did not edit words.py. Did not scaffold Q1. Did not write idea.md. Did not map words_contract.py. Did not turn INFO into FAIL.
- **Result:** Local words_contract PASS (exit 0). words_contract.py 5925 bytes. Queue still queued. No new packet. No media.
- **Verification status:** completed for local words_contract PASS on BELOW/ABOVE/IN BAND. unverified for live run against a real packet with idea.md (HTTPS clone blocked).
- **Important discovery:** Run 093 documented --strict band-only without an IN BAND lock. Treat the contract body as the lock, not the STATE sentence.
- **Blocker:** Human-owned non-fixture draft still missing. HTTPS clone unavailable; do not retry it first.
- **Recommended next action:** Human follows docs/human_session.md on Q1. Do not add another idea-lock wrapper or another words.py contract case unless the printer regresses.

## 2026-09-12T12:15:00Z — Run 093

- **Objective:** Fold apply_script.idea_lock_notes into words.py so idea_lock.py is not a required extra command.
- **Result:** words.py 15563 bytes with the fold. words_contract PASS locally.

## 2026-09-12T11:12:00Z — Run 092

- Added unmapped tools/idea_lock.py.

## 2026-09-12T10:20:00Z — Run 091

- apply_script.py idea_lock_notes() prints INFO only.

## Earlier runs 001–90
See prior commits for full detail.
