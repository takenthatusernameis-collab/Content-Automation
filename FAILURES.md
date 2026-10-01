# FAILURES

## 2026-10-01 — killed mux left moov-missing mp4 (closed Run 252)

- **Tried:** Sandbox mux `ffmpeg -i silent.mp4 -i vo.wav -filter_complex '[1:a]apad[a]' ... -shortest new.mp4`.
- **Evidence:** Process Killed. ffprobe: moov atom not found; Invalid data. Duration printed as 12.98 then 23.02 on a different file. Same class as Run 249 incomplete 262192-byte ftyp-only mp4.
- **Lesson:** Exit 0 is not enough. assemble --execute must sniff ftyp/moov before deleting segments or pointing upload at the file.
- **Avoid:** Bare apad. Treating any file named master.mp4 as export_present.

## 2026-10-01 — end screen cut by -shortest (fixed Run 251)

- **Tried:** Run 249 segmented execute muxed the card concat (including a 20s end card) to the VO with `-shortest`.
- **Evidence:** HANDOFF duration 308.40s equals the VO, not VO+20. Run 251 synthetic: 2.00s VO against a 6.02s silent video produced 2.00s with the old mux and 6.00s with `apad=pad_dur`. Bare `apad` did not EOF; ffmpeg ran until killed.
- **Lesson:** Pad with a finite `pad_dur` equal to the end-screen reserve, then `-shortest`. Do not treat the r249 master as the finished export.
- **Avoid:** Restoring raw `0:a` / `1:a` maps with `-shortest`. Using bare `apad`. Uploading `q1-media-r249` `q1-master.mp4` as complete.

