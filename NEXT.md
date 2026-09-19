# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Place a Selected VO take for `videos/002-stop-deciding-what-to-work-on-every-morning` at `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav` (or .flac) on the machine that runs gates. Generated audio is an authorized labeled fallback (`vo_origin.md` kind=generated). Repo-root `vo/` is ignored. Do not invent a wav in git. Do not `git add -f` the take. Inspect with `python3 tools/narration_adapter.py PATH`.
2. After a real selected take exists on disk: `python3 tools/vo_session.py PATH --force` then `python3 tools/set_status.py PATH --to ready_for_edit` dry-run; `--write` only if Selected VO present and gate still PASS. Keep `vo_origin.md` kind honest.
3. On the same machine: `python3 tools/card_generator.py PATH --write-manifest`. Requires Pillow. Writes gitignored 1920x1080 PNGs under `cards/`. Do not commit binaries. `--mark-ready` only after inspect-only reports all yes. Then `render_brief.py --force` and `qa_checklist.py --force`.
4. Human-edit `publish.md` description + approve pin comment (`docs/human_session.md` step 7). Tags already trimmed (Run 117). Do not upload.
5. Do **not** add another wrapper CLI. Do **not** map doctor.py. Do **not** scaffold Q2 yet. Do **not** add another operator/agent page that only restates this list. Do **not** re-implement `selected_vo_drop` in a second module.
6. Do **not** make apply_script or words.py idea-lock INFO a check() error or a status bump.
7. Do **not** map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / idea_brief.py / idea_brief_contract.py / doctor.py.
8. Do **not** attempt YouTube OAuth or publishing without credentials or a real VO file.
18. Do **not** run apply_script --write against sample-001.
22. Do **not** retry HTTPS clone after one failure.
27. Do **not** have new_packet or idea_brief write idea.md.
40. Do **not** treat draft.md as script.md.
56. Do **not** make words.py --strict fail on idea-lock INFO alone.
64. Do **not** strip the empty-script Target column from docs/human_session.md step 3.
65. Do **not** strip the Target comment from hint.py write-script/expand-script commands.
66. Do **not** re-implement `selected_vo_drop` in a second module.
67. Do **not** describe generated VO as a human recording.
68. Do **not** `git add -f` generated card PNGs.
