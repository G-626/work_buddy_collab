# CaseCraft

CaseCraft is a WorkBuddy custom agent skill, built for the Agent Creativity Hackathon (WorkBuddy track), that helps professionals (social workers, therapists) who support adolescents with mild-to-moderate autism spectrum disorder. Its differentiator over generic chatbots: every output is **linted against an evidence-based methodology with a visible audit report**, grounded in a longitudinal professional-curated dossier, and filed into a per-student library — things a one-shot chatbot structurally cannot do.

## Language

**CaseCraft**:
The product — a WorkBuddy custom agent skill suite for ASD support professionals. See [ADR-0001](docs/adr/0001-professional-facing-tool.md) for why we build for professionals, not teens.
_Avoid_: the app, the tool, the assistant, the chatbot, Bridge (former working name, retired)

**Coordinated Support Pack**:
The core abstraction CaseCraft produces: a set of audience-specific documents generated from one Student Dossier and one situation brief, kept consistent with each other and with the student's history by the linter and the dossier. The differentiator over a chatbot is *coordination* — anyone can generate one document; generating several that agree with each other is the moat. Implemented as a single WorkBuddy skill with one command and multiple output templates — not multiple skills — because WorkBuddy has no documented sub-skill mechanism, and the consistency check must run across all documents in one pass.
_Avoid_: pack, bundle, set of documents, Bridge (this is what "Bridge" was trying to name)

**Command**:
The professional's entry point: `/casecraft <student-id> "<situation brief>"`. No `--audiences` flag — the skill reads the Student Dossier's audience tags and generates the appropriate documents automatically. The dossier is the control mechanism: if a section is tagged `[teacher]`, the Teacher Guide is generated; if tagged `[parent]`, the Parent Guide is generated. This keeps the command surface minimal (one brief, one pack) and eliminates the mismatch risk of the professional requesting an audience the dossier doesn't cover.
_Avoid_: slash command, CLI, invocation

**Situation Brief**:
The free-text input the professional types into the Command. No structured template — the skill markdown includes a brief-writing guide ("A good brief covers: what, when, where, who, what the student will do, what's known to be hard") and the linter flags missing elements (e.g. "No timing information provided — story will use vague language"). Free text keeps the interaction natural; the guide and linter catch thin briefs.
_Avoid_: brief, input, prompt, form

**Linter Report**:
The audit trail for one Command invocation. Two levels of visibility: (1) a **summary line** in the command response — e.g. "3 documents generated, 12 checks passed, 2 auto-fixed, 1 flagged for your review" — this is the demo moment that shows the tool doing work, not just generating text. (2) The **full report** saved to `linter-report.md` in the Pack Folder — every check, pass/fix/flag status, before→after for auto-fixes, assumptions made, questions for the reviewer. The full report is for the professional's audit needs (supervision, quality assurance), not for sharing with teachers or parents.
_Avoid_: report, log, output

**Pack Folder**:
The output of one Command invocation: a dated folder under `students/<id>/packs/<YYYY-MM-DD>-<slug>/` containing one file per generated document (`teacher-guide.md`, `parent-guide.md`, optional `social-story.md`) plus `linter-report.md` (the audit trail, for the professional — not shared). Individual files map to the professional's sharing workflow (send Teacher Guide to teacher, Parent Guide to parent). PDF generation is roadmap (`--format pdf`).
_Avoid_: output folder, results, deliverables

**Cross-Document Consistency Check**:
The linter pass that runs across all documents in a Coordinated Support Pack to verify they agree with each other. Two levels in the Hackathon MVP: (1) **Shared facts** — factual claims (times, names, strategies, coping options) are extracted from each document and contradictions are flagged (e.g. Teacher Guide says 5-min warning, Parent Guide says 10-min warning → FLAG). (2) **Shared language** — key phrases (coping scripts, transition cues) must appear word-for-word identical across all documents that use them. A third level (coverage — every dossier trigger addressed in at least one document) is roadmap.
_Avoid_: consistency linter, cross-check, alignment pass

**Pilot Readiness**:
The project is designed so a real professional could install WorkBuddy, copy the skill files, create a real Student Dossier (with pseudonymisation per ADR-0002), and start using it with no code changes. The demo dossiers are examples, not the product. A one-page "getting started" guide and pseudonymisation checklist are part of the hackathon deliverable. Actively piloting with HK Children & Youth Services is pitched as an aspiration (closing slide), not a commitment — overpromising before knowing the charity's capacity damages credibility.
_Avoid_: deployment, production, launch

**Hackathon MVP**:
The committed hackathon scope: one command that produces a Coordinated Support Pack with two audiences — Teacher Guide and Parent Guide — from one Student Dossier and one situation brief. The Social Story is retained as an optional third document within the pack (not a standalone command). Employer Guide is designed-for but not built — the output directory structure and template registry must make adding a new audience a matter of dropping in a new template, not restructuring. `/casenote` and `/parentupdate` remain cut (thin chatbot wrappers). `/iepgoals` is roadmap. Demo lead: single-student pack generation, then batch across 2–3 fictional dossiers. Demo narrative: lead with the identical-sentence moment (Level 2 — show one coping script appearing word-for-word in both guides), then follow with the contradiction catch (Level 1 — a deliberate contradiction planted in the fictional dossier, flagged by the linter). Development constraint: WorkBuddy runs on a separate device; testing is asynchronous.
_Avoid_: the product, v1, full version

**Case Note**:
A structured clinical record generated from rough session observations. Distinguishes "observed" from "inferred" and never invents progress. Cut from MVP — thin chatbot wrapper. Roadmap only.
_Avoid_: note, record, summary

**Social Story**:
A personalised, literal-language narrative that prepares a teen for a specific situation, following Carol Gray's Social Stories 10.2 methodology. In the Coordinated Support Pack, it is the **optional teen-facing document** — the skill decides whether to include it based on the situation brief and dossier (e.g. a new transition or unfamiliar event warrants one; a routine situation may only need Teacher + Parent guides). This keeps the demo focused while showing the skill makes judgements, not just generates documents. Linted against the 10.2 criteria.
_Avoid_: story, script, guide

**Teacher Guide**:
A staff-facing document in the Coordinated Support Pack: what the teacher should know about the student's upcoming situation, classroom strategies to reinforce, warning signs to watch for, and language to use (and avoid). Written for a busy mainstream teacher, not a specialist.
_Avoid_: lesson plan, classroom notes, staff briefing

**Parent Guide**:
A parent/caregiver-facing document in the Coordinated Support Pack: what the student is preparing for, what to reinforce at home, what language to use (consistent with the Teen Guide and Teacher Guide), and what to avoid saying. Plain language, adjustable reading level, optional Chinese.
_Avoid_: parent update, letter home, caregiver notes

**Employer Guide**:
A workplace-facing document in the Coordinated Support Pack: what an employer or supervisor should know, task expectations, communication tips, and what to avoid. Relevant only for older teens in work experience. Roadmap — not in the Hackathon MVP.
_Avoid_: job description, HR notes

**Parent Update**:
A plain-language summary generated from case notes, for parents/caregivers. Cut from MVP — thin chatbot wrapper. Superseded by the Parent Guide within the Coordinated Support Pack. Roadmap only.
_Avoid_: update, email, report

**Student Dossier**:
A folder of professional-curated files (assessment.md, profile.md, past notes) that personalises all outputs. Written by the professional, not the teen. The main file (`profile.md`) uses **audience tags** on each section (e.g. `[teacher]`, `[parent]`, `[teacher, parent]`) to declare which audiences that section is relevant to — the skill reads tags to select content per audience, rather than inferring relevance. In the hackathon demo, all dossiers are fully fictional. For privacy, professionals should use pseudonyms or initials in prompts; full identifiers stay in local files only. See [ADR-0002](docs/adr/0002-privacy-reframing.md).

Demo dossiers: **Marco** (14, literal thinker, MTR interest, loud-noise sensitivity, ear defenders) and **Priya** (15, strong verbal skills, high social anxiety, masking behaviour, no sensory issues, visual learner, art interest) — chosen for maximum contrast so personalisation is undeniable in a 5-minute demo. A third dossier is stretch scope.
_Avoid_: profile, record, file

**Professional**:
The social worker, therapist, or counsellor who operates CaseCraft. The beneficiary is the teen, but the professional is the user.
_Avoid_: user, operator, clinician
