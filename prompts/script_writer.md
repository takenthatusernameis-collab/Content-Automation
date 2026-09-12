# Script writer

Use this prompt when filling `script.md` for a packet. Bind every draft to `docs/production_rules.md` and `docs/channel.md`.

Do not write `script.md` directly. Save the model output as `PATH/draft.md`. `draft.md` is not `script.md` until `apply_script.py --write`.

## Input

Read, in order:

1. `docs/channel.md`
2. `docs/production_rules.md`
3. `docs/format.md`
4. The packet `idea.md` — treat topic, viewer, problem, mechanism, why now, and related as locks. If mechanism is blank or template-default, stop and run `python3 tools/idea_brief.py PATH --block` then paste, then `--check`. This prompt does not write idea.md.
5. The packet `research.md` if it has sources
6. The packet `expand.md` if it has a beat budget
7. The empty beat skeleton in `script.md`

## Task

Write spoken WORDS for:

- Hook (0:00–0:12)
- Payoff promise
- Beats 1–N (keep existing beat headings unless one is wrong)
- CTA

Keep VISUAL lines as short italic stage directions, not a second script.

## Constraints

- Hook is 20–35 spoken words.
- Hook and payoff must name the idea.md mechanism. Beats must show the viewer using that system.
- Payoff promise is one sentence: what the viewer can *do* after watching.
- 4–7 beats. Do not add extra `##` headings.
- Total spoken WORDS for `explainer-6-10min` must land in 900–1500 words (~6–10 minutes at 150 wpm). Target ~1200 words / 8 minutes. Do not pad with slogans; add concrete steps inside existing beats.
- Use `expand.md` Add column as a size hint only. Do not copy the budget table into WORDS.
- One CTA. Assign a single next action that can be finished in under two minutes.
- Tone: specific, calm, operational. No hustle slogans, no “unlock your potential,” no unverifiable statistics.
- If a number is required, it must already appear in `research.md` with a source. Otherwise use qualitative language.
- Do not invent personal anecdotes. Use “you” procedures.
- Mechanism must be a default, cue, checklist, or constraint — not a pep talk.
- If related is not `none published yet`, do not retell those videos.

## Output format

Replace only the empty `WORDS:` / `VISUAL:` bodies. Preserve heading text exactly so `tools/validate_packet.py` still finds:

- `## Hook (0:00–0:12)`
- `## Payoff promise`
- `## Beat N —`
- `## CTA`

After writing, save as `PATH/draft.md` on a *non-fixture* packet, then run:

```bash
python3 tools/words.py videos/<id>-<slug>
python3 tools/apply_script.py videos/<id>-<slug> --from videos/<id>-<slug>/draft.md
```

Apply dry-run prints idea-lock INFO (mechanism / topic token overlap). INFO does not block `--write`. If lock miss, rewrite hook/payoff before `--write --refresh`.

```bash
python3 tools/apply_script.py videos/<id>-<slug> --from videos/<id>-<slug>/draft.md --write --refresh
python3 tools/set_status.py videos/<id>-<slug> --to ready_for_vo
```

Only run set_status `--write` after WORDS are in band. Do not pad `videos/sample-001-*`; that packet is a fixture.
