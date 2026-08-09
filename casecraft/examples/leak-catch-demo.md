# Worked Example — The Demo Moment: catching a leak on stage (FICTIONAL)

This is the stage demonstration of the linter catching what a generic chatbot would
silently ship. Two mini-cases, both drawn from a `/casecraft marco` run.

---

## Setup (shown to judges)

```
/casecraft marco "Week 2 at Sunbeam Bakery. Same role, same machines.
Addresses new: rotation with the cashier during off-peak…"
```

CaseCraft generates Teacher Guide, Parent Guide, Social Story → linter runs:
per-document methodology → cross-doc Level 1 (facts) + Level 2 (verbatim scripts) →
freshness → **sensitivity leak check → FAIL.**

---

## Leak 1 — a `[team]` fact inside the Parent Guide (B2/B5)

**Parent Guide draft contains:**

> "Great progress this term — Marco's IEP review at HKPC on the 26th will
> review his goals' progress notes…"

The phrase "IEP review" + "goals' progress notes" traces to the passport's
**Goals [team]** section. The Parent Guide's allowed set is `[open]` only.

**Linter output:**

| Check | Status | Detail |
|---|---|---|
| B2 — no `[team]` in Parent Guide | **FAIL** | "goals' progress notes (IEP review)" traces to `Goals [team]` |
| B5 — no `[clinical]` in Parent Guide | PASS | no clinical section visited |
| B7 — no diagnosis language | PASS | — |

→ The worker gets: *"FAIL — Parent Guide references the team's goals file. The
passport's Goals [team] section must not reach parents. Rewriting the Parent Guide
without the goals reference, then re-running the pack."* The parent guide is regenerated
and passes.

---

## Leak 2 — cross-document fact disagreement (Level 1, 5-min vs 10-min warning)

Teacher Guide says **"give Marco the 5-minute transition script before room move"**;
Parent Guide says **"the transition warning is given 10 minutes before leaving the
kitchen."** — the same script, different lead times.

**Level 1 check (shared facts):**

| Claim | Teacher Guide | Parent Guide | Status |
|---|---|---|---|
| Warning lead time | 5 minutes | 10 minutes | **FLAG — contradiction** |

Both docs were drafted from the brief ("…new step: end-of-shift, the assistant calls 5
minutes ahead…"). The teacher copy was correct; the parent copy drifted. The worker
confirms **5 minutes**, the pack regenerates, and both docs then render the same
**word-for-word script** (Level 2 verification):

> "Before we tidy up: 5 more minutes, then we tidy the trays together."

---

## What the demo proves

- **The system notices what no one else would** (a generic chatbot would silently ship
  both errors; the linter's audience rules make them impossible to ship).
- **The fix is professional-driven, not AI-hidden** (worker: "parent guide, drop the
  goals note" → regenerated; no auto-magic).
- **Sensitivity is a hard gate** — a single FAIL blocks delivery of the whole pack.