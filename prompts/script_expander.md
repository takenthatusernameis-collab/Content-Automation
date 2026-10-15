# Script expander

Use this when `next_action.py` prints `expand-script` and `expand.md` already has a budget.

Do not use this on `videos/sample-001-*`. That packet is a fixture.

## Before the paste

If `idea.md` mechanism is blank or template-default, paste `idea_brief.py PATH --block` into idea.md and run `--check`. Do not expand from the generic scaffold default or the video will not match the queued title.

`expand_prompt.py` prints an Idea locks section from idea.md. Keep those fields.

## Fast path

```bash
python3 tools/expand_prompt.py videos/<id>-<slug>
```

Paste stdout into a writer model. The assembler already includes idea locks, channel, idea, writer contract, budget, and current WORDS.

The command does not write `script.md`. A printed prompt is not a draft.
Save the writer result to `PATH/draft.md`, not `script.md`.

## Band landing

The writer contract in `prompts/script_writer.md` now names a spoken-word allocation. Keep it:

- Hook 20–35, payoff 40–70, each body beat 140–220, CTA 40–80
- Total 900–1500, target ~1200
- Count WORDS lines only
- Put `<!-- spoken_words: NNN  hook: NN  beats: N  target: 900-1500 -->` at the top of draft.md

If the first return is BELOW, grow a beat with a worked scene of this packet's stall. If ABOVE, cut repeated pep. Do not add a heading. Do not invent a morning reopen unless the idea card is about the morning.

## After the writer returns a script.md body

```bash
python3 tools/words.py videos/<id>-<slug>
python3 tools/apply_script.py videos/<id>-<slug> --from videos/<id>-<slug>/draft.md
python3 tools/apply_script.py videos/<id>-<slug> --from videos/<id>-<slug>/draft.md --write --refresh
```

`apply_script.py` refuses the sample fixture and refuses expand_prompt stdout.
Default is dry-run. `--write` replaces script.md. `--refresh` updates expand.md, vo_session.md, and captions.md.
It does not bump packet status.

## Rules

- Keep existing `##` headings.
- Hook stays 20-35 words.
- Grow beats with a worked example or failure mode.
- Land in 900-1500 spoken words for `explainer-6-10min`.
- No invented statistics. No extra beats unless count is under 4.
- Do not autofill WORDS from the budget table.
- Hook and payoff must name the idea.md mechanism.
- Avoid high-precision anti-slop fillers tracked by quality_scan.py (e.g. “it's worth noting”, “at its core”, “when it comes to”, “keep in mind”, “in essence”, “the fact remains”, “let's be honest”, “here's the kicker”, and the accumulated list in docs/content_quality.md). Prefer concrete mechanism language.
- Avoid unsourced survey/authority hedges tracked by claim_scan.py (e.g. “many studies show”, “research has shown”, “it is known that”, “statistics show”, and the full list in docs/content_quality.md) unless already cited in research.md. Optionally run the scanners on draft.md before --write.
