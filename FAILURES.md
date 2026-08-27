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

## 2026-08-27 — empty title list items forged three titles

- **Tried:** `^\\d+\\.\\s+(.+)$` on template `1.` / `2.` / `3.` lines
- **Evidence:** `titles_from` returned `['2.', '4.', 'Notes (promise vs clickbait risk):']` because `\\s` matched the newline and `$` ended on the next line. Draft validate then `FAIL`ed with `only 3 titles, need >=5` instead of `DRAFT-INCOMPLETE`.
- **Lesson:** Same class as empty field parsers. After `N.`, allow only `[ \\t]+`.
- **Avoid:** `\\s` in one-line list parsers.
