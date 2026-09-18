# Feedback and improvement loop

## Purpose

After publication, the pipeline should learn from observed audience response without turning noisy metrics or isolated comments into automatic overfitting.

## Sources

YouTube Analytics can provide metrics such as views, likes/dislikes, estimated minutes watched, average view duration, and average view percentage. citeturn562536search5turn562536search7
YouTube comment threads can be retrieved by video ID; full replies may require comments.list. citeturn562536search0turn562536search2

## Feedback record

Each published packet should accumulate a feedback record containing:
- video ID and packet ID
- publication timestamp
- observation-window start/end
- analytics retrieval timestamp
- selected metrics and their definitions
- comment samples plus classification (question, objection, praise, confusion, request, spam/noise)
- source URLs/API endpoints where applicable
- experiment IDs affected by the evidence

Do not compare raw counts across videos of different ages without normalization or a documented reason. Prefer comparable observation windows.

## Signal hierarchy

1. Repeated, specific viewer questions or confusion
2. Consistent audience-retention/watch-time patterns across comparable videos
3. Repeated positive/negative comments that map to a concrete content choice
4. One-off comments
5. Raw vanity counts without context

No individual comment or early metric should automatically rewrite the channel strategy.

## Experiment loop

1. Observe: collect data for a defined window.
2. Diagnose: identify one plausible content mechanism behind a weak or strong result.
3. Hypothesize: write one testable statement.
4. Change: modify one material variable where practical (hook, mechanism framing, example density, title promise, visual explanation, pacing, CTA, or topic selection).
5. Ship: publish the changed version as a new packet.
6. Compare: use a predeclared metric and guardrails against an appropriate baseline.
7. Learn: record result, uncertainty, and whether to keep, discard, or retest the change.

Never silently rewrite an old video's script to make the experiment appear successful.

## Anti-slop feedback rule

Feedback may identify confusion, repetition, vagueness, or missing examples. The response should make the content more specific and useful, not merely more sensational, more repetitive, or more optimized for engagement bait.

Do not train the writer to copy commenter phrasing blindly. Extract the underlying need.

## Required durable records

- feedback.md: observed evidence for a video
- experiments.md: hypothesis and result ledger
- failures.md: failed approaches and why
- topic_queue.md: future topics informed by repeated audience needs

Each record must distinguish observation from interpretation and interpretation from the next test.