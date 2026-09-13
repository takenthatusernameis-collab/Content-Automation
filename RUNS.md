# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-13T08:15:00Z — Run 114

- **Objective:** Unlock Q1 publish gate (validate_packet) and bump status to ready_for_vo if OK and no duration WARN. Fill titles/thumb if that is the only FAIL.
- **Inspected:** HEAD after Run 113. script.md applied (952 spoken). titles.md / thumbnail.md still empty templates. packet status draft.
- **Action taken:** Reconstructed packet locally (HTTPS clone still parked). validate_packet FAIL: 0 titles + missing on-image text. Generated titles.md + thumbnail.md with title_thumb_brief heuristics. Re-validate PASS and PASS --duration. set_status-equivalent check: gate empty, duration WARN none, current draft -> ready_for_vo one step. Wrote packet.md status ready_for_vo. Did not invent VO. No new CLI. No Q2 scaffold. Did not map forbidden tools.
- **Result:** Q1 is ready_for_vo with validating title/thumb copy. Remaining labor is selected VO + human title lock.
- **Verification status:** validate_packet executed in sandbox against reconstructed packet (script text matched HEAD SHA content). title/thumb generated locally then pushed. Official set_status.py not imported (pipeline_status/render_brief deps); status write matches set_status field rules.
- **Important discovery:** After script apply, the only publish-gate blockers were empty title/thumb templates. Filling those unblocked ready_for_vo without touching words.py.
- **Blocker:** No selected VO file. HTTPS clone parked. Official set_status.py import chain not executed in this sandbox.
- **Recommended next action:** Human lock Primary if desired. Record selected VO. Do not invent wav. Do not scaffold Q2.

## 2026-09-13T07:10:00Z — Run 113

- **Objective:** Official spoken-word count on Q1 draft, then apply to script.md if IN BAND.
- **Inspected:** HEAD after Run 112. Live packet draft.md present; script.md empty headings only; status draft.
- **Action taken:** Reconstructed packet locally (HTTPS clone still parked). Ran words.py-equivalent spoken-word rules on draft.md. Count **952 IN BAND** (~06:21 at 150 wpm). Hook 28 ok. Applied beat body onto `videos/002-.../script.md`. Did not run set_status. Did not refresh expand/vo/captions. Did not invent VO. No new CLI. No Q2 scaffold.
- **Result:** Q1 script.md now holds spoken WORDS. packet.md status remains draft.
- **Verification status:** Word count executed in sandbox against the live draft text. apply_script.py itself was not imported (caption_brief/validate_packet not fetched); script.md write matches extract_script heading wrap with draft comments stripped.
- **Important discovery:** Manual Run 112 count was 941; official-equivalent count is 952. Still IN BAND. Beat 3 is 221 vs writer allocation ceiling 220 — total band still OK; words.py beat hint is 80 so Grow does not fire.
- **Blocker:** Full-checkout words.py + apply --refresh + set_status still need the remaining tool imports. HTTPS clone parked.
- **Recommended next action:** validate_packet + set_status ready_for_vo dry-run. Then title_thumb_brief. Do not invent VO.

## 2026-09-13T06:30:00Z — Run 112

- **Objective:** Run 111 (other agent) scaffolded Q1 and pasted idea.md but left draft.md empty and the packet missing template files. Remaining labor was a first draft in band, not another Target reprint.
- **Inspected:** Live HEAD after commits 64c286b..c614594. Packet had idea.md + empty draft.md + empty script.md + packet.md only. Queue Q1 already used. STATE/NEXT still described Run 110 (docs lagged the scaffold).
- **Action taken:** Wrote spoken WORDS into `videos/002-.../draft.md` targeting hook 20-35 / beats 140-220 / total 900-1500 (manual count 941). Copied missing template files into the packet. Did not apply --write. Did not edit script.md. Did not map forbidden tools. No new CLI.
- **Result:** First non-fixture draft exists. script.md still empty. words.py official count unverified in this sandbox (no checkout). No media.
- **Verification status:** Packet files pushed (commit 3d671cd for draft+templates). Manual word count only. apply_script and words.py not executed here.
- **Important discovery:** Parallel Run 111 already auto-scaffolded Q1 despite the standing do-not-auto-scaffold rule. STATE was not updated in that burst. Inspect HEAD commits before acting.
- **Blocker:** HTTPS clone still parked. Official words.py count and apply --write need a machine that can run the tools against the packet.
- **Recommended next action:** `words.py` on PATH, then apply dry-run / `--write --refresh` if IN BAND. Do not scaffold Q2. Do not add a reprint CLI.

## 2026-09-13T06:20:00Z — Run 111 (other agent)

- **Action taken:** Scaffolded Q1 folder, filled idea.md, copied draft template, marked queue used (commits 64c286b, ff846a3, ba06f81, c614594). Did not write spoken WORDS.
- **Result:** Packet exists. draft.md still empty until Run 112.

## 2026-09-13T05:05:00Z — Run 110

- **Action taken:** hint.py write-script/expand-script Command includes empty-draft Target comment.

## Earlier runs 001–109
See prior commits for full detail.
