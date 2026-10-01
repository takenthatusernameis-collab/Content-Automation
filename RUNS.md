# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-10-01T12:20:00Z — Run 245

- **Objective:** Do not regenerate the wav. Confirm the Run 244 Drive take is still the same bytes, then leave the next media step (seven planned cards) durable on the same Drive folder. Do not claim Selected VO. Do not commit binaries.
- **Inspected:** STATE, NEXT, HANDOFF, FAILURES, RUNS, OPERATOR_HOLD, docs/gate_machine.md, live packet listing. Packet still 15 markdown files. No `vo/` directory. Drive folder `1ftaVyh8BWQeWp45TIyX7Hh1o0MPmGRev` still listed the wav at 27200958 bytes. HTTPS clone not retried.
- **Action taken:** Downloaded Drive file `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl`. sha256 matched `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`. Rendered the seven `assets.md` cards at 1920x1080 with the same layout rules as `tools/card_generator.py`. Uploaded the PNGs and `cards.sha256` to the handoff folder. Re-listed Drive and matched every PNG size. Did not `git add` binaries. Did not bump status. Did not scaffold Q2. Did not add a TTS or card wrapper.
- **Result:** Card handoff is seven Drive file ids in `HANDOFF.md`. Automated steps stay 94. Videos produced stay 0. Estimated human minutes stay 3.7. Packet status stays `ready_for_vo`.
- **Verification status:** Local sha256 match against HANDOFF.md. Drive folder listing shows wav 27200958 bytes and seven PNGs at 42073, 27644, 27977, 35279, 34701, 35053, 39935 bytes. Hook card inspected visually (title plus need text, not blank). Packet listing via GitHub file API still has no `vo/` and no `cards/`. Not run through `media_qa.py` or `card_generator.py --inspect-only` on a checkout. Not on the gate machine.
- **Important discovery:** The Drive file id survived the new workspace. Downloading it is enough; synthesis is no longer the recovery path. Cards have the same durability gap as VO until copied to the packet-relative paths.
- **Blocker:** Packet-relative Selected VO still absent. Flagged: runs 239–245 have not put a file at the DROP path. Another Drive upload does not clear that gate.
- **Recommended next action:** On the gate machine, copy the existing Drive wav and seven PNGs to the packet paths in `HANDOFF.md`, check sha256, then run narration_adapter / vo_session / card_generator --inspect-only / timeline / media_qa. Do not regenerate while those Drive sizes match. Do not commit the binaries.

## 2026-10-01T11:20:00Z — Run 244

- **Objective:** Stop the lost-sandbox-wav stall. Run 243's artifacts handoff was not durable. Recover the same bytes and leave a pointer the next agent can fetch. Do not claim Selected VO. Do not commit audio.
- **Inspected:** STATE, NEXT, HANDOFF, FAILURES, RUNS, OPERATOR_HOLD, docs/gate_machine.md, live packet listing. Packet still 15 markdown files. No `vo/` directory. Workspace artifacts empty at start. Drive search for the exact wav name returned no file. HTTPS clone not retried.
- **Action taken:** Regenerated 941 WORDS with edge-tts `en-US-AndrewNeural`. sha256 matched Run 243 (`758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`, 27200958 bytes). Created Drive folder `Content-Automation-handoff` (`1ftaVyh8BWQeWp45TIyX7Hh1o0MPmGRev`) and uploaded the wav. Re-searched Drive and confirmed file id `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` at 27200958 bytes. Did not `git add` the wav. Did not bump status. Did not scaffold Q2. Did not add a TTS wrapper.
- **Result:** Durable generated handoff is the Drive file, not the session artifacts path. Automated steps stay 94. Videos produced stay 0. Estimated human minutes stay 3.7. Packet status stays `ready_for_vo`.
- **Verification status:** Local sha256 match against HANDOFF.md. Drive files.list exact-name search returned the file id and size_bytes 27200958. Packet listing via GitHub file API still has no `vo/`. Not run through `media_qa.py` (no checkout). Not on the gate machine.
- **Important discovery:** Session artifacts writes do not appear in the connected Drive the next run can search. An explicit Drive upload with a recorded file id does. That still does not clear the packet-relative gate.
- **Blocker:** Packet-relative Selected VO still absent. No OAuth. No local master in the repo.
- **Recommended next action:** Download Drive file `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl`, copy it to the DROP path, check sha256, then run narration_adapter / vo_session / card_generator / timeline / media_qa. Do not regenerate while that Drive file lists 27200958 bytes. Do not commit the wav.

Earlier runs remain in git history before this file was rewritten with the Run 244 entry. Run 243 and earlier summaries are in commit `3f033837add2709337899990da4ed7983af7b1b4` and below.
