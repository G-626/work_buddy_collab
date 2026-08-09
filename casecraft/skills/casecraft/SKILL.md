# Skill: casecraft

Generate a **Coordinated Support Pack** for one student, for one situation, as a set of
**review-ready drafts** for the professional. Never deliver output to the student directly.

## Inputs

| Input | Required | Source |
|---|---|---|
| Student ID | yes | Folder name under `students/` (e.g. `marco`) |
| Situation brief | yes | Free text from the professional: what, when, where, who, what the student will do, anything known to be hard |

A good brief covers: **what** is happening, **when**, **where**, **who** is involved,
**what** the student will do, and **what's known to be hard**. If the brief is missing
elements, flag them in the linter report — do not silently guess.

## Pipeline

1. **Load the passport.** Read `students/<id>/passport.md`. Note the sensitivity tags on
   each section (`[open]`, `[team]`, `[clinical]`). These determine which documents to
   generate and which sections each document may draw from.
2. **Assess the situation.** Decide whether the situation warrants a Social Story
   (a new transition, unfamiliar event, or change to routine). If yes, include it.
   If no, note the decision in the linter report.
3. **Generate documents** — one per audience, plus optional Social Story. Use only the
   passport sections permitted for that audience:
   - Teacher Guide: `[open]` sections only
   - Parent Guide: `[open]` sections only
   - Social Story: `[open]` sections only
   - Therapist Summary (roadmap): `[open]` + `[team]` sections
   - `templates/teacher-guide.md` → `teacher-guide.md`
   - `templates/parent-guide.md` → `parent-guide.md`
   - `templates/social-story.md` → `social-story.md` (if warranted)
4. **Lint each document** against its template's linter:
   - `templates/linter-teacher-guide.md`
   - `templates/linter-parent-guide.md`
   - `templates/linter-social-story.md`
   - `templates/linter-sensitivity-leak.md` (runs across all documents)
5. **Cross-document consistency check** (Level 1 + Level 2):
   - **Level 1 — Shared facts**: Extract factual claims (times, names, strategies, coping
     options, dates, places) from all generated documents. Flag contradictions between any
     two documents. Example: Teacher Guide says "5-minute warning" but Parent Guide says
     "10-minute warning" → FLAG.
   - **Level 2 — Shared language**: Verify that key phrases (coping scripts, transition
     cues, help-seeking scripts) appear **word-for-word identical** in every document that
     uses them. If a coping script appears in the Teacher Guide and the Social Story, it
     must be the same sentence. Fix or flag any variation.
6. **Freshness check.** Read the passport's `## Freshness stamps` table (deterministic
   per-section dates). Flag any section untouched for >30 days:
   A stale passport is a liability; perceiving staleness keeps the passport trustworthy.
7. **Save outputs** to `students/<id>/packs/<YYYY-MM-DD>-<slug>/`:
   - `teacher-guide.md`
   - `parent-guide.md`
   - `social-story.md` (if generated)
   - `linter-report.md` (full audit trail)
8. **Report back to the professional:**
   - Summary line: `N documents generated, X checks passed, Y auto-fixed, Z flagged for your review`
   - Full document texts
   - File paths
   - End with: *"Drafts for your review — please edit before use."*

## Batch mode

`/casecraft batch "<situation brief>" --students <id1,id2,...>` — run the pipeline once per
student from **one brief**. Each pack must differ according to each dossier (audience tags,
reading level, voice preference, triggers, coping strategies). Produce a summary table:
student, documents generated, flags needing review.

## Hard boundaries

- **No invented facts.** Anything not in the brief or dossier must be hedged or flagged.
- **No clinical claims.** No document labels the student, mentions diagnosis, or frames
  the student as the problem.
- **No direct delivery.** Output is always addressed to the professional.
- **Cross-document consistency is not optional.** If two documents contradict each other
  on a fact, that is a FLAG — never silently pick one version.
