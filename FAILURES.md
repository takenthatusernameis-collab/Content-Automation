# FAILURES

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

Earlier failures remain in prior commits.
