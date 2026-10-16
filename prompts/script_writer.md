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

## Draft starter (recommended first step)

Before writing any WORDS, optionally run `python3 tools/draft_starter.py PATH`. It prints a complete mechanism-aligned skeleton (Hook candidates, Payoff, Body starters, Failure mode, CTA, and matching VISUAL directions) grounded in idea.md. Copy preferred lines into draft.md and expand the body beats to the word targets. This reduces sequential calls to the individual *suggest.py tools and keeps the starting point operational and packet-specific. Individual tools remain available if you need more options for one section.

## Band landing (count before you return)

Spoken WORDS for `explainer-6-10min` must land in **900–1500**. Target **~1200**. Count only WORDS lines, not VISUAL, not headings.

Use this allocation unless expand.md already names different beat sizes:

| Segment | Spoken words | Rule |
|---------|--------------|------|
| Hook | 20–35 | Name the mechanism. One sentence plus a sting is enough. |
| Payoff promise | 40–70 | One doable outcome. Name the mechanism again. |
| Each body beat | 140–220 | Worked example or failure mode inside the existing heading. |
| CTA | 40–80 | One action finishable in under two minutes. |

If you have 5 body beats: 30 + 55 + 5×180 + 60 ≈ 1045. If you have 6: stay near 160–180 per beat. If a first pass is under 900, grow the thinnest beat with a concrete scene of this packet's stall (the idea.md problem and mechanism), not a slogan and not a morning reopen unless the idea card is about the morning. If over 1500, cut repeated pep, not the mechanism name.

Before returning the draft, write one HTML comment at the very top:

```
<!-- spoken_words: NNN  hook: NN  beats: N  target: 900-1500 -->
```

That comment is not spoken WORDS. `words.py` still owns the official count after save.

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

## Hook guidance

Before writing the ## Hook section, optionally run `python3 tools/hook_suggest.py PATH` and use or adapt one of its candidates. The hook must name the mechanism and the concrete stall from idea.md, stay calm/operational, and land in 20–35 spoken words. Prefer the tool's suggestion over generic openers.

## Payoff guidance

Before writing the ## Payoff promise section, optionally run `python3 tools/payoff_suggest.py PATH` and use or adapt one of its candidates. The payoff must name the concrete doable outcome and the mechanism, stay calm/operational, and land in 40–70 spoken words. Prefer the tool's suggestion over abstract encouragement.

## Body guidance

Before writing the ## Beat sections, optionally run `python3 tools/body_suggest.py PATH` and use or adapt its starters inside the existing beat headings. Each beat must show the viewer using the mechanism on this packet's stall, include a concrete action/example/distinction/test, and stay operational. Prefer the tool's suggestion over abstract filler. Expand to the beat word target without adding slogans.

## Failure mode guidance

Before writing a failure-mode beat, optionally run `python3 tools/failure_mode_suggest.py PATH` and use or adapt one of its candidates inside an existing ## Beat heading. The failure mode must show the concrete stall that occurs when this packet's mechanism is absent, stay operational, and avoid generic lists that could fit any topic. Prefer the tool's suggestion over abstract "what goes wrong" filler.

## Visual guidance

Before writing any VISUAL: lines, optionally run `python3 tools/visual_suggest.py PATH` and use or adapt its short stage-direction candidates. Each VISUAL must show the stall or the installed default in the workspace the viewer already has (note, sticky, open file, desk edge), stay under 35 words, and remain a stage direction rather than a second script. Prefer the tool's suggestion over generic stock language.

## CTA guidance

Before writing the ## CTA section, optionally run `python3 tools/cta_suggest.py PATH` and use or adapt its spoken suggestion. The CTA must install the mechanism as a concrete under-two-minute action the viewer can finish immediately (channel promise: one small default the same day). Prefer the tool's suggestion over generic engagement language. After drafting, the end-screen / final CTA text should also pass `tools/end_screen_scan.py` (no "smash the like", "subscribe for more", reply prompts, etc.).

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

## Anti-slop quality gate

Before returning a draft, read docs/content_quality.md. Do not optimize for sounding “human” by inserting fake anecdotes, mistakes, slang, or unverifiable experience. Make the script feel specific by grounding it in the packet's actual mechanism, viewer, concrete scenes, decisions, tests, and failure modes.

Prefer original reasoning over generic listicles. Every body beat should add a concrete action, example, distinction, or test. Cut paragraphs whose only function is motivation, repetition, or word-count padding. Avoid repeated meta framing such as “in this video,” repeated “the key is” constructions, generic productivity slogans, and symmetrical slogan-heavy prose. Do not add claims requiring evidence when research.md does not support them.

Explicitly avoid the high-precision anti-slop phrases tracked by `tools/quality_scan.py` (see the current list in docs/content_quality.md). These include assumed-certainty and summary fillers such as “in fact”, “of course”, “obviously”, “clearly”, “simply put”, “in short”, “to be clear”, “all things considered”, plus further common fillers such as “it's worth noting”, “at its core”, “when it comes to”, “keep in mind”, “in essence”, “the fact remains”, “let's be honest”, “here's the kicker”, perspective/society fillers such as “bear in mind”, “in the modern world”, “in today's society”, additional transitions such as “it's safe to say”, “suffice it to say”, “one thing is clear”, “in a perfect world”, “when push comes to shove”, “to be fair”, “last but not least”, “with that said”, “to that end”, “as previously mentioned”, “it is worth mentioning”, further common fillers such as “in reality”, “as a result”, “for instance”, “in particular”, “on the other hand”, “that said”, “the bottom line”, “it is important”, additional summary and implication fillers such as “to sum up”, “in summary”, “put simply”, “what this means is”, “the implication is”, “case in point”, “in the final analysis”, “when you think about it”, and the longer accumulated list of openers, hedges, and transitions. Prefer concrete mechanism language instead.

Also avoid unsourced survey/authority hedges tracked by `tools/claim_scan.py` (“many studies show”, “research has shown”, “it is known that”, “widely known that”, “statistics show”, “data indicates”, “as research shows”, “studies have shown”, “researchers found”, “according to a survey”, “data reveals”, “experts agree”, “studies suggest”, plus “according to experts”, “research suggests”, “evidence shows”, “it has been shown”, “scientists say”, “a study found”, “surveys indicate”, and earlier hedges) unless the exact phrase or supporting number already appears in a non-placeholder Sources bullet in research.md.

After saving the draft.md, optionally run `python3 tools/quality_scan.py PATH` and `python3 tools/claim_scan.py PATH` (or inspect the spoken WORDS against the lists) and revise any hits before apply_script.py --write. Both scanners now include short context snippets for each hit. A hit is a revision signal, not an authorship claim.

Before promotion, perform the seven-item originality test in docs/content_quality.md. If a quality answer is “no,” revise the draft before apply_script.py --write.
