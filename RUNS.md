# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-10-01T17:30:00Z — Run 250

- **Objective:** Verify the Run 249 private release on a real checkout, then fix a live defect instead of packaging the same zip again.
- **Inspected:** STATE, NEXT, RUNS, HANDOFF, BLOCKED. `gh release view q1-media-r249` listed the wav, seven PNGs, and `q1-master.mp4`. Clone of main succeeded.
- **Action taken:** Downloaded the release. Checksums matched HANDOFF and master.sha256. Copied onto the local packet paths (not git add). narration_adapter, card inspect, media_qa PASS. complete.py INCOMPLETE_PUBLISH. youtube_upload.py YOUTUBE_AUTH_REQUIRED. selftest failed on extract_words returning empty. Fixed WORDS_RE to DOTALL with a VISUAL/heading stop. Labeled the single-graph assemble argv as do_not_copy_on_2gb. Did not bump status. Did not upload. Did not scaffold Q2. Did not regenerate media.
- **Result:** Live extract is 941 words (was 0). selftest PASS. Automated steps 96. Videos published stay 0. Human minutes stay 3.2. Packet status stays `ready_for_vo` in git.
- **Verification status:** Wav sha256 `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`. Master sha256 `abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53`. selftest PASS after the regex fix. Gates above observed on this checkout only.
- **Important discovery:** narration_adapter had been reporting words: 0 on every multiline script. The selftest miss was a real pipeline bug, not a fixture quirk.
- **Blocker:** YouTube OAuth still absent. Anonymous release download still fails because the repo is private.
- **Recommended next action:** Do not re-download `q1-media-r249` unless an asset is missing. Human sets YouTube OAuth if upload is wanted. Do not treat this checkout as the publish machine.

## 2026-10-01T17:05:00Z — Run 249

- **Objective:** Stop re-packaging the same Drive zip. Use the working GitHub token to check out the repo, find a real pipeline defect, and leave a durable media fetch that is not a session zip.
- **Inspected:** STATE, NEXT, RUNS, HANDOFF, BLOCKED, FAILURES, gate_machine. Clone with GH_TOKEN succeeded (the parked "clone always fails" note is stale for this sandbox). Drive wav and seven cards matched HANDOFF checksums. No share-permission tool.
- **Action taken:** Placed the existing Drive bytes on the local checkout (not git add). narration_adapter, card inspect, and media_qa passed. timeline.match_card mapped Beat 2–4 onto the Beat 1 card because the first token was the word "beat". Fixed match_card and locked it in selftest. Single-graph assemble --execute was killed on a 2 GB machine. execute now encodes one card at a time. Produced export/master.mp4 locally and published private release `q1-media-r249`. Did not upload to YouTube. Did not bump packet status. Did not scaffold Q2.
- **Result:** Card mapping is correct on the live packet. Local master is 6499414 bytes, 308.40 s, 1920x1080 h264 + aac, ftyp present, sha256 `abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53`. Release download of that asset matched the sha256. Automated steps 95 (segmented execute). Videos published stay 0.
- **Verification status:** Checksums matched before encode. Release re-download matched master sha256. selftest still fails on a pre-existing extract_words miss (`''`); the new card-match check did not add a failure. Master is not committed. Packet status stays `ready_for_vo` until a checkout has the DROP file.
- **Important discovery:** HTTPS clone works here when GH_TOKEN is present. The stall was not only the copy. The assembler would have shipped the wrong cards, and the single ffmpeg graph OOMs at 2 GB.
- **Blocker:** YouTube OAuth still absent. Anonymous release download still fails because the repo is private. Packet status was not bumped.
- **Recommended next action:** On a machine with gh auth, `gh release download q1-media-r249 -p '*-take-selected.wav' -p 'q1-master.mp4' -p '*.png'` into the packet paths, then narration_adapter and media_qa. Do not regenerate. Do not treat the release as a YouTube upload.

## 2026-10-01T15:11:00Z — Run 248

- **Objective:** Stop treating a missing agent workspace as lost media. Confirm the existing Drive handoff is still the same bytes, leave those bytes in this operator session, and flag the repeated copy stall. Do not regenerate. Do not claim Selected VO.
- **Inspected:** STATE, NEXT, HANDOFF, RUNS, FAILURES, BLOCKED, OPERATOR_HOLD. Drive folder `1ftaVyh8BWQeWp45TIyX7Hh1o0MPmGRev` still listed the wav at 27200958 bytes and the seven PNGs at the Run 245 sizes. No Drive permission tool and no GitHub release-upload tool. HTTPS clone not retried.
- **Action taken:** Downloaded the existing Drive wav, seven PNGs, and `cards.sha256` into this operator session (`q1-handoff/` and `q1-handoff-verified.zip`, 19908902 bytes) with `COPY_TO_PACKET.txt`. Checked sha256 and the wav header. Did not synthesize. Did not upload. Did not bump status. Did not scaffold Q2. Did not add a fetcher.
- **Result:** Checksums still match. Automated steps stay 94. Videos produced stay 0. Estimated human minutes stay 3.7. Packet status stays `ready_for_vo`.
- **Verification status:** Wav sha256 `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`, 27200958 bytes, 44.1 kHz mono s16, 308.40 s. Seven PNG sha256 values matched `cards.sha256`. Drive listing sizes unchanged. Not copied to a packet checkout. Not Selected VO.
- **Important discovery:** The stall is not missing bytes. It is that this agent cannot write the packet-relative DROP path (clone fails; binaries stay gitignored; Drive is not anonymously fetchable; no share or release-upload tool). Runs 239–248 have repeated handoff packaging instead of that copy.
- **Blocker:** Packet-relative Selected VO still absent. Flagged as suspicious: ten runs without a DROP-path file. Another session zip is not progress.
- **Recommended next action:** Human copies `q1-handoff-verified.zip` from this chat onto the gate machine using `COPY_TO_PACKET.txt`, then runs narration_adapter and card_generator --inspect-only. Next agent should not re-download unless the operator says this zip was lost.

## 2026-10-01T14:12:00Z — Run 247

- **Objective:** Stop re-checking Drive as if that were the gate. Put the already-verified wav and seven cards in the operator-visible session folder so a human can copy them. Do not regenerate. Do not claim Selected VO.
- **Inspected:** STATE, NEXT, HANDOFF, RUNS, OPERATOR_HOLD, FAILURES. Packet still blocked on the packet-relative DROP path. Runs 239–246 had not placed a file there. HTTPS clone not retried.
- **Action taken:** Downloaded Drive file `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` and the seven card ids through the connected Drive account into the operator session folder `q1-handoff/`. Checked sha256 against `HANDOFF.md` and `cards.sha256`. Wrote `COPY_TO_PACKET.txt` and `q1-handoff-verified.zip` (19908838 bytes). Did not synthesize. Did not upload. Did not bump status. Did not scaffold Q2.
- **Result:** Operator session has the matching bytes. Automated steps stay 94. Videos produced stay 0. Estimated human minutes stay 3.7. Packet status stays `ready_for_vo`.
- **Verification status:** Wav sha256 `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`, 27200958 bytes, 44.1 kHz mono s16, 308.40 s. Seven PNG sha256 values matched `cards.sha256`. Not copied to a packet checkout. Not Selected VO. Session artifacts are not durable for the next agent (Run 244).
- **Important discovery:** The connected Drive account can place the handoff in the current operator session. That is the human copy source for this run. It still does not clear the packet-relative gate.
- **Blocker:** Packet-relative Selected VO still absent. Flagged: runs 239–247 have not placed a file at the DROP path. Another Drive checksum is the stall.
- **Recommended next action:** Human copies `q1-handoff-verified.zip` onto the gate machine using `COPY_TO_PACKET.txt`, then runs narration_adapter and card_generator --inspect-only. Do not regenerate. Do not add a public-link fetcher.

Earlier runs remain in git history before this file was rewritten with the Run 248 entry. Run 246 and earlier summaries are in commit `7c688b10e10573634cfcb943a4cf96ea65a71591` and below.
