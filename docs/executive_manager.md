# Executive YouTube Manager

## Purpose

The daily task has two jobs:
1. operate the production system safely;
2. make one big-picture executive decision about the trajectory of the channel and production system.

The executive layer is not a generic motivational review. It is a portfolio decision about where the next unit of effort has the highest expected value while preserving the anti-slop and safety gates.

## Current executive decision

**Prioritize first-video completion over further architecture expansion.**

Rationale:
- The repository has substantial editorial, safety, and state-management scaffolding already.
- There are currently zero published videos.
- The most important missing evidence is real end-to-end production: a finished master that passes content + media QA.
- Further documentation or guard additions that do not unblock the first completed video have sharply lower information value than actually completing and observing one video.

Therefore, until the first complete video exists, daily executive reviews should favor work that directly advances the live packet through narration, visuals, assembly, QA, and publishing infrastructure. Defer speculative abstractions, extra wrapper CLIs, broad refactors, new formats, and premature channel strategy changes.

## Executive review sequence

Run this after the normal operational/unstick inspection:

### A. Reality check
- What is the highest-value unfinished stage?
- What concrete evidence changed since the prior review?
- Is the system producing real artifacts or only documentation?
- Are human minutes falling without reducing quality?

### B. Trajectory diagnosis
Classify the current trajectory as one of:
- **SHIP** — the bottleneck is execution; push the live packet toward completion.
- **BUILD** — a missing capability is directly blocking completion; build the smallest capability that removes it.
- **SIMPLIFY** — process overhead is growing faster than output; remove or freeze nonessential machinery.
- **PIVOT** — evidence shows the current content/process direction is repeatedly failing a documented objective; change one important assumption deliberately.
- **HOLD** — an unavoidable external dependency is genuinely blocking progress; do not manufacture work.

Choose exactly one primary state per daily review.

### C. Executive priority order before the first completed video
1. Finish the live packet.
2. Remove the smallest real bottleneck in the production path.
3. Make the pipeline repeatable for packet 2 without adding complexity that packet 1 did not need.
4. Only then optimize channel strategy using actual audience evidence.

### D. After the first completed video
Do not immediately redesign the channel from one result.
Use a small cohort of comparable videos to identify repeatable signals. Separate:
- production-system problems (time, failures, render reliability, human effort);
- content problems (clarity, specificity, retention, viewer confusion);
- packaging problems (title/thumbnail promise);
- distribution/platform variance.

Preserve what works while testing one material change at a time where practical.

## Executive evidence set

Every daily review should inspect, when available:
- completed videos and current packet status;
- time/human-intervention burden;
- QA failures and repeated failure classes;
- publishing readiness and authentication state;
- feedback/analytics observation windows;
- experiment results and null results;
- repeated viewer questions/confusion;
- backlog age and whether work is cycling without producing an artifact.

Do not optimize against one vanity metric or one early datapoint.

## Decision discipline

Each executive decision should record:
- date;
- primary trajectory state (SHIP/BUILD/SIMPLIFY/PIVOT/HOLD);
- evidence observed;
- decision;
- what is intentionally deferred;
- trigger for revisiting the decision.

Do not rewrite historical records to make a later decision look correct.

## Anti-slop constraint

Executive optimization never overrides the content-quality contract. Faster publishing is not success if the resulting videos become generic, repetitive, misleading, or low-value.

## Human-gate interaction

The 24-hour escalation policy still applies. After a manual gate expires, the executive decision should determine whether the safest fallback is to complete the task automatically, build supporting infrastructure, or hold for credentials. Do not use the executive layer to bypass authentication or invent human evidence.

## Success definition

The process is succeeding when it can repeatedly produce specific, useful, technically valid videos with falling avoidable human effort, then learn from comparable audience evidence and improve deliberately.

Do not claim “self-improving” merely because the agent edits prompts. Require observed feedback plus a recorded experiment or a documented null result.
For recurring daily checks, do not create a commit merely to record an unchanged executive decision. Only persist a decision when it changes the next action, capability priority, channel/process policy, or revisit trigger.
