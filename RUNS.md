# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

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
