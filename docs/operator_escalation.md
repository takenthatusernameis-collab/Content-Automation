# Operator escalation policy

## Purpose

The daily unstick agent may wait for a human decision when the repository reaches a genuine manual gate. That gate is not allowed to become an indefinite blocker.

## 24-hour rule

For every **new** manual-intervention request, record one request block in this file (or an equivalent durable state file) with:

- `requested_at_utc`: exact UTC timestamp when the request was first issued
- `reason`: the concrete missing human action
- `deadline_at_utc`: `requested_at_utc + 24 hours`
- `allowed_resolution`: the repository-side action the agent may take after the deadline

The daily unstick agent must:

1. Treat a new request as a single request, not a reason to create a commit on every daily check.
2. Remain read-only before `deadline_at_utc` unless the human has already supplied the missing input.
3. After `deadline_at_utc`, autonomously complete the allowed repository-side task using the permissions already granted to the agent.
4. Prefer the smallest safe completion path and preserve existing gates.
5. Never fabricate evidence of a human action. If the approved fallback is machine-generated (for example, generated VO), label it as generated.
6. Never bypass an authentication, authorization, payment, safety, or provider policy boundary merely because the 24-hour deadline passed.
7. If the only remaining blocker is a missing provider credential/token/secret, prepare and validate everything else, then leave the credential request as the **last manual bottleneck**.
8. Once the human supplies the missing credential, use it through the approved secret/environment mechanism; never write secrets into repository files, commits, logs, or generated state.

## No-churn rule

The daily check must not rewrite `STATE.md`, `NEXT.md`, prompts, logs, or documentation merely to say that the same request is still waiting. A request may produce a repository commit only when:

- the human supplied the requested input;
- the 24-hour escalation became eligible and the agent performed an allowed completion;
- the blocker materially changed; or
- a genuine regression requires a code/configuration fix.

## Current Q1 request

- `requested_at_utc`: 2026-09-18T00:00:00Z
- `reason`: selected VO file missing at the packet-relative DROP path
- `deadline_at_utc`: 2026-09-19T00:00:00Z
- `allowed_resolution`: generated VO labeled generated; narration adapter + `vo_origin.md` sidecar; do not commit audio; do not bump `ready_for_edit` without an on-disk take
- `resolved_at_utc`: 2026-09-19T00:10:00Z (Run 213)
- `resolution`: `tools/narration_adapter.py` added; Q1 `vo_origin.md` set to `kind: generated`. Workspace TTS artifact was not committed.

Do not retroactively treat earlier hold cycles as new requests.

## Permission boundary

The daily unstick agent is authorized to use repository write access and ordinary local build/test tooling to complete an eligible task. This does **not** grant permission to expose secrets, bypass third-party authorization, or claim a provider-side capability that has not been authenticated.
