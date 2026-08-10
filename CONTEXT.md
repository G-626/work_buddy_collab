# CaseCraft

CaseCraft is a WorkBuddy custom agent skill suite for the Agent Creativity Hackathon (WorkBuddy track), helping professionals (social workers, therapists, SEN teachers) support adolescents with mild-to-moderate autism spectrum disorder.

Its core artifact is the **Student Passport** — a living, versioned, single-source-of-truth document per student that coordinates every adult around the child. The passport is fed by a **session agent loop** (session capture → ingest → review → passport delta) and rendered into role-specific, linter-verified **stakeholder views** (teacher, parent, therapist, and the student's own materials).

The differentiator over a generic chatbot remains structural: every output is linted against an evidence-based methodology with a visible audit report, grounded in a longitudinal curated passport, and held consistent across all stakeholders in one pass — things a one-shot chatbot cannot do.

---

## 1. Why this product

An autistic student in Hong Kong is supported by a constellation of adults: a classroom teacher, a parent, an educational/behavioral therapist, and a school social worker. Each of them rebuilds an understanding of the same child from scratch — through meetings, forwarded notes, and guesswork. Information about the child lives in fragmented silos (school records, therapist notes, family conversations), goes stale, and never reaches the right person in the right form at the right time. Every school transition, new teacher, or new situation resets this understanding to zero.

CaseCraft replaces this with one coordinated system: **one passport, kept current by every session, rendered into each stakeholder's own lens.**

---

## 2. The Agent Loop (system architecture)

```
┌───────────────────────────────────────────────────────────────────┐
│ 1. SESSION START — the worker sets the session goal first          │
│    /session marco --goal="work experience: ask for help            │
│                       when unsure, ≤2 prompts"                     │
├───────────────────────────────────────────────────────────────────┤
│ 2. CAPTURE (worker's device, parent consent recorded)              │
│    a) Audio  → Local Whisper skill (on-device transcription) →     │
│                transcript                                          │
│    b) Video  → Capture Engine (MediaPipe landmarks) served as      │
│                an MCP server → Movement Event Stream (JSON)        │
│    → OBSERVABLES ONLY: events, quotes, counts, timestamps          │
│    → NO emotional inference; faces are landmarks-only,             │
│      anonymized by default (see §4)                                │
├───────────────────────────────────────────────────────────────────┤
│ 3. INGEST — WorkBuddy orchestrates: reads transcript + event       │
│    stream → structured session draft (observed events, goal        │
│    progress, quotes, "questions for the worker")                   │
├───────────────────────────────────────────────────────────────────┤
│ 4. REVIEW GATE — the worker approves or edits within ~90 seconds   │
│    (capture never auto-commits — human-in-the-loop by design)      │
├───────────────────────────────────────────────────────────────────┤
│ 5. PASSPORT DELTA — versioned merge into the Student Passport      │
│    (goals, triggers, scripts, movement-pattern counts, stamps)     │
├───────────────────────────────────────────────────────────────────┤
│ 6. STAKEHOLDER VIEWS — regenerate role-specific outputs            │
│    Teacher Guide · Parent Report · Therapist Sheet · Social Story   │
│    · passport.html (family/team UI) — all linter-checked           │
├───────────────────────────────────────────────────────────────────┤
│ 7. (platform-native, optional) AUTOMATION — scheduled freshness    │
│    checks + weekly stakeholder digest pushed via Assistant         │
│    (Telegram/Slack/WeCom…)                                          │
└───────────────────────────────────────────────────────────────────┘
```

Tools flow: capture files and event streams land in `sessions/<id>/` on the worker's local device → WorkBuddy orchestrates ingestion (calling the Capture Engine as an MCP tool, transcription via Local Whisper) → outputs land under `students/<id>/`.

## 3. Hard principles (the moat)

1. **Observables, never inferences.** The capture layer emits *what happened* (covered ears when the fire alarm drill sounded) — never *how the child felt* (was anxious). Movement event streams contain only descriptive primitives (gait, gaze targets, proxemics, gestures) plus counts and timestamps. Inferred labels fail with autistic children: movement patterns are individual and day-dependent, and no classifier reliably maps pose → affect. This is also the demo principle: evidence, not judgment.
2. **Positive reinforcement first.** All outputs are framed through reinforcement and support. Findings are expressed as *what works, what motivates, what to do more of*. Events that could be read negatively appear only as neutral observables routed to the worker as questions — never as a verdict on the child (see §4).
3. **Human-in-the-loop review gate.** Auto-committed session summaries erode trust fast. The worker reviews a structured draft in ~90 seconds; anything ambiguous is surfaced as a question, and every passport change is attributable to an approved session.
4. **One source of truth.** The Student Passport is the single artifact all views derive from. Nobody re-types facts about the child; the passport is the dossier, the memory, and the audit trail in one.
5. **Verifiable output.** Two passes, both file-level: pass 1 generates documents; pass 2 reads the saved artifacts and lints them (methodology + cross-document consistency + **sensitivity leak check**). Some checks are deterministic (verbatim script presence across documents, freshness of sections) and can be shown on stage as facts, not claims.
6. **Local-first files + anonymized capture.** Passport and sessions live in the worker's authorized local folders; prompts use pseudonyms; full identifiers stay local. Capture streams are landmark-only (no faces, no raw frames retained, no identity matching). All demo data (incl. media) is fictional/simulated.
7. **No clinical claims.** The passport describes *what supports the student* — never a diagnosis. The passport header carries an explicit "this is not a diagnostic/clinical document" line. Pattern data supports professional judgment; it never renders a diagnosis.

## 4. Movement & facial capture — the solution (descriptive, positive-first)

**What the capture layer does — and what it refuses to do.** The goal of video capture is to *understand and describe movement* so the team can spot triggers, habits, and patterns over time — not to label the child's feelings. The engine therefore outputs a **Movement Event Stream**: JSON records of the form `{observed_at, event_type, duration_ms, counts, context}` where `event_type` is drawn from a fixed descriptive vocabulary:

- **Body**: stands, sits, paces, rocks, hand movement, covers ears/eyes, self-touch, approaches/withdraws (proxemics)
- **Gaze**: looks at speaker, looks at task, looks away, scans room (head pose + gaze target)
- **Voice-adjacent**: talks, laughs, shouts, vocalizes (cross-referenced from the transcript)
- **Positive micro-events**: smile-like mouth-corner rise (calibrated threshold), spontaneous initiation (talk + gaze-to-speaker co-occurrence)

**What facial tracking contributes.** Face analysis is limited to *descriptive, identity-free signals*: gaze target, head orientation, mouth-open/smile-like events, blink-rate band (as an alert-neutral observable for fatigue — reviewed by a human, never auto-concluded). Face recognition, identity matching, and affect labels (angry/happy/anxious) are **disabled by default** and not part of the MVP. The child's face is never stored — the stream keeps landmarks only.

**Longitudinal pattern layer (the analytical value).** The passport's **Patterns** section aggregates event counts across sessions, aligned to context: what activity was happening, what sounds/transitions occurred, time of day. Output is descriptive and correlational:

> "Pacing clustered during the bakery tutorial (6 of 10 minutes) on drill days; 0 during quiet desk work. Mixer-sound onset was present in 4 of 5 pacing windows. Ear-covering events dropped from 3 → 0 after the 5-minute warning script was introduced."

Patterns like this *are* the "additional analytical data for future use" — they let the team compare sessions, test hypotheses, and see whether an intervention moved a count. They are never rendered as a verdict, and any surprising pattern is routed to the worker as a question, not a statement about the child.

**Positive-reinforcement-only rendering rule.** Every user-facing sentence that involves the child's data is expressed as reinforcement or support. "Negative" observations are translated: event counts feed sentences like *"Marco completed 4 self-regulation breaks; the predictable mixer briefing kept transitions smooth"* or are posed as neutral questions to the worker (*"Pacing appeared in 6/10 minutes of the tutorial — worth checking whether a new stressor or regulated movement was involved?"*). The system never emits *"Marco was anxious"* — ever.

## 5. WorkBuddy integration surfaces (verified against official docs)

The loop is built on documented platform capabilities, so "sponsored product usage" is deep, not cosmetic:

| Capability (official doc) | How CaseCraft uses it | Depth |
|---|---|---|
| **Skill Marketplace + Custom Skills** | The skill suite itself; marketplace skills reused (Local Whisper, Office Suite, Agent Browser) | core |
| **Local Whisper skill** | On-device transcription of session audio — no audio leaves the device | core |
| **MCP (Model Context Protocol)** | The Capture Engine (MediaPipe) ships as a local MCP server; WorkBuddy calls it as a tool inside a task (OAuth supported) | core |
| **Automation** | Nightly passport freshness check; weekly parent/teacher digest generation (per-workspace directory, scheduled) | deep |
| **Assistant remote control** | 9 messengers (Slack, Telegram, Discord, WeCom, Feishu, DingTalk, QQ, YuanbaoPai, WeChat Bot): worker triggers /session from the field; digest auto-pushed to stakeholders | deep |
| **Connectors** | Google Drive/Gmail/Notion for school documents and parent communications in later pilots | medium |
| **Task continuation** | Per-student task threads keep longitudinal context natively between sessions | medium |
| **Memory** | Conversation memory (nightly regeneration) reinforces the passport's stability claims | medium |
| **File Recognition practice** | PDF/DOCX/XLSX/PNG/JPG batch processing with parallel execution — the pack generation backbone | core |
| **Zero-code Local Apps + built-in browser** | passport.html viewer (family/team UI) built in Coding Mode, previewed in WorkBuddy's built-in browser | demo |
| **AI Self-Driven** | Multi-step autonomous pipeline (capture → summary → delta → views) with human review gates | core |

**Two honest caveats from the docs:**
1. **Skill file format discrepancy:** the techpedia guide says custom skills are "a simple Markdown file" (templates under `skills/`, commands under `commands/`), while the official practice case describes `skill.yml` + implementation files. Both exist in the wild — the repo scaffold uses the Markdown form, and **T5 must be re-run against the installed app to confirm which format the current build accepts** before the event.
2. **No native video processing:** WorkBuddy documents file formats (PDF/DOCX/XLSX/images) but not video. That's why the MediaPipe pass is an external engine behind an MCP server — WorkBuddy stays the orchestrator, and the capture stays local.

## 6. The Student Passport (the artifact)

Per-student living document: `students/<id>/passport.md` (plus `sessions/`, `patterns/`, and `packs/` folders).

| Section | Content | Sensitivity |
|---|---|---|
| Basics | Age, placement, reading level, languages | open |
| Communication profile | Literal/visual, scripts, help-seeking style | open |
| Triggers & sensory | Noise, transitions, crowding + coping plans | open (parent version simplified) |
| What works | Evidence from past support | open |
| Special interests | Regulation tools (e.g. MTR map) | open |
| Goals (current) | From support plan per term | team |
| Patterns | Movement-event counts + trends across sessions (descriptive) | team |
| Session log | Approved session facts, counted events, timestamps | team |
| Clinical | Diagnosis, medication, clinical reports | team/clinical (never in parent/teacher/student views) |

Versioning: every approved session delta bumps the version and refreshes the date stamp. A **freshness rule**: any section untouched for >30 days surfaces a flag in the next linter run — a stale passport is a liability, and perceiving staleness keeps the passport trustworthy.

## 7. Stakeholder views & the leak rule

The passport is never handed out raw. Stakeholders get role-specific views (see matrix):

| View | Contains | Never contains |
|---|---|---|
| Teacher Guide | Communication style, supports, warning signs, language to use/avoid | Diagnosis, clinical history |
| Parent Report | What the child is preparing for, what to reinforce at home, plain language, optional Chinese | Diagnosis, clinical records |
| Therapist Summary | Full working detail, goals, patterns (descriptive), session log | — (clinically scoped) |
| Student materials (Social Story) | Situation-specific narrative | Diagnosis, labels, "problem" framing |
| passport.html | Curated family/team dashboard (permission-filtered) | Anything not allowed for the viewer |

**Sensitivity leak check** (new linter class): every view is verified against `[open] / [team] / [clinical]` tags — a clinical-tagged section appearing in the Parent Report is a blocking FLAG. This is the demo moment other teams can't copy: catch a planted leak on stage.

## 8. Glossary

**Student Passport**: the living per-student source of truth described above. Supersedes and absorbs the former "Student Dossier" — same folder location, upgraded contract (sections, tags, versioning). Never the product of one prompt; always the product of a history of approved sessions.
_Avoid_: profile, record, file

**Coordinated Support Pack**: the set of audience-specific documents generated from the passport + a session/goal context, kept consistent by the linter. The differentiator is *coordination* — anyone can generate one document; generating several that agree with each other, and with the passport, is the moat.
_Avoid_: pack, bundle, set of documents

**Session**: one recorded interaction (therapy session, home visit, lesson observation) with a goal, a capture package, and an approved summary. The unit of intake for the passport.

**Agent Loop**: the 7-step pipeline in section 2. The shape of the product: capture → ingest → summarize → review → passport delta → views → (optional) automation push.
_Avoid_: pipeline (in pitch language), flow, automation

**Movement Event Stream**: the descriptive JSON output of the Capture Engine — `{observed_at, event_type, duration_ms, counts, context}` with a fixed observable vocabulary. Never affect, never a state label.
_Avoid_: emotion data, analytics, insights

**Capture Engine**: the on-device MediaPipe-based pipeline served to WorkBuddy as a local MCP server. Produces the Movement Event Stream; faces are landmarks-only; no raw frames retained.
_Avoid_: vision model, CCTV, tracker

**Positive-First Rule**: all user-facing output is framed as reinforcement/support; observations that could read negatively become neutral observables + a question to the worker, never a verdict.
_Avoid_: negative framing, behavior scoring

**Review Gate**: the ~90-second worker approval step before a session summary merges into the passport. Consent of the human is the trust mechanism of the system.
_Avoid_: approval flow, moderation

**Sensitivity Leak**: a linter finding where a restricted section (e.g. clinical) appears in a view that must not contain it (e.g. Parent Report). Blocking FAIL.
_Avoid_: privacy error, data leakage

**Command**: the professional's entry surface. Primary: `/session <student-id> --goal="..."` (capture → summary → passport) and `/casecraft <student-id> "brief"` (specialized pack generation). No `--audiences` flag — audience tags live in the passport; the skill reads them.
_Avoid_: slash command, CLI, invocation

**Situation Brief**: free-text context for document generation; the linter flags missing elements ("No timing info").
_Avoid_: brief, prompt, form

**Linter Report**: audit trail per invocation: summary line in the response, full `linter-report.md` in the pack folder. Covers: methodology checks, cross-document consistency, freshness, sensitivity leaks, assumptions, questions for the reviewer.
_Avoid_: report, log

**Social Story**: personalised literal-language narrative for a specific situation (Carol Gray 10.2), optional teen-facing document of the pack. Linted against the 10.2 criteria.
_Avoid_: story, script, guide

**Teacher Guide / Parent Report / Therapist Summary**: the role-specific views generated from the passport (see section 7). Written for busy mainstream professionals/non-specialists, plain language, correct register.
_Avoid_: lesson plan, letter home, staff briefing

**passport.html**: the readable, printable UI for families and teams, generated from the passport (permission-filtered). Built in WorkBuddy's Coding Mode and previewed in its built-in browser.
_Avoid_: dashboard, portal, app

**Pilot Readiness**: the stage where a professional installs WorkBuddy, copies the skills, creates a real (pseudonymized) passport, and starts using the loop with no code changes. Actively piloting with HK Children & Youth Services is pitched as an aspiration, not a commitment.
_Avoid_: deployment, production

**Hackathon MVP**: one `/session` command + the review gate + passport delta + two views (Teacher Guide, Parent Report) + leak-check linter + the MCP capture-engine demo (movement event stream → patterns section). Batch = `/session ... --batch` across 2–3 fictional dossiers (Marco, Priya). Demo media is always fictional/simulated — no real child's audio/video is ever captured or shown.
_Avoid_: the product, v1, full version

## 9. Commands (surface)

```
/session <student-id> --goal="<goal>"                 # start a session (capture → draft → review)
/session <student-id> --summary <approve|edit> ...    # the review gate
/casecraft <student-id> "<situation brief>"           # generate a stakeholder pack
/casecraft <student-id> [lens=teacher|parent|therapist|story]
/session batch "…" --students id1,id2,…               # group sessions (one goal → per-child deltas)
/passport <student-id> view [lens]                    # regenerate passport.html/view
/passport <student-id> patterns                       # movement-pattern trends (descriptive)
```

## 10. Why not just a chatbot (the pitch in one paragraph)

A professional *can* paste session notes into Gemini and get a plausible teacher guide. What they cannot get: (1) **an audit** — every output is linted against methodology + consistency + sensitivity rules, with visible proof; (2) **a living passport** — one source of truth that accumulates across months, keeps voice, scripts, and facts aligned, and follows the student through transitions; (3) **the loop** — sessions feed the passport without the professional re-typing history, and stakeholder views re-render from a single approved delta; (4) **descriptive movement patterns** — on-device capture converts sessions into longitudinal, positive-first observations that inform support without ever judging the child. Generic chatbots start from zero every conversation. CaseCraft accumulates.

## 11. Roadmap (not in MVP)

- WeCom (企業微信) enterprise rollout — the standard channel in HK schools/NGOs.
- `/casenote`: rapid pre-passport capture for talks without recording.
- Employer Guide: work-experience lens for older teens.
- Teen co-authorship: a "my side" passport section the student co-edits (self-advocacy best practice).
- Consent-aware research tracks for affect-adjacent signals — only ever outputs observables, always human-reviewed.
- Datasets & labels for event classification (still observable-only).
- Connector-driven integration with school SIS/Google Drive for document exchange (medium-term pilots).