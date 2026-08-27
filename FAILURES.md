# FAILURES

When recording a failure:
- What was tried
- Evidence it failed
- Lesson
- What to avoid

## 2026-08-27 — empty packet fields swallowed the next line

- **Tried:** matching `- id:` and `Primary:` with `\\s*` plus `(.*)$` / `(.+)$`
- **Evidence:** On `- id:` followed by `- slug: x`, group 1 became `- slug: x` because `\\s*` ate the newline. Empty `Primary:` captured `Alts:`.
- **Lesson:** After a colon, allow only spaces/tabs, then the rest of that line. Anchor `^`. Never let `\\s*` consume the newline after an empty value.
- **Avoid:** Using `\\s*` immediately after `:` when a blank value is valid.
