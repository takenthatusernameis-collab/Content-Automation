# Script writer

Use this prompt when filling `script.md` for a packet. Bind every draft to `docs/production_rules.md` and `docs/channel.md`.

## Input

Read, in order:

1. `docs/channel.md`
2. `docs/production_rules.md`
3. `docs/format.md`
4. The packet `idea.md`
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
- Payoff promise is one sentence: what the viewer can *do* after watching.
- 4–7 beats. Do not add extra `##` headings.
- Total spoken WORDS for `explainer-6-10min` must land in 900–1500 words (~6–10 minutes at 150 wpm). Target ~1200 words / 8 minutes. Do not pad with slogans; add concrete steps inside existing beats.
- Use `expand.md` Add column as a size hint only. Do not copy the budget table into WORDS.
- One CTA. Assign a single next action that can be finished in under two minutes.
- Tone: specific, calm, operational. No hustle slogans, no “unlock your potential,” no unverifiable statistics.
- If a number is required, it must already appear in `research.md` with a source. Otherwise use qualitative language.
- Do not invent personal anecdotes. Use “you” procedures.
- Mechanism must be a default, cue, checklist, or constraint — not a pep talk.

## Output format

Replace only the empty `WORDS:` / `VISUAL:` bodies. Preserve heading text exactly so `tools/validate_packet.py` still finds:

- `## Hook (0:00–0:12)`
- `## Payoff promise`
- `## Beat N —`
- `## CTA`

After writing, run:

```bash
python3 tools/validate_packet.py videos/<id>-<slug>
python3 tools/validate_packet.py --duration videos/<id>-<slug>
python3 tools/expand_brief.py videos/<id>-<slug> --force
```

Fix hook length, missing sections, and spoken-duration WARN before considering the draft ready to record.
Do not pad `videos/sample-001-*` to satisfy `--duration`; that packet is a fixture.
