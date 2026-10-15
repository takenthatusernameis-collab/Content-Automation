# Content quality: anti-slop contract

## Purpose

“Not AI slop” is an editorial requirement, not a claim that a detector can prove authorship.
The system should produce useful, specific, original-feeling work that could survive a skeptical human editor. Automated checks may catch obvious weak patterns, but they must not pretend to measure human authorship.

## Required qualities

- A concrete mechanism: the viewer can identify exactly what to do, write, change, or test.
- Specific scenes or examples: prefer observable situations, decisions, files, objects, constraints, or procedures over abstract encouragement.
- Original reasoning: follow the packet's actual problem and mechanism, not a generic “problem → 5 tips → motivational CTA” template.
- Useful compression: every paragraph should add a decision, example, distinction, test, failure mode, or instruction.
- Natural language: mix sentence length and cadence; prefer plain speech over polished corporate phrasing.
- Honest epistemics: no invented statistics, fake citations, fabricated personal stories, fake case studies, or implied experiments that did not happen.
- Calibrated claims: do not promise transformation, certainty, or universal results.
- A real ending: the CTA should be a concrete action that follows from the mechanism, not generic engagement bait.

## Anti-patterns to reject or rewrite

- Empty abstractions such as “unlock your potential” or “work smarter”.
- Generic setup filler such as “in today's fast-paced world” or “we all struggle with…”.
- Repeated meta language such as “in this video”, “you will learn”, or “the key is” when it adds no information.
- Motivational padding used to reach the word target.
- Excessive triads, symmetrical slogans, or repeated “not X, but Y” constructions.
- Claims of personal experience, testing, user results, or expertise that are not documented.
- Generic failure-mode lists whose examples could fit almost any productivity video.
- Repeated conclusions stated in slightly different words.
- CTA padding, subscribe language, or engagement bait when the packet does not call for it.
- A pinned comment that asks the viewer to reply. The pin is the assignment from the mechanism, not a reply prompt. `viewer_comment` drops "Reply with the cue you wrote down." before a comment post. Do not rewrite the approved Q1 pin to remove it.
- Common filler openers/closers such as “let's dive in”, “without further ado”, or “it goes without saying”.
- Assumed-common-knowledge hedges such as “as we all know”, “it's no secret that”, “needless to say”, or “the fact of the matter is”.
- Explanatory filler such as “to put it simply”, “in other words”, “the reality is”, “here's the thing”, “the truth is”, or “make no mistake”.
- Summary and transition padding such as “in a nutshell”, “long story short”, “when all is said and done”, “the point is”, “let me be clear”, or “as it turns out”.
- Additional filler hedges such as “believe it or not”, “to be honest”, “the thing is”, “all in all”, “moving forward”, or “going forward”.
- Priority/transition padding such as “first and foremost”, “it is important to note”, “it should be noted”, “as a matter of fact”, “for what it's worth”, “that being said”, or “having said that”.
- Assumed-certainty and summary fillers such as “in fact”, “of course”, “obviously”, “clearly”, “simply put”, “in short”, “to be clear”, or “all things considered”.
- Further common filler and meta phrases such as “it's worth noting”, “at its core”, “when it comes to”, “keep in mind”, “in essence”, “the fact remains”, “let's be honest”, or “here's the kicker”.

These are revision signals, not permission for a crude regex-based “AI detector.”

## Originality test

Before a script is promoted to ready_for_vo, ask:
1. Could the mechanism be explained in one sentence?
2. Does each beat contain at least one concrete action, example, distinction, or test?
3. Is there at least one detail that clearly belongs to this packet rather than any topic in the niche?
4. Are the examples internally consistent with the packet's viewer/problem?
5. Can any paragraph be deleted without losing information? If yes, cut it.
6. Does the final CTA naturally follow from the mechanism?
7. Does the script avoid pretending that generated prose is lived human experience?

A “no” is a revision signal before recording.

## Automation policy

The daily agent may rewrite generic or repetitive copy, replace abstract filler with concrete procedures from the packet's mechanism, remove repeated conclusions and meta narration, tighten claims when evidence is absent, and leave strong copy unchanged.

The daily agent must not invent anecdotes, testimonials, experiments, statistics, citations, or outcomes; add personal experience to make text sound human; deliberately introduce mistakes or awkwardness to simulate a human author; use a hidden AI score as the sole publish criterion; or change the locked topic/problem/mechanism merely to avoid a style pattern.

## Final editorial gate

Before ready_for_vo or publishing, combine mechanical packet validation, evidence/claim checks, the originality test above, and a read-aloud pass for cadence and repetition.
Generated narration is acceptable when explicitly authorized by the operator, but it must not be represented as a human recording.

The quality gate is about the content, not disguising the use of AI.

## Scanner

`python3 tools/quality_scan.py` reports the high-precision phrases in this file inside script.md WORDS. Matching uses word-boundary regex (\b) for higher precision. It does not rewrite the script and does not claim authorship. `--strict` exits 1 only when a hit remains. `tools/set_status.py` refuses `ready_for_vo` while a hit remains. A missing script is not a hit. Q1 was clear on Run 322 and was not rewritten. Do not rewrite Q1 WORDS to chase a later phrase list. Run 552 added “let's dive in”, “without further ado”, “it goes without saying” (plus curly apostrophe variants). Run 554 added “as we all know”, “it's no secret that” (plus curly), “needless to say”, “the fact of the matter is”. Run 555 added “to put it simply”, “in other words”, “the reality is”, “here's the thing” (plus curly), “the truth is”, “make no mistake”. Run 556 added “in a nutshell”, “long story short”, “when all is said and done”, “the point is”, “let me be clear”, “as it turns out”. Run 557 added “believe it or not”, “to be honest”, “the thing is”, “all in all”, “moving forward”, “going forward”. Run 558 switched to word-boundary matching and added “first and foremost”, “it is important to note”, “it should be noted”, “as a matter of fact”, “for what it's worth” (plus curly), “that being said”, “having said that”. Run 560 added “in fact”, “of course”, “obviously”, “clearly”, “simply put”, “in short”, “to be clear”, “all things considered”. Run 562 added “it's worth noting” (plus curly), “at its core”, “when it comes to”, “keep in mind”, “in essence”, “the fact remains”, “let's be honest” (plus curly), “here's the kicker” (plus curly).

`python3 tools/claim_scan.py` reports digit tokens and survey hedges in script WORDS that have no non-placeholder Sources bullet citing that same token or phrase. Matching uses word-boundary regex (\b) for higher precision. It does not rewrite script.md or research.md. `--strict` exits 1 only when a hit remains. `tools/set_status.py` refuses `ready_for_vo` while a hit remains. A missing script is not a hit. Q1 had no spoken digits or hedges on Run 326 and was not rewritten. Run 553 added “experts say”, “data shows”, “research indicates”, “studies indicate” to the hedge list. Run 559 switched to word-boundary matching and added “according to experts”, “research suggests”, “evidence shows”, “it has been shown”, “scientists say”, “a study found”, “surveys indicate”. Run 563 added “many studies show”, “research has shown”, “it is known that”, “widely known that”, “statistics show”, “data indicates”, “as research shows”, “studies have shown”.
