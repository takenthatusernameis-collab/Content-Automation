# FAILURES

## 2026-09-19 — dry-run adapter treadmill while VO missing (Runs 213–226)

- **Tried:** After the 24h generated-VO fallback became authorized, successive runs added narration_adapter, card_generator, timeline, media_qa, youtube_upload, assemble, youtube_feedback, experiment_loop, complete, then ftyp/level/selftest locks around those printers.
- **Evidence:** Videos produced stayed 0. Estimated human minutes fell only on paper. Q1 never gained a git-visible or gate-machine Selected VO. Run 226 closed the last documented size>0 / junk-master hole in youtube_upload + selftest.
- **Lesson:** Once late-pipeline printers are fail-closed and locked on HEAD, more adapters or fixtures are not progress. The compounding step is on-disk media at the packet-relative DROP path, then running the existing gates.
- **Avoid:** A 95th dry-run CLI. Another selftest fixture without a proven HEAD regression. Inventing wav/mp4. Scaffolding Q2. Treating hold-status bookkeeping as production.

## 2026-09-14 — render.md table-only Selected VO path (Run 131)

- **Tried:** Runs 121-130 locked pages and printers to `videos/NNN-slug/vo/...`. Q1 render.md still listed only `vo/002-...-take-selected.wav`.
- **Evidence:** An operator who records from the packet presence file could still copy the short path and drop the take at repo-root `vo/`. Two tools also rebuilt the same DROP string.
- **Lesson:** Pin the generated presence file and put the path helper next to presence_rows.
- **Avoid:** WAVE 4. Mapping doctor.py. Inventing a wav. Another Live job banner. A second search at repo-root `vo/`. A second selected_vo_drop implementation.

## 2026-09-13 — generic missing-VO refuse on set_status (Run 129)

- **Lesson:** Pin the refuse string on the status gate, not only the next-action printers.

## 2026-09-13 — short Selected VO path on record-vo printers (Run 128)

- **Lesson:** Pin the printers that emit the drop path, not only the markdown pages.

## 2026-09-12 — placeholder overwrite of queue_status.py / words.py / apply_script.py

- **Lesson:** Never commit a placeholder path. Push the verified local file body only. Check committed size immediately.

Earlier failures remain in force in prior commits.
