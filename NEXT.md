# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Record or generate a **selected VO take** for `videos/002-stop-deciding-what-to-work-on-every-morning` using `vo_session.md` and `docs/narration.md`. Place it at `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav` (or .flac). Repo-root `vo/` is ignored. README, BLOCKED.md, `.gitignore`, `docs/agent_session.md`, `docs/human_session.md`, `docs/production_rules.md` Human handoff, `tools/next_action.py`, `tools/hint.py`, `tools/set_status.py` missing-VO refuse, and `tools/pipeline_status.py` missing-VO DROP now agree on that path. Operator copy: `docs/human_session.md` Live job + steps 5–7. Do not invent a wav in-repo. Do not `git add -f` the take. Do not commit TTS as selected take unless a human names that policy.
2. After a real selected take exists: `python3 tools/vo_session.py PATH --force` then `python3 tools/set_status.py PATH --to ready_for_edit` dry-run; `--write` only if Selected VO present and gate still PASS.
3. After VO exists, build the 7 planned cards locally from `assets.md`. Do not commit binaries to make rows look ready. Re-run `render_brief.py --force` and `qa_checklist.py --force` when files exist.
4. Human-edit `publish.md` description + approve pin comment (`docs/human_session.md` step 7). Tags already trimmed (Run 117). Do not upload.
5. Do **not** add another wrapper CLI. Do **not** map doctor.py. Do **not** add another needed.py reconstruct path unless a READY lie is proven. Do **not** add a Band-landing reprint CLI. Do **not** scaffold Q2 yet. Do **not** add another operator/agent page that only restates this list. Do **not** add another Live job banner unless a first-contact lie is proven. First-contact surfaces already pinned: README, agent_session, human_session, production_rules Human handoff. Printers already name the packet-relative take (Run 128). set_status missing-VO refuse already names that path (Run 129). pipeline_status missing-VO DROP already names that path (Run 130).
6. Do **not** make apply_script or words.py idea-lock INFO a check() error or a status bump.
7. Do **not** map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / idea_brief.py / idea_brief_contract.py / doctor.py.
8. Do **not** attempt YouTube OAuth, TTS, ffmpeg, or publishing without credentials or a real VO file.
18. Do **not** run apply_script --write against sample-001.
22. Do **not** retry HTTPS clone after one failure.
27. Do **not** have new_packet or idea_brief write idea.md.
40. Do **not** treat draft.md as script.md.
56. Do **not** make words.py --strict fail on idea-lock INFO alone.
64. Do **not** strip the empty-script Target column from docs/human_session.md step 3.
65. Do **not** strip the Target comment from hint.py write-script/expand-script commands.
