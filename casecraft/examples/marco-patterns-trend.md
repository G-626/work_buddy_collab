# Worked Example — Patterns from Marco's bakery session (FICTIONAL)

The Movement Event Stream in `students/marco/sessions/2026-08-08-bakery/capture.md`
ingests into the passport's **Patterns** section after the review gate.

## Step 6 output (first session → baseline)

**Passport v1.0 → v1.1 · Patterns section after merge**

> *Last reinforced: Marco self-initiated his ear defenders before the second mixer run (10:15) — he can now call up his regulation tool himself.*

| Session | Pattern | Count | Aligned context | Outcome | Worker note |
|---|---|---|---|---|---|
| 2025-08-19 | cover_ears | 1 | mixer start | baseline (1/3) | — |
| 2025-08-19 | help_request_prompted | 2 | after task completion | baseline (1/3) | — |
| 2025-08-19 | help_request_unprompted | 1 | after tray finished | baseline (1/3) | possibly new skill — track next sessions |
| 2025-08-19 | self_regulation_use | 2 | mixer running | baseline (1/3) | 10:15 was unprompted — reinforce |
| 2025-08-19 | stand_still ≥ 10 s | 2 (45 s, 30 s) | before help request | baseline (1/3) | worker: within normal range; reassess at 3 sessions |

*Surfaces aligned:* cover_ears and stand_still pauses both co-occurred with task-complete
moments and mixer runs in this session.
*Questions for the worker:* none opened this session — worker approved the note on the
45 s pause at the gate ("within normal range, reassess after 3 sessions").

## Step 2 — What feeds into the passport text

The linter's traceable rule validates every row to `capture.md`. No extrapolated rows.

The "reinforce" line is positive-first: it tells the team **what to redo** (praise and
repeat the defer-proofing moment), not what's wrong.

## Step 3 — After 3 sessions

When sessions 2–3 land (e.g. bakery again, hotel), rows flip from *baseline* to a trend
line (e.g., "ear-cover count 2 → 1 → 0 across 3 sessions; 0 coincident with defensive-
first"), and only then does the section render a *forward surface* for the worker's
week review.