# CaseCraft

CaseCraft is a WorkBuddy custom agent skill suite for the Agent Creativity Hackathon (WorkBuddy track), helping professionals (social workers, therapists, SEN teachers) support adolescents with mild-to-moderate autism spectrum disorder.

Its core artifact is the **Student Passport** — a living, versioned, single-source-of-truth document per student that coordinates every adult around the child. The passport is fed by a **session agent loop** (session capture → ingest → review → passport delta) and rendered into role-specific, linter-verified **stakeholder views** (teacher, parent, therapist, and the student's own materials).

The differentiator over a generic chatbot remains structural: every output is linted against an evidence-based methodology with a visible audit report, grounded in a longitudinal curated passport, and held consistent across all stakeholders in one pass — things a one-shot chatbot cannot do.

---

## 1. Why this product

An autistic student in Hong Kong is supported by a constellation of adults: a classroom teacher, a parent, an educational/behavioral therapist, and a school social worker. Each of them rebuilds an understanding of the same child from scratch — through meetings, forwarded notes, and guesswork. Information about the child lives in fragmented silos (school records, therapist notes, family conversations), goes stale, and never reaches the right person in the right form at the right time. Every school transition, new teacher, or new situation resets this understanding to zero.

CaseCraft is designed to replace this with one coordinated system: **one passport, kept current by every session, rendered into each stakeholder's own lens.**

---

## 2. The Agent Loop (system architecture)

```
┌───────────────────────────────────────────────────────────────────┐
│ 1. SESSION START — the worker sets the session goal first          │
│    /session marco --goal="work experience: ask for help              │
│    when unsure, no more than 2 prompts"                             │
├───────────────────────────────────────────────────────────────────┤
│ 2. CAPTURE (worker's device, parent consent recorded)               │
│    Audio + Video — transcription (Whisper) + body-language          │
│    analysis (MediaPipe, external engine)                            │
│    → OBSERVABLES ONLY: events, quotes, counts, timestamps           │
│    → NO emotional inference (hard rule — see §3)                    │
├───────────────────────────────────────────────────────────────────┤
│ 3. INGESTION — WorkBuddy skill /session reads the capture package   │
│    → structured session draft: observed events, goal progress,      │
│      staff-worthy quotes, "questions for the worker"                 │
├───────────────────────────────────────────────────────────────────┤
│ 4. REVIEW GATE — the worker approves or edits within ~90 seconds    │
│    (an capture never auto-commits — human-in-the-loop by design)    │
├───────────────────────────────────────────────────────────────────┤
│ 5. PASSPORT DELTA — versioned merge into the Student Passport       │
│    (goals, triggers, scripts, counts, freshness stamps)             │
├───────────────────────────────────────────────────────────────────┤
│ 6. STAKEHOLDER VIEWS — regenerate role-specific outputs             │
│    Teacher Guide · Parent Guide · Therapist Sheet · Social Story    │
│    · passport.html (family/team UI) — all linter-checked            │
└───────────────────────────────────────────────────────────────────┘
```

Tools flow: capture files drop into `sessions/<id>/` on the worker's local device → WorkBuddy skill `ingestion` orchestrates read + synthesis → outputs land under `students/<id>/`.

## 3. Hard principles (the moat)

1. **Observables, never inferences.** The capture layer emits *what happened* (covered ears when the fire alarm drill sounded) — never *how the child felt* (was anxious). Emotional inferences are not passed to the model and are not written into the passport. Inferred labels also fail with autistic children: movement patterns are individual and day-dependent, and no classifier reliably maps pose → affect.
2. **Human-in-the-loop review gate.** Auto-committed session summaries erode trust fast. The worker reviews a structured draft in ~90 seconds; anything ambiguous is surfaced to them as a question, and every passport change is attributable to an approved session.
3. **One source of truth.** The Student Passport is the single artifact all views derive from. Nobody re-types facts about the child; the passport is the dossier, the memory, and the audit trail in one.
4. **Verifiable output.** Two passes, both file-level: pass 1 generates documents; pass 2 reads the saved artifacts and lints them (methodology + cross-document consistency + **sensitivity leak check**). Some checks are deterministic (verbatim script presence across documents, freshness of sections) and can be shown on stage as facts, not claims.
5. **Local-first files.** Passport and sessions live in the worker's authorized local folders; prompts use pseudonyms; full identifiers stay local. All demo data (incl. media) is fictional/simulated.
6. **No clinical claims.** The passport describes *what supports the student* — never a diagnosis. The passport header carries an explicit "this is not a diagnostic/clinical document" line.

## 4. The Student Passport (the artifact)

Per-student living document: `students/<id>/passport.md` (plus `sessions/` and `packs/` folders).

| Section | Content | Sensitivity |
|---|---|---|
| Basics | Age, placement, reading level, languages | open |
| Communication profile | Literal/visual, scripts, help-seeking style | open |
| Triggers & sensory | Noise, transitions, crowding + coping plans | open (parent version simplified) |
| What works | Evidence from past support | open |
| Special interests | Regulation tools (e.g. MTR map) | open |
| Goals (current) | From support plan per term | team |
| Session log | Approved session facts, counted events, timestamps | team |
| Clinical/clinical | Diagnosis, medication, clinical reports | team/clinical (never in parent/teacher/student views) |

Versioning: every approved session delta bumps the version and refreshes the date stamp. A **freshness rule**: any section untouched for >30 days surfaces a flag in the next linter run — a stale passport is a liability, and perceiving staleness keeps the passport trustworthy.

## 5. Stakeholder views & the leak rule

The passport is never handed out raw. Stakeholders get role-specific views (see matrix):

| View | Contains | Never contains |
|---|---|---|
| Teacher Guide | Communication style, supports, warning signs, language to use/avoid | Diagnosis, clinical history |
| Parent Guide | What the child is preparing for, what to reinforce at home, plain language, optional Chinese | Diagnosis, clinical records |
| Therapist Summary | Full working detail, goals, session log | — (clinically scoped) |
| Student materials (Social Story) | Situation-specific narrative | Diagnosis, labels, "problem" framing |
| passport.html | Curated family/team dashboard (permission-filtered) | Anything not allowed for the viewer |

**Sensitivity leak check** (new linter class): every view is verified against `[open] / [team] / [clinical]` tags — a clinical-tagged section appearing in the Parent Guide is a blocking FLAG, the same way a 10.2 violation is. This is the demo moment other teams can't copy: catch a planted leak on stage.

## 6. Glossary

**Student Passport**: the living per-student source of truth described above. Supersedes and absorbs the former "Student Dossier" — same folder location, upgraded contract (sections, tags, versioning). Never the product of one prompt; always the product of a history of approved sessions.
_Avoid_: profile, record, file

**Coordinated Support Pack**: The set of audience-specific documents generated from the passport + a session/goal context, kept consistent by the linter. The differentiator is *coordination* — anyone can generate one document; generating several that agree with each other, and with the passport, is the moat.
_Avoid_: pack, bundle, set of documents

**Session**: One recorded interaction (therapy session, home visit, lesson observation) with a goal, a capture package, and an approved summary. The unit of intake for the passport.

**Agent Loop**: the 6-step pipeline in section 2. The shape of the product: capture → ingest → summarize → review → passport delta → views.
_Avoid_: pipeline (in pitch language), flow, automation

**Observables**: verifiable events captured from a session — quotes, counts, timestamps, occurrences ("covered ears when the alarm drill sound played"). The only thing the model may consume and the passport may record. Never emotions, never attributions.
_Avoid_: analysis, insights (for raw captures)

**Review Gate**: the ~90-second worker approval step before a session summary merges into the passport. Consent of the human is the trust mechanism of the system.
_Avoid_: approval flow, moderation

**Sensitivity Leak**: a linter finding where a restricted section (e.g. clinical) appears in a view that must not contain it (e.g. Parent Guide). Blocking FAIL.
_Avoid_: privacy error, data leakage

**Command**: The professional's entry surface. Primary: `/session <student-id> --goal="..."` (capture → summary → passport) and `/casecraft <student-id> "brief"` (specialized pack generation). No `--audiences` flag — audience tags live in the passport; the skill reads them.
_Avoid_: slash command, CLI, invocation

**Situation Brief**: Free-text context for document generation; the linter flags missing elements ("No timing info").
_Avoid_: brief, prompt, form

**Linter Report**: Audit trail per invocation: summary line in the response, full `linter-report.md` in the pack folder. Covers: methodology checks, cross-document consistency, freshness, sensitivity leaks, assumptions, questions for the reviewer.
_Avoid_: report, log

**Social Story**: personalised literal-language narrative for a specific situation (Carol Gray 10.2), optional teen-facing document of the pack. Linted against the 10.2 criteria.
_Avoid_: story, script, guide

**Teacher Guide / Parent Guide / Therapist Summary**: The role-specific views generated from the passport (see section 5). Written for busy mainstream professionals/non-specialists, plain language, correct register.
_Avoid_: lesson plan, letter home, staff briefing

**passport.html**: the readable, printable UI for families and teams, generated from the passport (permission-filtered). The hackathon's answer to "where do stakeholders actually read this".
_Avoid_: dashboard, portal, app

**Pilot Readiness**: The stage where a professional installs WorkBuddy, copies the skills, creates a real (pseudonymized) passport, and starts using the loop with no code changes. Actively piloting with HK Children & Youth Services is pitched as an aspiration, not a commitment.
_Avoid_: deployment, production

**Hackathon MVP**: One /session command + the review gate + passport delta + two views (Teacher Guide, Parent Guide) + leak-check linter. Batch = /session ... --batch across 2–3 fictional dossiers (Marco, Priya). Demo media is always fictional/simulated — no real child's audio/video is ever captured or shown.
_Avoid_: the product, v1, full version

## 7. Commands (surface)

```
/session <student-id> --goal="<goal>"                 # start a session (capture → draft → review)
/session <student-id> --summary <approve|edit> ...    # the review gate
/casecraft <student-id> "<situation brief>"           # generate a stakeholder pack
/casecraft <student-id> [lens=teacher|parent|therapist|story]
/session batch "…" --students id1,id2,…               # group sessions (one real brief → per-child deltas)
/passport <student-id> view [lens]                    # regenerate passport.html/view
```

## 8. Why not just a chatbot (the pitch in one paragraph)

A professional *can* paste session notes into Gemini and get a plausible teacher guide. What they cannot get: (1) **an audit** — every output is linted against methodology + consistency + sensitivity rules, with visible proof; (2) **a living passport** — one source of truth that accumulates across months, keeps voice, scripts, and facts aligned, and follows the student through transitions; (3) **the loop** — sessions feed the passport without the professional re-typing history, and stakeholder views re-render from a single approved delta. Generic chatbots start from zero every conversation. CaseCraft accumulates.

## 9. Roadmap (not in MVP)

- Messenger delivery: post generated view/PDF into Telegram/Slack for the relevant stakeholder (WorkBuddy remote control — "sponsored feature" demo).
- `/casenote`: rapid pre-passport capture for talks without recording.
- Employer Guide: work-experience lens for older teens.
- Teen co-authorship: a “my side” passport section the student co-edits (self-advocacy best practice).
- True emotion-adjacent research (with consent + human validation) — only ever outputs observables.
- Datasets & labels for event classification (still observable-only).