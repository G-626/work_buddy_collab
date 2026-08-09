# CaseCraft — SocialStory Skill (Hackathon Scaffold)

A WorkBuddy Custom Agent Skill that drafts **methodology-compliant, personalised Social Stories**
for adolescents with mild-to-moderate ASD. The operator is a **professional** (social worker,
therapist, SEN teacher) — never the teen. Every output is a **draft for professional review**.

Built for the Agent Creativity Hackathon (WorkBuddy Track) —
https://luma.com/agentcreativity

## Structure

```
casecraft/
├── commands/
│   └── socialstory.md                 # Slash command definition (/socialstory)
├── skills/
│   └── socialstory/
│       ├── SKILL.md                   # Skill orchestration (inputs → pipeline → outputs)
│       └── templates/
│           ├── story-template.md      # Generation rules (sentence types, language, register)
│           ├── linter-checklist.md    # Methodology linter (checks + auto-fix rules)
│           └── companion-template.md  # Staff/parent one-pager template
├── students/                          # Fictional demo dossiers (per-student folders)
│   └── marco/
│       ├── profile.md                 # The dossier — professional-curated student profile
│       └── stories/
│           └── index.md               # Longitudinal story library index
└── examples/
    └── marco-bakery-story.md          # Worked example: draft story + linter report
```

## Key design principles

1. **Describe, don't command.** Stories follow Carol Gray's Social Stories 10.2 methodology:
   descriptive sentences ≥ 2× coaching sentences, first/third person only, literally accurate.
2. **The dossier personalises, the professional approves.** Personalisation comes from the
   worker's curated `profile.md`, not the teen's self-report.
3. **The linter enforces the methodology** — sentence ratio, WH-question coverage, perspective,
   literal language, positive framing, fact-grounding — and shows its work in a report the
   reviewer can trust.
4. **Local data stays local.** Dossiers live in local folders under WorkBuddy's sandboxed
   execution. All demo data is fictional.

## Why not just a chatbot?

A professional *can* paste notes into Gemini and get a plausible story. What they cannot get:

- **An audit against the methodology.** Practitioner-made materials routinely drift from the
  10.2 criteria; fidelity declines without ongoing support. The linter checks every draft and
  shows pass/fix/flag per criterion.
- **Longitudinal consistency.** The dossier + story library keep voice, scripts, reading level,
  and facts consistent across months of materials, and recycle past achievements into applause.
- **One brief → many students.** Batch mode produces per-student differentiated stories for a
  whole intervention group from a single brief — in a chatbot, that means re-pasting every
  dossier by hand.

## Installing in WorkBuddy

Follow the WorkBuddy custom-skill doc (techpedia 144100, section 7):
- Add the skill Markdown + templates under WorkBuddy's `skills/` directory.
- Add `commands/socialstory.md` under its `commands/` directory.
- Authorise WorkBuddy to access the `casecraft/` folder.

Then run, e.g.:

```
/socialstory marco "First work-experience placement at Sunbeam Bakery next Tuesday 19 Aug,
9:00–15:30. Travel by MTR Jordan → Mong Kok. Supervisor is Mrs. Chan. Jobs: bagging rolls,
labelling boxes. Kitchen is warm and mixers are loud."
```
