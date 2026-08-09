# Sensitivity Leak Linter Checklist

Score every generated view against every check. Status per check: PASS / FAIL.
- **FAIL** = blocking. The view must not be delivered until the leak is resolved.
  There is no auto-fix — the professional must decide whether the content belongs.

## A. Sensitivity tags

The Student Passport uses three sensitivity levels:

| Tag | Meaning | Visible to |
|---|---|---|
| `[open]` | General information about what supports the student | Teacher, parent, therapist, student |
| `[team]` | Working documents for the professional team (goals, session log) | Therapist, social worker only |
| `[clinical]` | Diagnosis, medication, clinical reports | Clinical team only — never in parent/teacher/student views |

## B. Leak checks

| # | Check | Status |
|---|---|---|
| B1 | No `[team]` content in Teacher Guide | PASS / FAIL |
| B2 | No `[team]` content in Parent Guide | PASS / FAIL |
| B3 | No `[team]` content in Social Story | PASS / FAIL |
| B4 | No `[clinical]` content in Teacher Guide | PASS / FAIL |
| B5 | No `[clinical]` content in Parent Guide | PASS / FAIL |
| B6 | No `[clinical]` content in Social Story | PASS / FAIL |
| B7 | No diagnosis language in any view (autism, ASD, or any clinical label) | PASS / FAIL |

## C. How to check

For each generated view:
1. Extract every factual claim, strategy, and reference.
2. Trace each back to the passport section it came from.
3. Check the section's sensitivity tag against the view's audience.
4. If any claim traces to a `[team]` or `[clinical]` section and the view's audience
   should not see it → **FAIL**.

## D. Report format

Output the report as a table: `Check | Status | Detail (what leaked, from which section,
into which view)`.

A single FAIL blocks the entire pack. The professional must resolve the leak before
any view is delivered.
