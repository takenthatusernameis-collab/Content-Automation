# Script writer

Use this prompt when filling `script.md` for a packet. Bind every draft to `docs/production_rules.md` and `docs/channel.md`.

## Input

Read, in order:

1. `docs/channel.md`
2. `docs/production_rules.md`
3. The packet `idea.md`
4. The packet `research.md` if it has sources
5. The empty beat skeleton in `script.md`

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
```

Fix hook length and missing sections before considering the draft done.
