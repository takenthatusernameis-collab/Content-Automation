# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-14T05:20:00Z — Run 135

- **Objective:** While selected VO is blocked, stop future runs from silently rebuilding a second DROP string, and stop the editor convention page from omitting the packet-relative take path.
- **Inspected:** HEAD after Run 134. Printers and Q1 cards already share `selected_vo_drop()`. `docs/editor.md` named tracks but not DROP. `selftest.py` covered fixture gates only.
- **Action taken:** `selftest.py` source-checks that pipeline_status, next_action, caption_brief, qa_checklist, and vo_session import `selected_vo_drop` from `render_brief`, that render_brief still defines it, and that set_status reuses the helper instead of redefining it. `docs/editor.md` now names `videos/NNN-slug/vo/NNN-slug-take-selected.wav`. Did not invent wav. Did not bump ready_for_edit. No new CLI. No WAVE 4. No Q2. Did not map forbidden tools.
- **Result:** An editor opening the convention page is told the same path the board and status gate check. A later printer drift fails selftest instead of waiting for another alignment run.
- **Verification status:** Files committed via GitHub file API. Official tools not executed against a full checkout in this sandbox (no clone). No wav on disk. Target column left in human_session step 3. Target comment left on hint write-script/expand-script.
- **Important discovery:** After captions.md agreed, the remaining first-contact omit for the *edit* stage was editor.md. The compounding lock is monitoring the import, not another generated stub.
- **Blocker:** No selected VO file. HTTPS clone parked. Connected Voice exists but repo policy forbids inventing a selected take.
- **Recommended next action:** Record selected VO to the packet-relative path. Follow human_session Live job + steps 5–7. Do not invent wav. Do not `git add -f` the take. Do not drop it at repo-root `vo/`. Do not scaffold Q2. Do not upload. Do not add another Live job banner unless a first-contact lie is proven. Do not re-split selected_vo_drop.

## 2026-09-14T04:10:00Z — Run 134

- **Objective:** While selected VO is blocked, stop captions.md from telling a human to "read cues against the selected VO take" without naming the DROP path the board/gate already print.
- **Result:** An operator who opens the captions card to align cues is told the same path the board and status gate check.
- **Blocker:** No selected VO file.

## 2026-09-14T03:06:00Z — Run 133

- **Objective:** While selected VO is blocked, stop qa.md from listing mechanical PASS and an unchecked VO box without naming the Selected VO drop path the board/gate already print.
- **Result:** An operator who opens the QA card to tick VO is told the same path the board and status gate check.
- **Blocker:** No selected VO file.

## Earlier runs 001–132
See prior commits for full detail.
