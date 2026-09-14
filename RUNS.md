# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-14T07:12:00Z — Run 137

- **Objective:** While selected VO is blocked, stop the narration convention page from listing only the short packet-relative take path.
- **Inspected:** HEAD after Run 136. Printers, generated cards, editor.md, format.md, and selftest DROP-import / hint / format locks already exist. `docs/narration.md` Where-files table still listed `vo/NNN-slug-take-selected.wav` only as the role path, with the repo-root DROP only later as a Q1 example.
- **Action taken:** `docs/narration.md` now names `videos/NNN-slug/vo/NNN-slug-take-selected.wav` at the top of Where files live. `selftest.py` source-checks that narration.md keeps the DROP line (shared helper with format.md). Did not invent wav. Did not bump ready_for_edit. No new CLI. No WAVE 4. No Q2. Did not map forbidden tools.
- **Result:** A recorder using the narration page for file placement is told the same path the board and status gate check. A later narration rewrite that drops the DROP line fails selftest.
- **Verification status:** Files committed via GitHub file API. Official tools not executed against a full checkout in this sandbox (no clone). No wav on disk. Target column left in human_session step 3. Target comment left on hint write-script/expand-script.
- **Important discovery:** After format.md agreed, the remaining first-contact omit for *VO file placement* was narration.md — same short-path class as Run 136 format.md.
- **Blocker:** No selected VO file. HTTPS clone parked. Connected Voice exists but repo policy forbids inventing a selected take.
- **Recommended next action:** Record selected VO to the packet-relative path. Follow human_session Live job + steps 5–7. Do not invent wav. Do not `git add -f` the take. Do not drop it at repo-root `vo/`. Do not scaffold Q2. Do not upload. Do not add another Live job banner unless a first-contact lie is proven. Do not re-split selected_vo_drop.

## 2026-09-14T06:10:00Z — Run 136

- **Objective:** While selected VO is blocked, stop the format convention page from listing only the short packet-relative take path, and stop hint.py from quietly growing a second path builder.
- **Result:** An editor using the format page for named outputs is told the same path the board and status gate check. A later hint rewrite that rebuilds the path string fails selftest.
- **Blocker:** No selected VO file.

## 2026-09-14T05:20:00Z — Run 135

- **Objective:** While selected VO is blocked, stop future runs from silently rebuilding a second DROP string, and stop the editor convention page from omitting the packet-relative take path.
- **Result:** An editor opening the convention page is told the same path the board and status gate check. A later printer drift fails selftest instead of waiting for another alignment run.
- **Blocker:** No selected VO file.

## Earlier runs 001–134
See prior commits for full detail.
