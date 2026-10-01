# FAILURES

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

## 2026-10-01 — ten runs without a DROP-path copy (flagged Run 248)

- **Tried:** Run 247 already put matching bytes in a session zip. This run confirmed Drive listing sizes were unchanged, downloaded the same wav and seven cards, and matched sha256 again so this chat has a copy pack.
- **Evidence:** Wav sha256 still `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2` (27200958 bytes, 308.40 s, 44.1 kHz mono s16). Seven PNG sha256 values matched `cards.sha256`. Zip `q1-handoff-verified.zip` is 19908902 bytes. No share-permission tool and no GitHub release-upload tool. Packet status stayed `ready_for_vo`.
- **Lesson:** The bytes are not the missing piece. The agent cannot write the packet-relative DROP path. Session zips, Drive checksums, and state-page updates have repeated across runs 239–248 without that copy. Treat another packaging run as the stall unless the operator says the zip was lost.
- **Avoid:** Regenerating while the Drive sizes match. Calling the zip Selected VO. A public-link fetcher. Another same-day Drive re-download. Another documentation-only commit that only restates this hold.

## 2026-10-01 — session zip is not the DROP path (flagged Run 247)

- **Tried:** After Runs 244–246 left matching bytes on Drive and proved anonymous curl is a login wall, this run downloaded those bytes into the operator session and zipped them for a human copy.
- **Evidence:** Wav sha256 matched `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2` (27200958 bytes, 308.40 s). Seven PNG sha256 values matched `cards.sha256`. Zip `q1-handoff-verified.zip` is 19908838 bytes. Packet status stayed `ready_for_vo`. No packet checkout received the files.
- **Lesson:** A chat zip can be the human copy source for that session. It does not clear Selected VO. Run 244 already showed session artifacts disappear for the next agent. Runs 239–247 have not performed the packet-relative copy. Another checksum commit is the stall.
- **Avoid:** Regenerating while the Drive sizes match. Calling the zip Selected VO. A public-link fetcher. Another same-day Drive re-download unless the operator says the zip was lost.

Earlier failures remain in force in prior commits. The 2026-10-01 rows before Run 248 are unchanged in git history at `7c688b10e10573634cfcb943a4cf96ea65a71591`.
