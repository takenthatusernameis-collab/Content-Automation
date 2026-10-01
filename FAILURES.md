# FAILURES

## 2026-10-01 — session zip is not the DROP path (flagged Run 247)

- **Tried:** After Runs 244–246 left matching bytes on Drive and proved anonymous curl is a login wall, this run downloaded those bytes into the operator session and zipped them for a human copy.
- **Evidence:** Wav sha256 matched `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2` (27200958 bytes, 308.40 s). Seven PNG sha256 values matched `cards.sha256`. Zip `q1-handoff-verified.zip` is 19908838 bytes. Packet status stayed `ready_for_vo`. No packet checkout received the files.
- **Lesson:** A chat zip can be the human copy source for that session. It does not clear Selected VO. Run 244 already showed session artifacts disappear for the next agent. Runs 239–247 have not performed the packet-relative copy. Another checksum commit is the stall.
- **Avoid:** Regenerating while the Drive sizes match. Calling the zip Selected VO. A public-link fetcher. Another same-day Drive re-download unless the operator says the zip was lost.

## 2026-10-01 — anonymous Drive fetch is a login wall (flagged Run 246)

- **Tried:** After Runs 244–245 left the wav and seven cards on Drive, this run checked whether a gate machine could fetch file id `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` with an unauthenticated curl.
- **Evidence:** `curl -L` of `https://drive.google.com/uc?export=download&id=1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` returned HTTP 303 then an HTML Google sign-in page (`accounts.google.com`), not a wav. The same file downloaded through the connected Drive account still matched sha256 `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2` and 27200958 bytes. Packet status stayed `ready_for_vo`.
- **Lesson:** A Drive file id is durable for the connected account. It is not a public URL. Writing a curl or gdown one-liner into `docs/gate_machine.md` would not place Selected VO. Runs 239–246 have not performed the packet-relative copy.
- **Avoid:** Another upload while those Drive sizes match. Another checksum-only commit. A public-link fetcher under tools/. Calling the Drive file Selected VO.

## 2026-10-01 — Drive media is still not the gate (flagged Run 245)

- **Tried:** Run 244 uploaded the generated wav. Run 245 confirmed that file id still listed 27200958 bytes, matched sha256 on download, and uploaded the seven planned cards to the same folder.
- **Evidence:** Packet listing still has no `vo/` and no `cards/` directory. Drive folder listing matched the local PNG sizes. Videos produced stayed 0.
- **Lesson:** A recorded Drive file id survives agent workspaces. It does not clear `ready_for_vo`. Runs 239–245 have not performed the packet-relative copy. Treat another upload or another checksum note as the stall unless the DROP path listing changes.
- **Avoid:** Regenerating the wav while file `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` lists 27200958 bytes. Regenerating the seven cards while `HANDOFF.md` sizes match. Calling Drive files Selected VO or packet cards. Committing binaries. A TTS or card wrapper under tools/.

## 2026-10-01 — artifacts handoff still dies between agent runs (flagged Run 244)

- **Tried:** Run 243 wrote the generated wav under operator artifacts `handoff/` and stored only the sha256 in git. It treated that artifacts write as the handoff.
- **Evidence:** Run 244 opened an empty artifacts workspace. Drive search for the exact wav name returned no file. Packet listing still has no `vo/` directory. Regenerating the same edge-tts pass reproduced sha256 `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2` and 27200958 bytes. Uploading that file to Drive succeeded: file id `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl`, size_bytes 27200958.
- **Lesson:** Checksum-in-git plus a session artifacts path is not durable for the next agent. A Drive file id is. The file is still not Selected VO until it is copied to the packet-relative DROP path on the gate machine.
- **Avoid:** Another synthesis while Drive file `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` lists 27200958 bytes. Calling the Drive file Selected VO. Committing the wav. A TTS wrapper under tools/.

## 2026-10-01 — operator-downloadable sandbox wav did not survive (flagged Run 243)

- **Tried:** Run 242 synthesized a level-passing generated wav and told the next run not to regenerate unless the operator said the handoff was lost. It did not commit audio (correct) and did not leave a checksum in git.
- **Evidence:** Run 243 opened an empty artifacts workspace. Packet listing still has no `vo/` directory. The Run 242 file was not recoverable. Same size and peak/rms as Run 242 after a fresh edge-tts pass (27200958 bytes, peak=0.7713, rms=0.1012), so the synthesis is repeatable, but the file itself was not durable.
- **Lesson:** "Operator-downloadable" is false unless the file is in the operator artifacts folder for that session and the sha256 is in git (`HANDOFF.md`). Repeating synthesis without that record is the stall. Copy to the packet-relative DROP path is still the only step that clears the gate.
- **Avoid:** Another synthesis while `HANDOFF.md` checksum `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2` is current and the artifacts file exists. Committing the wav. Calling the handoff Selected VO. A TTS wrapper under tools/.

## 2026-10-01 — sandbox generated wav is not Selected VO (flagged Run 242)

- **Tried:** After Run 241 forbade another same-week heartbeat, this run synthesized Q1 WORDS (edge-tts, because apt cannot install espeak-ng here) into a 308.40s 44.1 kHz mono wav that passes media_qa level constants.
- **Evidence:** Packet listing still has no `vo/` directory. Audio was not committed. Run 213 already left a sandbox MP3 that did not clear `ready_for_vo`.
- **Lesson:** A disposable or operator-download wav does not move the gate. The compounding step is a copy onto the gate machine at the packet-relative DROP path. Regenerating the same take is not progress.
- **Avoid:** Committing the wav. Describing it as a human recording. Adding an edge-tts wrapper under tools/. Another synthesis run unless the operator says the handoff file was lost.

## 2026-10-01 — eleven-day gate-machine absence (flagged Run 241)

- **Tried:** Agent runs 239–240 froze architecture and waited for packet-relative Selected VO. No further agent commits until this heartbeat.
- **Evidence:** HEAD SHA stayed `20861fa` from 2026-09-20 through 2026-10-01. Q1 listing still has no `vo/` directory. Videos produced stayed 0. Automated steps stayed 94.
- **Lesson:** When the remaining labor is a file on a machine this agent cannot persist, more agent sessions cannot ship a video. Weekly heartbeat is enough to prove the stall; daily hold-verification is not.
- **Avoid:** Same-week hold-verification commits. Inventing sandbox wav as if it were gate-machine VO. A 95th adapter. Scaffolding Q2. Another README/printer reorder.

## 2026-09-20 — documentation-order treadmill (Runs 227–238, flagged Run 239)

- **Tried:** After late-pipeline printers were fail-closed (Run 226), successive runs aligned drop-page pointers, bootstrap reconstruct, WAVE 3 hold text, hold-before-scaffold order, and README first bash blocks.
- **Evidence:** Videos produced stayed 0. Automated steps stayed 94. Estimated human minutes fell only on paper (4.8 → 3.7). By Run 238 the live first commands already named the packet-relative drop. Run 239 found no remaining first-command stall on README or NEXT.
- **Lesson:** Once hold-before-scaffold is locked in printers, queue_contract, and README, more alignment is the stall. The compounding step is on-disk media at the DROP path, or no commit.
- **Avoid:** Another README/WAVE 3/hint/next_action reorder. Another NEXT do-not item that only restates the hold. Treating a state-page rewrite as production. A 95th adapter. Inventing wav/mp4. Scaffolding Q2.

Earlier failures remain in force in prior commits. The 2026-09-20 rows that were in this file before Run 243 are unchanged in git history.
