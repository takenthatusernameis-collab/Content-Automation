# FAILURES

## 2026-10-01 — r249 master treated as finished export (closed Run 253)

- **Tried:** Run 249 uploaded the segmented mux as `q1-master.mp4`. Duration matched the VO (308.40s), so the 20s end card was cut.
- **Evidence:** Run 253 re-encode with `apad=pad_dur=20` produced 328.40s, ftyp+moov, sha256 `4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546`. Release re-download matched.
- **Lesson:** The finished local export is `q1-media-r253` `q1-master-r253.mp4`. Do not re-encode unless that asset is missing.
- **Avoid:** Uploading `q1-media-r249` `q1-master.mp4`. Another checksum-only run of the truncated file.

## 2026-10-01 — killed mux left moov-missing mp4 (closed Run 252)

- **Tried:** Sandbox mux `ffmpeg -i silent.mp4 -i vo.wav -filter_complex '[1:a]apad[a]' ... -shortest new.mp4`.
- **Evidence:** Process Killed. ffprobe: moov atom not found; Invalid data. Same class as Run 249 incomplete 262192-byte ftyp-only mp4.
- **Lesson:** Exit 0 is not enough. assemble --execute must sniff ftyp/moov before deleting segments or pointing upload at the file.
- **Avoid:** Bare apad. Treating any file named master.mp4 as export_present.

## 2026-10-01 — end screen cut by -shortest (fixed Run 251)

- **Tried:** Run 249 segmented execute muxed the card concat (including a 20s end card) to the VO with `-shortest`.
- **Evidence:** HANDOFF duration 308.40s equals the VO, not VO+20. Run 251 synthetic: 2.00s VO against a 6.02s silent video produced 2.00s with the old mux and 6.00s with `apad=pad_dur`. Bare `apad` did not EOF; ffmpeg ran until killed.
- **Lesson:** Pad with a finite `pad_dur` equal to the end-screen reserve, then `-shortest`. Do not treat the r249 master as the finished export.
- **Avoid:** Restoring raw `0:a` / `1:a` maps with `-shortest`. Using bare `apad`. Uploading `q1-media-r249` `q1-master.mp4` as complete.

## 2026-10-01 — extract_words dropped every multiline WORDS block (fixed Run 250)

- **Tried:** narration_adapter.extract_words used `^WORDS:\s*(.*?)` without DOTALL. `.` never crossed the newline after `WORDS:`, so the match failed and the adapter printed words: 0. selftest reported `extract_words missed WORDS blocks: ''`.
- **Result:** Spoken-word count on the live packet was wrong. Duration and TTS callers that used this helper would have seen an empty script.
- **Lesson:** The existing selftest was the lock. words.py already used `re.S`. Match that, and stop at `VISUAL:` or the next `##` heading.
- **Avoid:** Treating the selftest miss as a pre-existing fixture to ignore.

## 2026-10-01 — Beat 2–4 encoded as Beat 1 (fixed Run 249)

- **Tried:** Dry-run assemble after placing the verified cards. The argv reused `cards/beat1-split-open-task-board-vs-one-index-car.png` for Beat 2, Beat 3, and Beat 4.
- **Evidence:** `match_card` returned the first card whose label started with the word "beat". Live packet rows confirmed the collapse. After the key fix, each beat mapped to its own PNG.
- **Lesson:** A shared prefix is not a beat identity. Lock the mapping. Do not encode from the old argv.
- **Avoid:** Restoring `t.startswith(beat.split()[0])`.

## 2026-10-01 — single-graph assemble killed at 2 GB (fixed in execute, Run 249)

- **Tried:** `assemble.py --execute` and the printed ffmpeg graph directly.
- **Evidence:** Process killed (exit 137) after a few seconds. Incomplete mp4 had ftyp and no moov (262192 bytes). Segmented encode then produced a 6499414-byte master.
- **Lesson:** The dry-run argv is not safe on a 2 GB machine. execute must stay segmented. Mux must use the packet `vo/` file, not the repo-relative drop string.
- **Avoid:** Treating a killed ffmpeg file as a master. Reverting execute to the single graph.

Earlier failures remain in force in prior commits.
