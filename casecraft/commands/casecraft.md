# Command: /casecraft

## Usage

```
/casecraft <student-id> "<situation brief>"
/casecraft batch "<situation brief>" --students <id1,id2,...>
```

## What it does

Invokes the `casecraft` skill (skills/casecraft/SKILL.md): loads the student's
passport, reads the sensitivity tags, generates a Coordinated Support Pack
(Teacher Guide + Parent Report + optional Social Story + Therapist Summary), lints
each document, runs cross-document consistency checks, exports PDFs, saves all
outputs to a dated pack folder, and returns a summary + full texts for
professional review.

## Examples

```
/casecraft marco "First work-experience placement at Sunbeam Bakery next Tuesday 19 Aug,
9:00–15:30. Travel by MTR Jordan to Mong Kok, Exit B2. Supervisor is Mrs. Chan. Jobs:
bagging rolls, labelling boxes. Kitchen is warm and the mixers are loud."
```

```
/casecraft priya "New art class starts Thursday 21 Aug, room change from 3B to 1A,
different teacher (Ms. Liu), group project in week 3."
```

```
/casecraft batch "First day of new term, room changes, new timetable" --students marco,priya
```

## Response shape

1. Summary line: `N documents generated, X checks passed, Y auto-fixed, Z flagged for your review`
2. Full document texts (Teacher Guide, Parent Report, optional Social Story, Therapist Summary)
3. Linter report (full audit trail, saved to pack folder)
4. PDF + saved file paths
5. Closing line: *"Drafts for your review — please edit before use."*
