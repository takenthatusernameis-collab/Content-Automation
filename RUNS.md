## Run 1008 — 2026-11-04T02:20:00Z
- Objective: Add a reusable media QA signal for awkward start/end pauses on Selected VO without credentials, inventing media, or changing the existing hard gate.
- Action: Inspected STATE/NEXT/RUNS and media_qa.py. Extended tools/media_qa.py _wav_levels to compute leading_silence_s and trailing_silence_s from PCM (stdlib). Added soft vo_leading_silence / vo_trailing_silence reports (not in hard_names). No secrets polled, no dispatch, no media writes, no ffmpeg execute. Committed.
- Result: Videos published stay 0. media_qa now surfaces leading/trailing silence seconds for every future WAV packet. Estimated savings: 1-2 human minutes per future VO by catching long lead/trail pauses early. Pre-upload path unchanged. Gate behavior unchanged for existing hard checks.
- Verification: File updated and committed via push_files. Structure reuses existing stdlib PCM path. Soft checks only. No regressions to hard gate.
- Discovery: Soft silence-boundary reporting compounds media quality visibility across packets without requiring credentials or adding consistency printers.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or python3 tools/human_one_pager.py then secrets + single execute=true dispatch). Optional: python3 tools/media_qa.py on a packet with WAV.

# RUNS

## Run 1007 — 2026-11-04T01:30:00Z
- Objective: Reduce rediscovery and manual date arithmetic for the 7+3 day observation window once a private video id and uploaded_at exist, by integrating the exact due-date calculation into the single post-publish sequence command.
- Action: Inspected STATE/NEXT/RUNS and post_publish_sequence.py + observation_window.py. Extended tools/post_publish_sequence.py step 1 to parse uploaded_at and print due_at (+10 days), status (DUE/WAITING), and days_until. No secrets polled, no dispatch, no media writes, no ffmpeg execute. Committed.
- Result: Videos published stay 0. Post-publish sequence now prints the precise observation due date in one place. Estimated savings: 1-2 human minutes after first publish by eliminating separate observation_window.py run or manual calculation. Pre-upload path unchanged.
- Verification: File updated and committed via create_or_update_file. Structure reuses existing read-only printer pattern and datetime logic from observation_window.py. No regressions.
- Discovery: Inlining the fail-closed due-date printer into the consolidated after-publish sequence compounds clarity for the long-stalled system without requiring credentials or adding new consistency printers.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or python3 tools/human_one_pager.py then secrets + single execute=true dispatch). Optional: python3 tools/post_publish_sequence.py

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)
