# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-13T17:05:00Z — Run 123

- **Objective:** While selected VO is blocked, close the last documented path that still told a human to record at repo-root `vo/`.
- **Inspected:** HEAD after Run 122. Operator pages, narration, NEXT, gitignore, and DECISIONS already required packet-relative Selected VO. `BLOCKED.md` TTS/mic row still said `vo/NNN-slug-take-selected.wav`.
- **Action taken:** Updated BLOCKED.md setup path to `videos/NNN-slug/vo/NNN-slug-take-selected.wav` and stated repo-root `vo/` is not Selected VO. Recorded the decision. Did not invent wav. Did not bump ready_for_edit. No new CLI. No Q2. Did not map forbidden tools. Did not strip Target column.
- **Result:** A human reading BLOCKED.md before recording will place the take where `render_brief` / `set_status` look. Human gate is still the selected take.
- **Verification status:** BLOCKED.md committed via GitHub file API. Official tools not executed in this sandbox (no clone). No wav on disk. Target column left in human_session step 3.
- **Important discovery:** After operator pages and gitignore were aligned, the remaining in-repo path lie was the parked-dependency table.
- **Blocker:** No selected VO file. HTTPS clone parked. Connected Voice exists but repo policy forbids inventing a selected take.
- **Recommended next action:** Record selected VO to the packet-relative path. Follow human_session steps 5–7. Do not invent wav. Do not `git add -f` the take. Do not drop it at repo-root `vo/`. Do not scaffold Q2. Do not upload.

## 2026-09-13T16:20:00Z — Run 122

- **Objective:** While selected VO is blocked, enforce the existing keep-media-out-of-git rule so a recording session cannot commit binaries and fake present rows.
- **Result:** A recording session can drop the take at the packet path without that file entering git by default. Human gate is still the selected take.
- **Recommended next action:** Record selected VO to the packet-relative path. Do not invent wav. Do not `git add -f` the take.

## 2026-09-13T15:10:00Z — Run 121

- **Objective:** While selected VO is blocked, remove the path lie that would make a recorded take invisible to `set_status` / `render_brief`.
- **Result:** A recording session can place the file where the gate actually looks.

## 2026-09-13T14:15:00Z — Run 120

- **Result:** Operator path now covers ready_for_vo through the first legal publish-metadata edit.

## 2026-09-13T13:10:00Z — Run 119

- **Result:** Operator path now covers ready_for_vo through the first legal card refresh.

## 2026-09-13T12:25:00Z — Run 118

- **Result:** Operator path now covers ready_for_vo through the first legal status bump.

## 2026-09-13T11:14:00Z — Run 117

- **Result:** Upload tags are usable. Editor has a named presence list that will stay honest until files exist.

## 2026-09-13T10:20:00Z — Run 116

- **Result:** Editor has a named card list. Upload metadata exists as a stub. Status remains ready_for_vo.

## 2026-09-13T09:16:00Z — Run 115

- **Result:** Human can read the card and record to the named path. Caption stub exists. Status remains ready_for_vo.

## 2026-09-13T08:15:00Z — Run 114

- **Result:** Q1 ready_for_vo with validating title/thumb copy.

## 2026-09-13T07:10:00Z — Run 113

- **Result:** script.md holds spoken WORDS (952 IN BAND). status remained draft until Run 114.

## 2026-09-13T06:30:00Z — Run 112

- **Result:** First non-fixture draft.md WORDS (manual 941).

## 2026-09-13T06:20:00Z — Run 111 (other agent)

- **Result:** Packet exists. draft.md empty until Run 112.

## Earlier runs 001–110
See prior commits for full detail.
