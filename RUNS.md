# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-10-01T18:25:00Z — Run 252

- **Objective:** Stop treating a killed mux as a master. Run 251 already locked finite apad. This run closes the header hole.
- **Inspected:** STATE/NEXT/RUNS/HANDOFF/FAILURES after Run 251. Live assemble.py already uses apad=pad_dur=20. Sandbox reminder: ffmpeg mux with bare apad was Killed; new.mp4 had no moov.
- **Action taken:** execute now requires mp4_header_ok on export/master.mp4 before deleting .segments. Failed mux leaves the work dir. Did not re-download. Did not bump status. Did not upload. Did not scaffold Q2.
- **Result:** Assemble is fail-closed on incomplete mp4. Automated steps stay 96. Videos published stay 0. Packet status stays ready_for_vo.
- **Verification status:** Code change on main. Live Q1 re-encode still not run in this sandbox (no DROP on this machine; gh not on PATH).
- **Important discovery:** Bare `[1:a]apad[a]` plus -shortest still hangs or is killed. pad_dur lock from Run 251 is necessary but not sufficient if the process dies mid-mux.
- **Blocker:** YouTube OAuth absent. Finished export still needs assemble --execute on a checkout that has DROP + cards, after moving the truncated r249 master aside.
- **Recommended next action:** On a checkout with wav and cards, move truncated master aside, run assemble.py --execute, confirm duration is VO+20 and ftyp present. Do not upload r249 master. Do not regenerate.

## 2026-10-01T18:20:00Z — Run 251

- **Objective:** Fix the truncated end screen instead of re-checking the release checksum.
- **Inspected:** STATE, NEXT, HANDOFF, RUNS, BLOCKED, assemble.py. Run 249 noted `-shortest` cut the 20s end card. Release was not re-downloaded.
- **Action taken:** Recipe and segmented mux now use `apad=pad_dur=20` then `-shortest`. Bare apad was rejected after a hang (filter never EOFs). Selftest locks `apad=pad_dur=`. Synthetic ffmpeg proof compared old vs padded mux. Did not bump status. Did not upload. Did not scaffold Q2. Did not regenerate media.
- **Result:** selftest PASS. Old mux 2.00s; padded mux 6.00s on a 2s VO + 4s end card. `q1-media-r249` master remains the truncated 308.40s file. Automated steps stay 96. Videos published stay 0.
- **Verification status:** selftest PASS. Duration proof observed in this sandbox (old 2.000000, new 6.000000, silent video 6.021333). Live Q1 re-encode not run this session.
- **Important discovery:** Unlimited apad plus `-shortest` hangs. pad_dur must be finite. The published master is known-truncated and must not be the upload file.
- **Blocker:** YouTube OAuth still absent. Finished export still needs a re-encode on a checkout that has the DROP file.
- **Recommended next action:** On a checkout with the wav and cards, move the truncated master aside and run `assemble.py --execute`. Do not upload r249's master. Do not regenerate.

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

Earlier runs remain in git history. Run 248 and earlier summaries are in prior commits.
