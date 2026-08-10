# Therapist Summary Linter Checklist

Score the drafted Therapist Summary against every check. Status per check:
PASS / FIXED / FLAG.
- **FIXED** = mechanical auto-fix applied; show before → after.
- **FLAG** = needs professional judgement or missing information; do NOT auto-fix.

## A. Boundary (blocking)

| # | Check | Auto-fix |
|---|---|---|
| A1 | No `[clinical]` content: diagnosis, medication, clinical records, test results | FLAG — blocking. The `[clinical]` section is never rendered; if the source contains it, this is a boundary violation |
| A2 | No diagnosis asserted ("has ASD", "autistic") | FIXED: rephrase as support language |
| A3 | No affect labels ("seemed anxious", "was frustrated") | FIXED: rewrite as observables |
| A4 | No causation claims ("because the noise", "to avoid…") — co-occurrence only | FIXED: rewrite as correlation, route as question |

## B. Content

| # | Check | Auto-fix |
|---|---|---|
| B1 | Every goal-progress row has evidence (count/quote/timestamp) | FLAG if evidence column empty |
| B2 | Patterns are descriptive/correlational, never a verdict | FIXED: rewrite |
| B3 | Open questions section present with ≥ 2 real questions | FLAG if missing/empty |
| B4 | Recommended next step present | FLAG if missing |
| B5 | `[open]` + `[team]` coverage: relevant passport sections actually used | FLAG if a clearly relevant section was ignored |

## C. Consistency (cross-document)

| # | Check | Auto-fix |
|---|---|---|
| C1 | Goal-progress statuses do not contradict the Parent Report version (may be more detailed, never opposite) | FLAG on contradiction |
| C2 | Shared facts (times, names, strategies) match all other documents in the pack | FLAG on contradiction |
| C3 | Coping scripts / language examples identical to Teacher Guide + Parent Report | FIXED: align to the dossier's version |

## D. Report format

Output the report as a table: `Check | Status | Detail (before → after, or flag
reason)`, followed by:
- **Assumptions made**
- **Questions for the reviewer**
- One-line verdict: `Ready for review` / `Needs reviewer input on N item(s)`
