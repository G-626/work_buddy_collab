# Teacher Guide Template

Generate ONE Teacher Guide following every rule below. Rules marked ⚠️ are also enforced by
the linter (see `linter-teacher-guide.md`).

## 1. Audience

A busy mainstream teacher — not an autism specialist. They have 30 students, limited time,
and no training in ASD beyond a general awareness session. Write for someone who wants to
help but doesn't know how.

## 2. Purpose

Give the teacher three things: (1) what to expect from this student in this situation,
(2) what to do, (3) what to avoid. Everything must be actionable in a classroom with
29 other students present.

## 3. Language rules (⚠️ all linter-enforced)

- **Plain professional English.** No jargon ("executive function", "sensory processing",
  "stimming"). If a technical term is necessary, define it in one plain sentence.
- **Short sentences.** One idea per sentence. Bullet points over paragraphs.
- **Positive framing.** ⚠️ Say what TO do, not what NOT to do. ("Don't single her out" →
  "Give feedback privately, after class.")
- **Concrete actions, not principles.** "Be patient" is useless. "Wait 5 seconds after
  asking a question before repeating it" is useful.
- **No diagnosis language.** Never mention autism, ASD, or any label. The teacher may or
  may not know the student's diagnosis — the guide works either way.

## 4. Structure

1. **Header**: Student name, date, situation (one line).
2. **What to expect** (3–5 bullets): How this student is likely to behave in this situation.
   Grounded in the dossier's `[teacher]`-tagged sections. Frame as "many students find this
   hard" not "this student has a problem."
3. **What helps** (3–5 bullets): Specific, classroom-feasible actions the teacher can take.
   Drawn from the dossier's "What works" section. Each bullet is one action, one sentence.
4. **What to avoid** (2–3 bullets): Common teacher behaviours that backfire with this student.
   Frame positively where possible ("Give feedback privately" not "Don't criticise publicly").
5. **Language to use** (2–3 examples): Exact phrases the teacher can use, drawn from the
   dossier's communication profile and coping scripts. ⚠️ These phrases must be identical
   to those in the Parent Guide and Social Story (if generated).
6. **Warning signs** (2–3 bullets): What escalation looks like for this student, and what
   to do if the teacher sees it.

## 5. Personalisation rules (from the dossier)

- Only use sections tagged `[teacher]` or `[teacher, parent]` or `[teacher, parent, employer]`.
- **Special interests**: mention only if directly relevant to the classroom situation.
  Do not use as decoration.
- **Triggers**: include classroom-relevant triggers only. Home-specific triggers (e.g.
  bedtime routines) do not belong here.
- **What works**: prioritise strategies that are feasible in a mainstream classroom
  (a teacher cannot provide one-to-one support, but can adjust seating, give advance
  warning, or use written instructions).

## 6. Length

200–350 words. One page when printed. If it doesn't fit on one page, it's too long —
a busy teacher won't read it.

## 7. Uncertainty rule

If a fact is unknown (e.g. whether the student has met the new teacher before), either
phrase it as typical ("Most students benefit from meeting a new teacher before the first
lesson") or omit it and flag the question in the linter report. ⚠️ Never assert an
unstated fact.
