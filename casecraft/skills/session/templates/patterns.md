# Patterns section — template (observables, correlational, never verdicts)

Read by the `session` skill (Step 6) and `casecraft` (freshness/lens checks). The
Passport **Patterns [team]** section accumulates rows across approved sessions.

## Rendering rules

1. **One row per (variable × context)** per session. Example columns:
   `session | variable | count | context | observed trend | worker note`
2. **Context must be an observable** (`mixer running`, `group discussion`, `transition`).
   Co-occurrence is reported as **alignment**, never causation: write
   *"ear-cover events aligned with mixer start (2 of 2 sessions)"* — never
   *"the mixer causes distress."*
3. **Trends over ≥ 3 sessions only.** One session is a baseline, not a pattern.
   Until 3 sessions exist, rows show `baseline (session N of 3)` and route to the
   worker as a question.
4. **Surprises route to the worker as questions** — never as findings.
5. **Positive-first:** reinforcement facts (self-regulation use, unprompted help-seeking)
   are first-class rows; the section opens with a one-line summary of what the team can
   reinforce.
6. **No affect labels, no disposition, no diagnosis** — the anti-schema of
   `docs/schemas/movement-events.md` applies verbatim to this section.

## Template

```markdown
## Patterns [team]

*What the team can reinforce (this period): <1–2 positive-first sentences>*

| Session | Variable | Count | Aligned context | Trend | Worker note |
|---|---|---|---|---|---|
| 2025-08-19 | cover_ears | 1 | mixer running | baseline (1/3) | — |
| … | … | … | … | … | … |

*Correlations observed (descriptive):* <one or two correlational sentences, neutral>
*Questions for the worker:* <anything surprising, routed as questions>
```

## Lint rules applied by the linter (Level 0 — traceable)

- Every count must trace to a capture file under `sessions/<id>/sessions`.
- Any row that names a state/intention/feeling → **FAIL** (anti-schema).
- Less than 3 sessions reduces the whole section to "baseline" wording.