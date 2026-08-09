# CaseCraft — Coordinated Support Pack Skill (Hackathon Scaffold)

A WorkBuddy Custom Agent Skill that generates a **Coordinated Support Pack** — a set of
audience-specific documents (Teacher Guide, Parent Guide, optional Social Story) from one
Student Dossier and one situation brief, kept consistent with each other by cross-document
linting. The operator is a **professional** (social worker, therapist, SEN teacher) — never
the teen. Every output is a **draft for professional review**.

Built for the Agent Creativity Hackathon (WorkBuddy Track) —
https://luma.com/agentcreativity

## Structure

```
casecraft/
├── commands/
│   ├── session.md                     # /session — the primary command (agent loop)
│   └── casecraft.md                   # /casecraft — pack generation from passport
├── skills/
│   ├── session/
│   │   └── SKILL.md                   # Agent loop: capture → ingest → review → passport → views
│   └── casecraft/
│       ├── SKILL.md                   # Pack generation: passport → views → lint → save
│       └── templates/
│           ├── teacher-guide.md       # Teacher Guide generation rules
│           ├── parent-guide.md        # Parent Guide generation rules
│           ├── social-story.md        # Social Story generation rules (Carol Gray 10.2)
│           ├── linter-teacher-guide.md    # Teacher Guide linter checks
│           ├── linter-parent-guide.md     # Parent Guide linter checks
│           ├── linter-social-story.md     # Social Story linter checks (10.2 + cross-doc)
│           └── linter-sensitivity-leak.md # Sensitivity leak check (blocking)
├── students/                          # Fictional demo passports (per-student folders)
│   ├── marco/
│   │   ├── passport.md                # The Student Passport — living, versioned, tagged
│   │   ├── sessions/                  # Session capture packages land here
│   │   └── packs/                     # Generated stakeholder views land here
│   └── priya/
│       ├── passport.md                # Second demo passport — contrasting profile
│       ├── sessions/
│       └── packs/
└── examples/
    ├── marco-bakery-pack.md           # Worked example: full pack + linter report
    └── marco-bakery-session.md        # Worked example: full session loop
```

## Key design principles

1. **Observables, never inferences.** The capture layer emits what happened — quotes, counts,
   timestamps — never how the student felt. No emotional inference, no attribution.
2. **Human-in-the-loop review gate.** Nothing merges into the passport without the worker's
   approval. Auto-commit is off by design.
3. **One source of truth.** The Student Passport is the single artifact all views derive from.
   Nobody re-types facts about the child.
4. **Verifiable output.** Every document is linted against methodology, cross-document
   consistency, and sensitivity rules — with visible proof the professional can audit.
5. **Local-first files.** Passports and sessions live in the worker's authorized local folders;
   prompts use pseudonyms; full identifiers stay local. All demo data is fictional.

## Why not just a chatbot?

A professional *can* paste session notes into Gemini and get a plausible teacher guide. What
they cannot get:

- **An audit** — every output is linted against methodology + consistency + sensitivity rules,
  with visible proof. A chatbot gives you prose; CaseCraft gives you prose *and* an audit trail.
- **A living passport** — one source of truth that accumulates across months, keeps voice,
  scripts, and facts aligned, and follows the student through transitions. A chatbot starts
  from zero every conversation.
- **The loop** — sessions feed the passport without the professional re-typing history, and
  stakeholder views re-render from a single approved delta. Generic chatbots don't accumulate.

## Installing in WorkBuddy

Follow the WorkBuddy custom-skill doc (techpedia 144100, section 7):
- Add the skill Markdown + templates under WorkBuddy's `skills/` directory.
- Add `commands/session.md` and `commands/casecraft.md` under its `commands/` directory.
- Authorise WorkBuddy to access the `casecraft/` folder.

Then run, e.g.:

```
/session marco --goal="work experience: ask for help when unsure, no more than 2 prompts"
```

or

```
/casecraft marco "First work-experience placement at Sunbeam Bakery next Tuesday 19 Aug,
9:00–15:30. Travel by MTR Jordan → Mong Kok. Supervisor is Mrs. Chan. Jobs: bagging rolls,
labelling boxes. Kitchen is warm and mixers are loud."
```
