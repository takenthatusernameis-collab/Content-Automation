# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-19T12:10:00Z — Run 224

- **Objective:** Close the remaining media-QA export-decode gap without a new adapter and without inventing a master file.
- **Inspected:** HEAD after Run 223. Q1 still ready_for_vo, no git-visible take. media_qa decoded WAV PCM but treated any non-empty export path as irrelevant. assemble.py treated size>0 as EXPORT_EXISTS. complete.py treated size>0 as master_export_present. Roadmap item 60 listed export decode after ffmpeg as remaining.
- **Action taken:** Added stdlib `mp4_header_ok` (ftyp box at offset 4) in `tools/media_qa.py`. export_decodable joins the hard gate only when a file exists. Wired the same helper into `assemble.py` and `complete.py`. Extended selftest fixtures so a junk master.mp4 cannot PASS media_qa, cannot be EXPORT_EXISTS, and cannot flip master_export_present. No new CLI. No wav or mp4 committed.
- **Result:** A dummy export can no longer look like a finished video. Human-minute estimate 5.1 → 5.0. Automated steps stay 94.
- **Verification status:** Isolated ftyp helper checked on junk vs synthetic ftyp bytes. Selftest fixtures updated on HEAD. Full packet selftest against a clone was not executed (HTTPS clone still parked). Live PASS not attempted.
- **Important discovery:** size>0 is not evidence of a master. Header sniff is cheap and reusable across assemble and complete.
- **Blocker:** Packet-relative Selected VO still absent from any persistent machine the next agent can see. HTTPS clone parked. No OAuth env. No local master. No provider_video_id. No metrics.
- **Recommended next action:** On the gate machine, drop the selected take, generate cards, write timeline.md, run media_qa (expect level rows; export_decodable FAIL until a real encode), assemble.py without `--execute`, then complete.py (expect INCOMPLETE_MEDIA until files exist). Do not upload. Do not invent metrics. Do not write a dummy mp4. Do not `git add -f`. Do not scaffold Q2. Do not add another dry-run adapter.

## 2026-09-19T11:12:00Z — Run 223

- **Objective:** Close the remaining media-QA gap (loudness / silence / clip) without a new adapter and without inventing a Selected VO file.
- **Result:** Silent or clipped takes will fail before ffmpeg. Human-minute estimate 5.2 → 5.1. Automated steps stay 94.
- **Blocker:** Packet-relative Selected VO still absent.

## 2026-09-19T10:10:00Z — Run 222

- **Objective:** Land the experiment/complete selftest lock that Run 221 claimed but did not push to HEAD `tools/selftest.py`.
- **Result:** Claimed lock is now on HEAD. Automated steps stay 94.

## 2026-09-19T09:10:00Z — Run 221

- **Action taken:** Added `tools/complete.py`.

## 2026-09-19T08:03:00Z — Run 220

- **Action taken:** Added `tools/experiment_loop.py`.

## 2026-09-19T06:06:00Z — Run 219

- **Action taken:** Added `tools/youtube_feedback.py`.

## 2026-09-19T05:17:00Z — Run 218

- **Action taken:** Added `tools/assemble.py`.

## 2026-09-19T04:10:00Z — Run 217

See prior commits for Runs 217–213. Summary: youtube_upload.py READY_FOR_CREDENTIAL; media_qa.py READY_FOR_MEDIA; timeline.py PLAN_BUILT; card_generator.py READY_FOR_MEDIA; narration_adapter.py READY_FOR_MEDIA.

## 2026-09-18T23:23:00Z — Run 212

Hold honor. Deadline not yet eligible. Packet markdown-only; no vo/ dir.

## 2026-09-16 — Runs 138–211

Consecutive hold honors after OPERATOR_HOLD was written. Same blocker until Run 213 deadline.
