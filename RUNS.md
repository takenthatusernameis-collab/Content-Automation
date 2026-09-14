# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-14T06:10:00Z — Run 136

- **Objective:** While selected VO is blocked, stop the format convention page from listing only the short packet-relative take path, and stop hint.py from quietly growing a second path builder.
- **Inspected:** HEAD after Run 135. Printers, generated cards, editor.md, and selftest DROP-import lock already exist. `docs/format.md` Named outputs table still listed `vo/NNN-slug-take-selected.wav` only. `hint.py` already reused `next_action.selected_vo_path` but selftest did not watch it.
- **Action taken:** `docs/format.md` now names `videos/NNN-slug/vo/NNN-slug-take-selected.wav` and states repo-root `vo/` is not Selected VO. `selftest.py` source-checks hint.py does not redefine `selected_vo_drop` / `selected_vo_path`, and that format.md keeps the DROP line. Did not invent wav. Did not bump ready_for_edit. No new CLI. No WAVE 4. No Q2. Did not map forbidden tools.
- **Result:** An editor using the format page for named outputs is told the same path the board and status gate check. A later hint rewrite that rebuilds the path string fails selftest.
- **Verification status:** Files committed via GitHub file API. Official tools not executed against a full checkout in this sandbox (no clone). No wav on disk. Target column left in human_session step 3. Target comment left on hint write-script/expand-script.
- **Important discovery:** After editor.md agreed, the remaining first-contact omit for *named outputs* was format.md — same short-path class as Run 131 render.md.
- **Blocker:** No selected VO file. HTTPS clone parked. Connected Voice exists but repo policy forbids inventing a selected take.
- **Recommended next action:** Record selected VO to the packet-relative path. Follow human_session Live job + steps 5–7. Do not invent wav. Do not `git add -f` the take. Do not drop it at repo-root `vo/`. Do not scaffold Q2. Do not upload. Do not add another Live job banner unless a first-contact lie is proven. Do not re-split selected_vo_drop.

## 2026-09-14T05:20:00Z — Run 135

- **Objective:** While selected VO is blocked, stop future runs from silently rebuilding a second DROP string, and stop the editor convention page from omitting the packet-relative take path.
- **Result:** An editor opening the convention page is told the same path the board and status gate check. A later printer drift fails selftest instead of waiting for another alignment run.
- **Blocker:** No selected VO file.

## 2026-09-14T04:10:00Z — Run 134

- **Objective:** While selected VO is blocked, stop captions.md from telling a human to "read cues against the selected VO take" without naming the DROP path the board/gate already print.
- **Result:** An operator who opens the captions card to align cues is told the same path the board and status gate check.
- **Blocker:** No selected VO file.

## Earlier runs 001–133
See prior commits for full detail.
