# Worked Example — Batch mode (FICTIONAL)

Two students, one goal brief, independent sessions. Demonstrates T7 (iteration) at the
product level: one run → per-student passport deltas → per-student views.

## Command

```
/session batch "end-of-term work experience: ask for help when unsure" --students marco,priya
```

(WorkBuddy runs the pipeline once per student; each has its own capture package, its
own review gate, its own passport delta.)

## Summary table (returned to the worker)

| Student | Session goal | Goal met? | Passport | Flags |
|---|---|---|---|---|
| marco | ask for help, ≤ 2 prompts | MET (3 asks) | v1.1 | none — 45 s pause reassess@3 |
| priya | contribute one idea, ≤ 2 prompts | MET (1 prompted + 1 unprompted) | v1.1 | 11:15 look-down → question |

## Per-student review gates (independent)

- **Marco** approves with one edit ("45-second pause within normal range; reassess at 3
  sessions") → passport delta merges, views regenerate.
- **Priya** approves as-is; add a note: "look-down consistency to compare across
  sessions; keep in Questions for now."

## Result: both passports v1.0 → v1.1

- Marco: Goal 1 progress noted; What works (ear-defender self-initiation); Session log;
  Patterns (bakery baseline) — all stamped 2025-08-19.
- Priya: Goal 1 progress noted; What works (role assignment works as passport predicted);
  Session log; Patterns (baseline 1/3) — stamped 2025-08-21.

Views regenerated: 3 per student (Teacher Guide, Parent Guide, Social Story) — 6
documents, each linter-checked (incl. both leak checks: PASS).

## Batch ≠ template copying

Both students differ because each pack derives from its own passport + capture:
Marco's Teacher Guide notes written step lists + ear-defender reminder; Priya's Teacher
Guide notes assigned-role-only group work + written feedback preference — different
voices, different scripts, zero manual re-typing.