# Skill: socialstory

Draft a personalised, methodology-compliant Social Story for one student, for one situation,
as a **review-ready draft** for the professional. Never deliver output to the student directly.

**Moat (why not just a chatbot):** professionals *can* paste notes into Gemini and get a story —
but they get no audit against the Social Stories 10.2 criteria, no longitudinal consistency with
the student's past stories, and no local record. This skill is an **evidence engine**: every draft
is linted against the methodology with a visible report, grounded in the curated dossier, and
filed into a searchable story library that keeps voice, scripts, and facts consistent over time.

## Inputs

| Input | Required | Source |
|---|---|---|
| Student ID | yes | Folder name under `students/` (e.g. `marco`) |
| Situation brief | yes | Free text from the professional: what, when, where, who, what the student will do, anything known to be hard |
| `voice` | optional | `first` (default) or `third` (social-article register for older teens) |
| `format` | optional | `pdf-onepager` (default), `pdf-multipage`, or `markdown-only` |
| `language` | optional | `en` (default) or `zh` |

## Pipeline

1. **Load the dossier.** Read `students/<id>/profile.md`. If the dossier is missing a field
   needed for the story (e.g. reading level), note the assumption in the linter report —
   never silently guess.
2. **Draft the story** following `templates/story-template.md` exactly — sentence types,
   ratio, language rules, adolescent register, personalisation rules.
3. **Lint the draft** using `templates/linter-checklist.md`. Auto-fix violations where the
   fix is mechanical (vague words, negative framing, ratio rebalancing by adding description).
   If a violation requires information not in the brief or dossier, flag it for the reviewer
   instead of inventing content.
4. **Write the companion one-pager** for staff/parents from `templates/companion-template.md`,
   using the same situation facts.
5. **Check continuity.** Read `students/<id>/stories/index.md` and any prior stories on
   related situations. Reuse established scripts (e.g. the student's help-seeking script)
   word-for-word where relevant; flag contradictions with previous stories instead of
   silently introducing new wording.
6. **Save outputs:**
   - `students/<id>/stories/<YYYY-MM-DD>-<slug>.md` (editable source)
   - `students/<id>/stories/<YYYY-MM-DD>-<slug>.pdf` (unless `markdown-only`)
   - `students/<id>/stories/<YYYY-MM-DD>-<slug>-companion.md`
   - Append one line to `students/<id>/stories/index.md`
7. **Report back to the professional:** story text, linter report (checks, pass/fix/flag),
   and file paths. End with: *"Draft for your review — please edit before use with the student."*

## Batch mode (the differentiation engine)

`/socialstory batch <situation brief> --students <id1,id2,...>` — run the pipeline once per
student from **one brief**. Each story must differ according to each dossier (reading level,
voice preference, interests, triggers, coping strategies) — this is the group-intervention
scenario (e.g. 6 students preparing for the same outing) that a generic chatbot cannot handle
without the professional re-pasting every dossier by hand. Produce a summary table: student,
file, flags needing review.

## Hard boundaries

- **No invented facts.** Anything not in the brief or dossier must be hedged with "usually" /
  "typically", or flagged as a question for the reviewer.
- **No clinical claims.** The story never labels the student, never mentions diagnosis, never
  frames the student as the problem.
- **No direct delivery.** Output is always addressed to the professional.
