# Human session

One page. Follow this instead of scanning `tools/`.

`videos/sample-001-*` is a fixture. Never apply WORDS to it. Never promote it.

Agents without a checkout: `docs/agent_session.md`.

## Start every session

```bash
python3 tools/doctor.py
python3 tools/queue_status.py
```

Read the doctor block. Run only the printed Command (dry-run first). Doctor writes nothing. queue_status writes nothing. Default queue_status exit is 0. Use `--strict` only when you want a non-zero exit on mark-needed or missing-folder.

If a mark-needed folder already exists, `queue_status.py` prints `idea_brief.py PATH --block`, a paste-by-hand line, and `idea_brief.py PATH --check` under that folder. Follow those printed lines. Do not reopen this page to recover the paste.

If you still need a first real title:

```bash
python3 tools/next_topic.py
```

That command writes nothing. It prints a queued title, a predicted `videos/NNN-slug`, and a dry-run `mark_topic` line. After that predicted folder exists, it also prints `idea_brief.py PATH --block`, a paste-by-hand line, and `idea_brief.py PATH --check`. Prefer the printed title over inventing a new one. Prefer the printed idea_brief lines over scanning this page for the paste.

## First real video (not the fixture)

1. Scaffold the printed queue title (Q1 today)

```bash
python3 tools/queue_status.py
python3 tools/next_topic.py
python3 tools/new_packet.py "Stop deciding what to work on every morning"
python3 tools/doctor.py videos/002-stop-deciding-what-to-work-on-every-morning
python3 tools/queue_status.py
```

Use the exact Q1 working title from `docs/topic_queue.md` unless a human replaced that row. `new_packet` reprints the matching `mark_topic --id Q1` dry-run after the folder is created. It also reprints suggested `idea.md` topic + problem + mechanism (problem from the operator pin, mechanism from the queue `one_line`). It does not mark the row used and does not write idea.md. After scaffold, queue_status should show `mark-needed` for that id and the PACKET column from packet.md. Doctor Code should be `fill-idea` until idea.md is pasted.

If scaffold stdout is gone, reprint the same three fields without writing:

```bash
python3 tools/idea_brief.py videos/002-stop-deciding-what-to-work-on-every-morning
python3 tools/idea_brief.py videos/002-stop-deciding-what-to-work-on-every-morning --block
```

`idea_brief.py` writes nothing. It prints current idea.md fields and the suggested paste. `--block` prints only the paste-ready idea.md body. Still does not write idea.md.

After you paste that body into idea.md by hand, confirm without writing:

```bash
python3 tools/idea_brief.py videos/002-stop-deciding-what-to-work-on-every-morning --check
```

`--check` writes nothing. Exit 2 means the paste is still blank or does not match the suggested topic/problem/mechanism; stdout then prints the exact `python3 tools/idea_brief.py PATH --block` line. Exit 0 means PASTE READY; stdout then prints the exact `python3 tools/expand_prompt.py PATH` line and the dry-run `python3 tools/apply_script.py PATH --from PATH/draft.md` line for that packet. Expand off-repo. Save that draft to `videos/002-stop-deciding-what-to-work-on-every-morning/draft.md`. Do not treat expand_prompt stdout as script.md.

```bash
python3 tools/mark_topic.py --id Q1
# python3 tools/mark_topic.py --id Q1 --write
```

`mark_topic` writes nothing until `--write` and a matching non-fixture folder exist.

2. Replace the template mechanism before expanding

Scaffolded `idea.md` still uses blank template fields. Paste the reprint from `new_packet` or `idea_brief` (or the `--block` body, or write these if you skipped the reprint):

- topic: Stop deciding what to work on every morning
- problem: they reopen the whole work list every morning instead of starting
- mechanism: Install a written next-action default so the morning does not reopen the whole list.

Do not treat that edit as spoken WORDS. Do not invent statistics. Do not leave the template-default / blank mechanism. `expand_prompt.py` exits 2 until that paste exists. It does not write idea.md. `next_action.py` / `hint.py` / `doctor.py` stay on `fill-idea` until that paste exists; they will not lead with expand_prompt. `idea_brief.py --check` is the read-only confirm for that paste.

3. Expand off-repo, then paste back only onto the new packet

```bash
python3 tools/expand_prompt.py videos/002-stop-deciding-what-to-work-on-every-morning
# paste that pack into an off-repo writer; save the draft to videos/002-stop-deciding-what-to-work-on-every-morning/draft.md
# do not treat stdout as script.md
python3 tools/words.py videos/002-stop-deciding-what-to-work-on-every-morning
# expect Result: IN BAND before apply --write; --strict exits 2 otherwise (total band only)
# if BELOW, use Delta + Grow; if ABOVE, use Delta + Cut; if hook is not 20-35, use Hook Delta; use Beats + Thin as context; do not invent filler
python3 tools/apply_script.py videos/002-stop-deciding-what-to-work-on-every-morning --from videos/002-stop-deciding-what-to-work-on-every-morning/draft.md
# after dry-run OK:
python3 tools/apply_script.py videos/002-stop-deciding-what-to-work-on-every-morning --from videos/002-stop-deciding-what-to-work-on-every-morning/draft.md --write --refresh
python3 tools/validate_packet.py videos/002-stop-deciding-what-to-work-on-every-morning
```

`expand_prompt.py` pastes a live budget even when copied expand.md is still a stub. On an empty first draft use the Target column: hook 28 (20-35), payoff 60 (40-70), each of four beats 220 (140-220), CTA 50 (40-80), land ~1010 inside 900-1500. Follow `prompts/script_writer.md` Band landing. Do not wait for WORDS before using those targets. Do not invent filler to hit a heading.

`words.py` writes nothing. On a packet folder it prefers `draft.md` when that file exists. IN BAND is not apply --write. If it prints EXPAND PROMPT, the file is still expand_prompt stdout. Delta, Hook Delta, Beats, Thin, Grow, and Cut are counts, not permission to pad. `--strict` does not fail on hook length, thin headings, Grow, or Cut alone.

If expand_prompt prints `refusing expand: idea.md mechanism is blank or template-default`, or doctor prints `Code: fill-idea`, or `idea_brief.py --check` exits 2, go back to step 2. Do not run `apply_script.py --write` on `videos/sample-001-*`. Do not auto-write WORDS. Do not pad the fixture.

4. Promote only when spoken WORDS sit in the 900-1500 band

```bash
python3 tools/words.py videos/002-stop-deciding-what-to-work-on-every-morning --strict
python3 tools/set_status.py videos/002-stop-deciding-what-to-work-on-every-morning --to ready_for_vo
# after dry-run OK and no duration WARN:
python3 tools/set_status.py videos/002-stop-deciding-what-to-work-on-every-morning --to ready_for_vo --write
python3 tools/vo_session.py videos/002-stop-deciding-what-to-work-on-every-morning
```

Then record the selected take at the named path in `vo_session.md`. Do not invent a wav. Do not write an ffmpeg recipe.

5. After the selected take exists (do not invent the file)

Named path for Q1:

`vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`

Read `videos/002-stop-deciding-what-to-work-on-every-morning/vo_session.md` and `docs/narration.md`. Record or generate locally. Keep large raw takes out of git.

When that file is on disk:

```bash
python3 tools/vo_session.py videos/002-stop-deciding-what-to-work-on-every-morning --force
python3 tools/set_status.py videos/002-stop-deciding-what-to-work-on-every-morning --to ready_for_edit
# after dry-run OK and Selected VO present:
python3 tools/set_status.py videos/002-stop-deciding-what-to-work-on-every-morning --to ready_for_edit --write
```

`--force` refreshes the session card from WORDS. `set_status` still refuses `ready_for_edit` if the named take is missing. Do not bump from this page without the file. Do not scaffold Q2 while Q1 has no selected take. Do not write an ffmpeg recipe until VO + cards exist.

If unsure of the next command after any step, re-run `python3 tools/doctor.py videos/002-stop-deciding-what-to-work-on-every-morning` and use the printed Command.

## Stop

- Do not pad the fixture to clear Duration WARN.
- Do not treat the topic queue as a finished script.
- Do not mark a queue row used without a matching `videos/` folder.
- Do not expect `new_packet.py`, `idea_brief.py`, `queue_status.py`, or `words.py` to write the queue or idea.md.
- Do not treat `idea_brief.py --check` PASS as a written idea.md; it only compares.
- Do not treat `expand_prompt.py` stdout as a rewritten script.
- Do not treat `draft.md` as the finished `script.md` until apply_script `--write` succeeds.
- Do not treat `words.py` IN BAND as apply `--write`.
- Do not treat `words.py` Delta, Hook Delta, Beats, Thin, Grow, or Cut as permission to invent filler.
- Do not promote while duration WARN is present.
- Do not expand while idea.md still says `template-default` / generic or blank mechanism.
- Do not treat start-of-session `queue_status.py` / `next_topic.py` as mark_topic-only after a folder exists; they print idea_brief --block / paste / --check.
- Do not ignore the Target column on an empty first draft.
- Do not invent a selected wav or treat TTS as selected unless a human names that policy.
- Do not bump `ready_for_edit` without the named take on disk.
