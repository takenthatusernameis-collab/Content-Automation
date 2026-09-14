# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-14T00:20:00Z — Run 130

- **Objective:** While selected VO is blocked, stop pipeline_status from reporting missing disk without naming the Selected VO drop path the gate opens.
- **Inspected:** HEAD after Run 129. next_action / hint / set_status refuse already print `videos/NNN-slug/vo/...`. pipeline_status listed all-missing and status-ahead-of-vo without a DROP line. ready_for_vo is not DRIFT for missing VO, so the board hid the path unless status was already illegally ahead.
- **Action taken:** pipeline_status.inspect now stores vo_state + vo_drop via selected_vo_drop(). format_report prints a footer rule and a per-packet `DROP \`videos/{vid}-{slug}/vo/...\`` whenever Selected VO is not present. Did not add a Live job banner. Did not invent wav. Did not bump ready_for_edit. No new CLI. No WAVE 4. No Q2. Did not map forbidden tools.
- **Result:** An operator who runs the production board on Q1 is told the same path render_brief / next_action / set_status check.
- **Verification status:** Files committed via GitHub file API. Official tools not executed in this sandbox (no clone). No wav on disk. Target column left in human_session step 3. Target comment left on hint write-script/expand-script.
- **Important discovery:** After refuse strings and record-vo printers were pinned, the remaining short-path omit was the read-only board used to confirm presence.
- **Blocker:** No selected VO file. HTTPS clone parked. Connected Voice exists but repo policy forbids inventing a selected take.
- **Recommended next action:** Record selected VO to the packet-relative path. Follow human_session Live job + steps 5–7. Do not invent wav. Do not `git add -f` the take. Do not drop it at repo-root `vo/`. Do not scaffold Q2. Do not upload. Do not add another Live job banner unless a first-contact lie is proven.

## 2026-09-13T23:16:00Z — Run 129

- **Objective:** While selected VO is blocked, stop set_status from refusing ready_for_edit with a generic "Selected VO missing on disk" that hides the path the gate opens.
- **Result:** An operator who dry-runs set_status after dropping a take in the wrong place is told the same path render_brief / next_action check.
- **Blocker:** No selected VO file.

## 2026-09-13T22:19:00Z — Run 128

- **Result:** An operator who runs next_action or hint on Q1 is told the same path render_brief / set_status check.

## 2026-09-13T21:18:00Z — Run 127

- **Result:** An operator landing on production rules now sees the recording gate before session-start printers.

## 2026-09-13T20:08:00Z — Run 126

- **Result:** An operator landing on human_session now sees the recording gate before scaffold commands.

## 2026-09-13T19:15:00Z — Run 125

- **Result:** An agent landing on agent_session now sees the recording gate before reconstruct commands.

## 2026-09-13T18:05:00Z — Run 124

- **Result:** Opening README now names the remaining human gate before the fixture command list.

## 2026-09-13T17:05:00Z — Run 123

- **Result:** A human reading BLOCKED.md before recording will place the take where `render_brief` / `set_status` look. Human gate is still the selected take.

## 2026-09-13T16:20:00Z — Run 122

- **Result:** A recording session can drop the take at the packet path without that file entering git by default.

## 2026-09-13T15:10:00Z — Run 121

- **Result:** A recording session can place the file where the gate actually looks.

## Earlier runs 001–120
See prior commits for full detail.
