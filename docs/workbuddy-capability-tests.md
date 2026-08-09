# WorkBuddy Capability Tests

**Purpose**: Before committing to an idea (Social Story skill vs. "Bridge" multi-audience engine),
verify that WorkBuddy can actually perform the file operations both ideas depend on. Run these
tests on the WorkBuddy device. Testing is asynchronous — batch the tests, run them in one session,
record results here.

**Decision rule** (from discussion):
- If T1–T6 mostly pass → either idea is viable; pick on merit (likely Bridge).
- If T1–T4 pass but T5–T6 fail → Social Story skill only (simpler, already scaffolded).
- If T1–T3 fail → rethink entirely; WorkBuddy may not support skill-based file workflows.

---

## T1 — Folder access (prerequisite for everything)

**Test**: Authorize WorkBuddy to access a folder (e.g. `~/casecraft-test/`) containing one
markdown file with the text `DOSSIER_CONTENT_MARKER`. Ask WorkBuddy: "Read the file in the
casecraft-test folder and tell me what word it contains."

**Pass if**: WorkBuddy reads the file and returns the marker word.
**Fail if**: Permission error, or WorkBuddy says it cannot access local files.

---

## T2 — Write one file

**Test**: Ask WorkBuddy: "Create a file called `output-test.md` in the casecraft-test folder
with the content `WRITE_SUCCESS`."

**Pass if**: File exists in the folder with the expected content.
**Fail if**: WorkBuddy only produces chat output, no file written.

---

## T3 — Write multiple files in one run

**Test**: Ask WorkBuddy: "In the casecraft-test folder, create three files: `a.md` with content
`FILE_A`, `b.md` with content `FILE_B`, and `c.md` with content `FILE_C`."

**Pass if**: All three files exist with correct content.
**Fail if**: Only one file written, or files written but empty/wrong.

**Why this matters**: Both ideas need to produce multiple outputs from one invocation
(story + linter report + companion; or teacher + parent + employer versions).

---

## T4 — Read multiple files and cross-reference

**Test**: Create two files in the test folder:
- `dossier.md` containing: `Student name: TestStudent. Reading level: age 11. Interest: trains.`
- `brief.md` containing: `Situation: first day at a bakery. Noise: loud mixers.`

Ask WorkBuddy: "Read both files in casecraft-test and write a new file `combined.md` that
mentions the student's interest and the noise concern from the brief."

**Pass if**: `combined.md` contains references to trains AND loud mixers (i.e., WorkBuddy read
and synthesised both files).
**Fail if**: Output only references one source, or WorkBuddy says it can only process one file.

**Why this matters**: The dossier + brief pattern is the core of both ideas.

---

## T5 — Custom skill registration (the hackathon deliverable)

**Test**: Following the custom-skill doc (techpedia 144100, section 7):
1. Create a minimal skill markdown file (e.g. `SKILL.md` with a trivial instruction like
   "When invoked, write `SKILL_RAN` to a file called `skill-test.md`").
2. Register it in WorkBuddy's `skills/` directory.
3. Invoke it.

**Pass if**: The skill is discovered and executed; the output file is written.
**Fail if**: WorkBuddy doesn't recognise the skill, or the registration steps in the doc
don't match reality.

**Note**: This is the hackathon's core deliverable format. If this fails, we need to know
immediately — it may mean custom skills work differently than documented.

---

## T6 — Slash command with arguments

**Test**: Create a minimal slash command definition (e.g. `/testcmd <arg>`) that writes the
argument value to a file. Register it in WorkBuddy's `commands/` directory. Invoke it as
`/testcmd hello_world`.

**Pass if**: Command is recognised, argument is captured, and a file containing `hello_world`
is written.
**Fail if**: Command not recognised, or arguments not passed through.

**Why this matters**: The professional's UX is `/socialstory marco "situation brief"` or
`/bridge marco "new placement"`. If slash commands can't take arguments, the UX degrades to
pasting instructions in natural language (still works, but less clean).

---

## T7 — Batch / iterate over multiple inputs

**Test**: Create three files: `student-a.md`, `student-b.md`, `student-c.md`, each with
different content (e.g. different names and interests). Ask WorkBuddy: "For each student file
in the casecraft-test folder, create a file called `output-<name>.md` that says 'Hello <name>,
your interest is <interest>.'"

**Pass if**: Three output files are created, each personalised to the correct student.
**Fail if**: Only one output created, or outputs are generic (not personalised per file).

**Why this matters**: This is the "differentiation engine" (one brief → N students). If
WorkBuddy can't iterate, batch mode requires the professional to run the command N times
manually — weaker demo but not fatal.

---

## T8 — Read files written in a previous session (longitudinal memory)

**Test**: In session 1, ask WorkBuddy to write a file `memory.md` containing `FACT: the student
uses ear defenders for loud noise`. Close WorkBuddy. In session 2 (new conversation), ask
WorkBuddy: "Read memory.md in casecraft-test and write a story that includes the fact from
that file."

**Pass if**: The new output references ear defenders (i.e., WorkBuddy can read files written
in a previous conversation, not just the current one).
**Fail if**: WorkBuddy can't access files from prior sessions, or can't find the file.

**Why this matters**: The longitudinal dossier + story library depend on this. Without it,
every invocation starts from zero and the "consistency over time" argument collapses.

---

## T9 — PDF generation

**Test**: Ask WorkBuddy: "Create a PDF in casecraft-test called `test.pdf` containing the
text 'PDF generation test'."

**Pass if**: PDF file exists and opens correctly.
**Fail if**: No PDF, or only markdown/text output possible.

**Why this matters**: Both ideas promise "print-ready PDF" output for professionals. If PDF
generation isn't available, the fallback is markdown-only (still usable, less polished).

---

## T10 — Template / variable substitution

**Test**: Create a template file `template.md` with placeholders: `Hello {{name}}, your
reading level is {{level}}.` Ask WorkBuddy: "Read template.md and dossier.md from
casecraft-test, fill in the placeholders using the dossier data, and write the result to
`filled.md`."

**Pass if**: `filled.md` contains the dossier values substituted into the template.
**Fail if**: Placeholders left as-is, or WorkBuddy can't follow the template structure.

**Why this matters**: Both ideas rely on templates (story template, companion template,
linter checklist). If WorkBuddy can't do variable substitution, templates become reference
documents the LLM reads for style guidance rather than fill-in templates — workable but
requires different prompt engineering.

---

## Scoring sheet

| Test | Description | Result | Notes |
|---|---|---|---|
| T1 | Folder access | ✅ PASS | |
| T2 | Write one file | ✅ PASS | |
| T3 | Write multiple files | ✅ PASS | |
| T4 | Read + cross-reference | ✅ PASS | |
| T5 | Skill registration | ✅ PASS | |
| T6 | Slash command + args | ✅ PASS | |
| T7 | Batch iteration | ✅ PASS | |
| T8 | Cross-session file read | ✅ PASS | |
| T9 | PDF generation | ✅ PASS | |
| T10 | Template substitution | ✅ PASS | |

**All tests passed. Output files confirmed at `~/casecraft-test` on the WorkBuddy machine.**

## Outcome

- [x] All/most pass → proceed with chosen idea (Bridge or Social Story)
- [ ] T1–T4 pass, T5–T6 fail → natural-language UX instead of slash commands; still viable
- [ ] T7 fails → drop batch mode; single-student invocation only
- [ ] T8 fails → drop longitudinal claims; single-session tool only (major rethink needed)
- [ ] T9 fails → markdown-only output; adjust pitch
- [ ] T1–T3 fail → WorkBuddy may not be suitable; escalate before investing more time

**Decision: all constraints cleared. The platform supports every capability both candidate
ideas require (file read/write, batch, cross-session memory, skill registration, slash
commands with args, PDF, templates). Idea selection should now be made on merit, not on
feasibility risk.**
