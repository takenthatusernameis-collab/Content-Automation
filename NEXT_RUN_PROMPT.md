# NEXT RUN PROMPT

Keep the original master prompt unchanged.

Targeted addition from Run 136:

- `docs/format.md` names `videos/NNN-slug/vo/NNN-slug-take-selected.wav` and states repo-root `vo/` is not Selected VO.
- `tools/selftest.py` source-checks that hint.py does not redefine `selected_vo_drop` / `selected_vo_path`, and that format.md keeps the DROP line.
- Do not invent a wav or card binaries. Do not bump ready_for_edit. Do not scaffold Q2. Do not add another wrapper CLI. Do not add WAVE 4. Do not upload.
- Do not spend the run adding another Q1 markdown stub or another operator/agent page that only restates NEXT.md.
- Do not re-implement selected_vo_drop in a second module.
- Next value is a real selected take at `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`, or an explicit human TTS policy.

Targeted addition from Run 135:

- `tools/selftest.py` source-checks that VO printers import `render_brief.selected_vo_drop` and that `set_status.py` does not redefine it.
- `docs/editor.md` names `videos/NNN-slug/vo/NNN-slug-take-selected.wav`.

Targeted addition from Run 134:

- `tools/caption_brief.py` imports `render_brief.selected_vo_drop()`. Generated captions.md prints `DROP videos/NNN-slug/vo/NNN-slug-take-selected.wav`. Export names and the Human box use the same helper.

Targeted addition from Run 133:

- `tools/qa_checklist.py` imports `selected_vo_drop()`. Generated qa.md Notes print DROP.

Targeted addition from Run 132:

- `tools/vo_session.py` imports `render_brief.selected_vo_drop()`. Generated vo_session.md prints DROP. Record-to uses the same helper.

Targeted addition from Run 131:

- `tools/render_brief.selected_vo_drop()` is the shared Selected VO path helper. pipeline_status and next_action import it. Generated render.md prints DROP. Table rows stay packet-relative.

Targeted addition from Run 130:

- tools/pipeline_status.py missing-VO packets print `DROP videos/NNN-slug/vo/NNN-slug-take-selected.wav`. Repo-root `vo/` is not Selected VO. This includes legal ready_for_vo (not only status-ahead-of-vo drift).

Targeted addition from Run 121:

- Selected VO is packet-relative only: `videos/NNN-slug/vo/NNN-slug-take-selected.wav` (or .flac, optional `-v2`). Repo-root `vo/` is ignored by `render_brief` / `set_status`.

Targeted addition from Run 110:

- hint.py write-script/expand-script Command must keep the empty-draft Target comment.
- Do not map doctor.py. Do not strip that comment.

Targeted addition from Run 109:

- `docs/human_session.md` step 3 must keep the empty-script Target column.

Targeted addition from Run 104:

- Do not touch needed.py reconstruct / WAVE 3 / doctor mapping unless a new READY lie is proven.
- Do not rewrite writer prompts again unless words.py on this draft misses 900-1500.

Targeted addition from Run 081:

- After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py` first.
- Do not map words.py, words_contract.py, placeholder_guard.py, or prove_locks.py.
