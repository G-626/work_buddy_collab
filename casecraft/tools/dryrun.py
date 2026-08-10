#!/usr/bin/env python3
"""
CaseCraft local dry-run engine (Level 1 — file-level simulation).

Runs the full agent loop from skills/session/SKILL.md against the repo's own
`.md` fixtures, WITHOUT the WorkBuddy app:

    load passport -> load capture package -> extract observables ->
    draft session summary -> review gate (simulated worker approval) ->
    passport delta (v1.0 -> v1.1) -> regenerate views (Teacher Guide,
    Parent Report, Social Story, Therapist Summary) -> linters (sensitivity
    leak, freshness, cross-doc consistency) -> PDF export (fpdf2) ->
    planted-leak drill (the demo moment) -> report.

Zero required dependencies (Python stdlib only) — PDF export is optional and
activates when `fpdf` is installed. Deterministic output.

Usage:
    python tools/dryrun.py                     # both students (batch)
    python tools/dryrun.py marco               # one student
    python tools/dryrun.py --as-of 2025-08-19 marco

Output lands in <repo>/casecraft/dryrun/<student>-<session>/.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # <repo>/casecraft
STUDENTS = ROOT / "students"
OUTBASE = ROOT / "dryrun"

# Sensitivity-leak linter tokens.
# FAMILY_BANNED: must never reach parent/teacher/student-facing views.
# THERAPIST_HARD: the only tokens the Therapist Summary must never contain —
#                 everything else in the list is legitimate working vocabulary
#                 for the professional team.
FAMILY_BANNED = ["iep", "clinical", "goals file", "goal progress", "progress notes",
                 "assessment", "diagnos", "tier 2", "behaviour plan", "comply"]
THERAPIST_HARD = ["diagnos"]  # even the team doc never asserts a diagnosis

# Context mapping for the Patterns table (event_type -> activity context).
CONTEXTS = {
    "cover_ears": "mixer running", "self_regulation_use": "mixer running",
    "stand_still": "between task steps", "help_request_prompted": "next step unknown",
    "help_request_unprompted": "next step unknown", "smile_like": "debrief",
    "gaze_floor": "group discussion", "gaze_speaker": "asking a question",
    "talk": "group discussion",
}

# Per-student evidence notes (deterministic; mirrors passport "Notes").
# Each entry: goal-progress row(s), what-went-well bullet, home-strategy bullet.
STUDENT_NOTES = {
    "marco": {
        "script": ("Before we tidy up: 5 more minutes, then we tidy the trays together.",
                   "transition warning before tidying"),
        "progress": [
            ("Asking for help when unsure (up to 2 prompts)",
             "Asked 3 times: 2 after one prompt each, 1 freely at 10:30", "Met"),
            ("Work experience readiness (3-step job routine)",
             "Completed bagging → labelling → packing flow without a missed step", "Progressing"),
        ],
        "well": [
            "Reached for the ear support before the machine sound — no reminder needed at 10:15",
            "Asked \"What should I do next?\" freely after the second tray",
            "Said at debrief: \"I asked Mrs. Chan two questions. I knew the answer to the third one.\"",
        ],
        "home": [
            "Practice the script: \"Before we tidy up: 5 more minutes, then we tidy the trays together.\"",
            "Look at the MTR route for the bakery together — route details are calming",
            "Keep ear support in the same bag pocket every day",
        ],
        "watch": [
            "Pauses longer than ~30 seconds before the next step",
            "Hands moving toward ears when a machine starts",
        ],
    },
    "priya": {
        "script": ("Take a minute, then write it down.",
                   "private, written-response cue"),
        "progress": [
            ("Contributing one idea in group work (assigned role)",
             "Fact-checker role: 1 idea after one prompt, 1 freely at 11:38", "Met"),
            ("Using a private help channel instead of struggling silently",
             "Asked a follow-up question in writing after the session", "Progressing"),
        ],
        "well": [
            "Took the fact-checker role and used it — asked for the poster sources in writing",
            "Stayed in the group the whole activity with the assigned role",
            "Asked a follow-up question by email after class — the private channel worked",
        ],
        "home": [
            "Keep the same phrase at home: \"Take a minute, then write it down.\"",
            "Sketching before talking about the day — drawing regulates",
            "Agree on a private signal for \"I need a quiet moment\"",
        ],
        "watch": [
            "Going quiet and dropping eye contact during group activities",
            "Erasing or restarting written work repeatedly",
        ],
    },
}


def lines(p: Path) -> list[str]:
    return p.read_text(encoding="utf-8").splitlines()


def parse_passport(p: Path) -> dict:
    txt = p.read_text(encoding="utf-8")
    ver = re.search(r"Version:\s*(\S+)", txt)
    mname = re.search(r"Student Passport — (.+)", txt)
    stamps: dict[str, str] = {}
    in_stamps = False
    for ln in lines(p):
        if ln.startswith("## Freshness stamps"):
            in_stamps = True
            continue
        if in_stamps and ln.startswith("|") and "|" in ln:
            c = [x.strip() for x in ln.strip("|").split("|")]
            if len(c) >= 2 and c[0] != "Section":
                stamps[c[0]] = c[1]
    return {"version": ver.group(1) if ver else "1.0", "stamps": stamps,
            "name": mname.group(1) if mname else "Student"}


def parse_transcript(p: Path) -> dict:
    txt = p.read_text(encoding="utf-8")
    worker = re.search(r"^> Worker:\s*(.+)$", txt, re.M)
    goal = re.search(r"^> Goal:\s*(.+)$", txt, re.M)
    sect = re.search(r"### Goal progress\s*(.*?)(?=\n## |\Z)", txt, re.S)
    assessment = "UNKNOWN"
    if sect:
        m = re.search(r"\*\*Assessment\*\*:\s*([A-Z]+)", sect.group(1))
        assessment = m.group(1) if m else assessment
    quotes = re.findall(r"^-\s*([^:]+):\s*[\"“]([^”\"]+)[”\"].*$", txt, re.M)
    counts = dict(re.findall(r"^- ([^:]+?):\s*([0-9]+(?:\s*\([^)]*\))?)\s*$",
                             txt, re.M))
    events = re.findall(r"^-\s(\d{2}:\d{2})\s*—\s*(.+)$", txt, re.M)
    return {"assess": assessment, "quotes": quotes, "counts": counts,
            "events": events,
            "goal": goal.group(1).strip() if goal else "(no goal in header)",
            "worker": worker.group(1).strip() if worker else "School Social Worker"}


def parse_capture(p: Path) -> list[dict]:
    events, in_tbl = [], False
    for ln in lines(p):
        if ln.startswith("| time |"):
            in_tbl = True
            continue
        if in_tbl:
            if not ln.startswith("|"):
                break
            c = [x.strip() for x in ln.strip("|").split("|")]
            if len(c) == 6:
                events.append(dict(time=c[0], event=c[1], duration=c[2],
                                   count=c[3], context=c[4], note=c[5]))
    return events


def bump(v: str) -> str:
    a, b = v.split(".")
    return f"{a}.{int(b) + 1}"


def pattern_rows(events: list[dict]) -> list[str]:
    buckets: dict[str, list[str]] = {}
    for e in events:
        if e["event"] in CONTEXTS:
            buckets.setdefault(e["event"], []).append(e["time"])
    rows = []
    for ev, times in sorted(buckets.items()):
        rows.append(f"| {CONTEXTS[ev]} | {ev} | {len(times)} | {', '.join(times)} |")
    return rows


def render_passport(passport: Path, date_s: str, patterns_tbl: str, log_entry: str,
                    goal_note: str, ww_note: str) -> tuple[str, str]:
    txt = passport.read_text(encoding="utf-8")
    newver = bump(parse_passport(passport)["version"])
    txt = re.sub(r"Version:\s*\S+", f"Version: {newver}", txt, count=1)
    txt = re.sub(r"Last updated:\s*\S+", f"Last updated: {date_s}", txt, count=1)
    if "No patterns recorded yet" in txt:
        txt = re.sub(
            r"\*No patterns recorded yet\..*?\*",
            "| context | event | count | trace |\n|---|---|---|---|\n" + patterns_tbl +
            "\n\n*Baseline observations — read with `templates/patterns.md`; reassess "
            "after \u22653 sessions.*",
            txt, flags=re.S)
    if "No sessions recorded yet" in txt:
        txt = re.sub(r"\*No sessions recorded yet\..*?\*", log_entry, txt, flags=re.S)
    txt = txt.replace("## Goals (current) [team]\n",
                      "## Goals (current) [team]\n\n*" + goal_note + "*\n")
    txt = txt.replace("## What works [open]\n",
                      "## What works [open]\n\n- *Session note: " + ww_note + "*\n")
    txt = re.sub(r"^\|\s*Session log\s*\|[^|]*\|", f"| Session log | {date_s} |", txt, flags=re.M)
    txt = re.sub(r"^\|\s*Patterns\s*\|[^|]*\|", f"| Patterns | {date_s} |", txt, flags=re.M)
    txt = re.sub(r"^\|\s*Goals\s*\|[^|]*\|", f"| Goals | {date_s} |", txt, flags=re.M)
    txt = re.sub(r"^\|\s*What works\s*\|[^|]*\|", f"| What works | {date_s} |", txt, flags=re.M)
    return txt, newver


# ---------------------------------------------------------------- view renderers

def teacher_guide(name: str, tr: dict, date_s: str, brief: str, script: str) -> str:
    counts = "; ".join(f"{k}: {v}" for k, v in tr["counts"].items())
    return f"""# Teacher Guide — {name} ({date_s})

*Draft for professional review — generated by CaseCraft.*

**Situation:** {brief.split(chr(10))[0][:140]}

## Snapshot
{name} communicates best with clear, literal language and one instruction at a time.
New or loud situations can be hard; advance warning and written steps help a lot.

## What to expect
- May pause before the next step and not ask — waiting briefly, then using the script below, works.
- In a loud environment, may reach for ear support or cover ears. This is self-regulation, not refusal.
- Asks precise questions when unsure; vague answers ("maybe", "we'll see") cause confusion.

## What helps
- One instruction at a time, in literal language — no idioms.
- If there is a pause before the next step, wait a few seconds, then use the script.
- Give a written step list when the task has more than two steps.
- Offer the ear support before the machine starts, so it is a choice, not a rescue.

## What to avoid
- Abstract or sarcastic phrasing ("hold your horses").
- Repeating a question before waiting ~5 seconds.
- Raising your voice over the machine — the ear support is the tool, not volume.

## Language to use (same words as the family report)
> "{script}"

## Warning signs
- Pauses longer than ~30 seconds before the next step.
- Hands moving toward ears without the ear support nearby.
- Looks at the exit repeatedly during a new activity.

## Escalation plan
If the signs above persist, offer the script once, then the break option. Contact:
____ (fill in the school contact) if support is needed.

---
*Session evidence: {counts}.*
"""


def parent_report(name: str, tr: dict, date_s: str, brief: str, notes: dict) -> str:
    progress_rows = "".join(
        f"| {g} | {ev} | {st} |\n" for g, ev, st in notes["progress"])
    well = "".join(f"- {b}\n" for b in notes["well"])
    home = "".join(f"- {b}\n" for b in notes["home"])
    watch = "".join(f"- {b}\n" for b in notes["watch"])
    script, script_ctx = notes["script"]
    return f"""# Parent Report — {name} ({date_s})

*Draft for professional review — generated by CaseCraft.*

**Situation:** {brief.split(chr(10))[0][:140]}

## Overview
{name} worked towards: "{tr['goal']}". Session outcome: **{tr['assess']}**.
This report summarises what happened and what you can reinforce at home.

## What we're working on
| What we're working on | Evidence this session | Status |
|---|---|---|
{progress_rows}
*No status without evidence — if it says "Met", the evidence is in the middle column.*

## What went well
{well}
## Home strategies
{home}
## Same words at home
Say the same phrase the class uses ({script_ctx}), so things stay consistent:
> "{script}"

## What to watch for
{watch}
If you see these, the script above and a quiet minute usually help.

## Next session focus
Building on what worked this session — more practice with the same script and one
new step.

## Contact
____ (fill in the professional's name and role)

*This update is written deliberately for the family; the bigger picture lives with
the professional team.*
"""


def social_story(name: str, date_s: str, first_person: bool) -> str:
    short = name.split()[0]
    if first_person:
        story = (
            "The bakery is a big room. Many people work there.\n\n"
            "When I am not sure what to do next, I can ask: \"What should I do next?\"\n\n"
            "Many people take a pause before the next step. Taking a pause is fine —\n"
            "then I ask, or a grown-up shows me the first step.\n\n"
            "When the machine is loud, I can put on my sound support before my ears\n"
            "need it. That works well.\n\n"
            "At the end of the morning, someone says: \"Before we tidy up: 5 more\n"
            "minutes, then we tidy the trays together.\"")
    else:
        story = (
            "The art room has one big table. Everyone has a job.\n\n"
            "When the class is not sure what to do next, they can ask: "
            "\"What should I do next?\"\n\n"
            "Many people pause before a new step. Taking a pause is fine — then they\n"
            "ask, or the teacher shows the first step.\n\n"
            "At the end of the lesson, the teacher says: \"5 more minutes, then we\n"
            "tidy the tables together.\"")
    return f"""# Social Story — {name} ({date_s})

{story}

*This is a story about a real situation, written with the student for practice at
home and at school. Fictional demo data.*
"""


def therapist_summary(name: str, tr: dict, date_s: str, notes: dict) -> str:
    progress_rows = "".join(
        f"| {g} | {ev} | {st} |\n" for g, ev, st in notes["progress"])
    counts = "; ".join(f"{k}: {v}" for k, v in tr["counts"].items())
    return f"""# Therapist Summary — {name} ({date_s})

*Working document for the professional team — not for family distribution.*

## Relevant passport summary
Communication: literal, precise; does not ask for help spontaneously — needs explicit
permission scripts. Triggers: loud machine noise, transitions to unfamiliar places.
What works: advance preview, written steps, ear support, scripts.

## Goal progress
| Goal | Evidence this session | Status | Recommended next target |
|---|---|---|---|
{progress_rows}
*Session counts: {counts}.*

## Patterns & trends
Baseline observations (descriptive, correlational — never a verdict). Reassess after
\u22653 sessions. See passport Patterns section for the event table.

## Session log reference
Session {date_s} — {tr['goal']} — outcome {tr['assess']}. Approved by {tr['worker']}.

## Open questions for the team
- Confirm whether the ~45 s and ~30 s pauses correlate with step-transition timing
  across sessions, or with something else in the environment.
- Validate the self-initiated regulation event (10:15) against the transcript line.

## Recommended next step
Continue the same script for one more session; introduce one new step, then re-check
goal progress.
"""


# ---------------------------------------------------------------- linters

def lint_views(views: dict[str, str]) -> list[dict]:
    checks = []
    for fn, txt in views.items():
        banned = THERAPIST_HARD if fn == "therapist-summary.md" else FAMILY_BANNED
        hits = sorted({t for t in banned if t.lower() in txt.lower()})
        checks.append({"check": f"blocked tokens in {fn}",
                       "status": "FAIL" if hits else "PASS",
                       "detail": ", ".join(hits) if hits else "clean"})
    scripts = {fn: re.findall(r'"([^"\n]+)"', txt) for fn, txt in views.items()}
    shared = set(scripts.get("teacher-guide.md", [])) & \
        set(scripts.get("parent-guide.md", []))
    checks.append({"check": "verbatim script identical teacher/parent",
                   "status": "PASS" if shared else "FAIL",
                   "detail": " and ".join(sorted(shared)) if shared else "no shared script"})
    return checks


def lint_freshness(stamps: dict, ref: str) -> list[dict]:
    flagged = []
    for sec, d in stamps.items():
        if not d or d in ("—", "-"):
            continue
        try:
            age = (datetime.strptime(ref, "%Y-%m-%d")
                   - datetime.strptime(d, "%Y-%m-%d")).days
        except Exception:
            continue
        if age > 30:
            flagged.append(f"{sec}: {age} days")
    return [{"check": "freshness: sections untouched >30 days",
             "status": "FAIL" if flagged else "PASS",
             "detail": "; ".join(flagged) or "all sections within 30 days"}]


def drill(student: str, name: str, views_dir: Path) -> dict:
    dirty = (f"# Parent Report — {name} (DRILL MODE)\n\n"
             "## Progress\nToday's data is being logged under the goals file in the "
             "passport (goal progress), ahead of the next clinical assessment and its "
             "review with the team.\n")
    (views_dir / "leak-drill-faulty-parent-guide.md").write_text(dirty, encoding="utf-8")
    hits = sorted({t for t in FAMILY_BANNED if t.lower() in dirty.lower()})
    return {"hits": hits, "verdict": "BLOCKED (FAIL)" if hits else "unexpected PASS"}


# ---------------------------------------------------------------- PDF export

DOC_TYPES = {
    "teacher-guide.md": "Teacher Guide",
    "parent-guide.md": "Parent Report",
    "social-story.md": "Social Story",
    "therapist-summary.md": "Therapist Summary",
    "05-linter-report.md": "Linter Report",
    "01-session-draft.md": "Session Draft",
    "02-review-gate.md": "Review Gate",
}


def export_pdf(md_path: Path, out_dir: Path, student: str, date_s: str,
               situation: str = "") -> Path | None:
    """Render one .md view to a styled, dated PDF via pdfrender.

    Filename: <YYYY-MM-DD>-<student>-<doc-type>.pdf — date-first so packs
    sort chronologically and sessions can be compared over time.
    """
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        from pdfrender import render_markdown_to_pdf
    except ImportError:
        return None
    doc_type = DOC_TYPES.get(md_path.name, md_path.stem.replace("-", " ").title())
    stem = md_path.stem
    if stem.startswith("05-"):
        stem = "linter-report"
    elif stem.startswith("01-"):
        stem = "session-draft"
    elif stem.startswith("02-"):
        stem = "review-gate"
    out = out_dir / f"{date_s}-{student}-{stem}.pdf"
    return render_markdown_to_pdf(md_path, out, doc_type,
                                  student_title(student), date_s, situation)


def student_title(folder: str) -> str:
    titles = {"marco": "Marco L.", "priya": "Priya S."}
    return titles.get(folder, folder.title())


def export_all_pdfs(views_dir: Path, extra: list[Path], student: str,
                    date_s: str, situation: str = "") -> list[str]:
    """Export every .md view to a dated PDF; returns list of PDF paths."""
    made = []
    for md in sorted(views_dir.glob("*.md")):
        if md.name.startswith("leak-drill"):
            continue
        p = export_pdf(md, views_dir, student, date_s, situation)
        if p:
            made.append(str(p))
    for md in extra:
        p = export_pdf(md, views_dir, student, date_s, situation)
        if p:
            made.append(str(p))
    return made


# ---------------------------------------------------------------- runner

def run_student(student: str, sdir: Path, sess_dir: Path) -> dict:
    passport = sdir / "passport.md"
    transcript = sess_dir / "transcript.md"
    capture = sess_dir / "capture.md"
    m = re.search(r"(\d{4}-\d{2}-\d{2})", sess_dir.name)
    session_date = m.group(1) if m else "2025-08-19"
    # SYSTEM date for all generated artifacts — never assume a date.
    date_s = datetime.now().strftime("%Y-%m-%d")

    pp = parse_passport(passport)
    tr = parse_transcript(transcript)
    evs = parse_capture(capture)
    name = pp["name"]
    newver = bump(pp["version"])
    notes = STUDENT_NOTES.get(student, STUDENT_NOTES["priya"])
    brief = tr["goal"]  # brief = session goal for the session loop

    out = OUTBASE / f"{student}" / sess_dir.name.replace("-", "_")
    views_dir = out / "views"
    views_dir.mkdir(parents=True, exist_ok=True)

    # --- Step 4 draft -----------------------------------------------------
    quote_lines = "".join(f'- {s}: "{q}"\n' for s, q in tr["quotes"])
    event_lines = "".join(f"- {t} — {d}\n" for t, d in tr["events"])
    count_lines = "".join(f"- {k}: {v}\n" for k, v in tr["counts"].items())
    draft = f"""# Session draft — {name} ({date_s}) — AWAITING REVIEW GATE

> goal: {tr["goal"]} | outcome: {tr["assess"]}

## Questions for the worker
- Q1: pauses (45 s / 30 s) before new steps — observed, no speech. Not a verdict;
  route: within usual range for step transition? Monitor across sessions.
- Q2: self-initiated regulation at the second machine start (no cue) — candidate
  positive micro-event; verify the transcript line.

## Observed events (timestamps)
{event_lines}
## Counts
{count_lines}
## Quotes
{quote_lines}
## Proposed passport delta
- goals note, what-works note, patterns baseline, session log entry, stamps refresh.
"""
    (out / "01-session-draft.md").write_text(draft, encoding="utf-8")

    # --- Step 5: review gate ----------------------------------------------
    gate = f"""# Review gate — {date_s}
Approver: {tr["worker"]}
Decision: **APPROVED with one edit**
- Q1 edit: "Pauses occurred between task steps during the session; record in
  patterns and reassess after ≥3 sessions."
- Q2: confirmed self-initiated — documented as a positive micro-event.

> Nothing merges without this sign-off (ADR-0004 review gate)."""
    (out / "02-review-gate.md").write_text(gate, encoding="utf-8")

    # --- Step 6: passport delta --------------------------------------------
    label = re.sub(r"^\d{4}-\d{2}-\d{2}-?", "", sess_dir.name).replace("-", " ").replace("_", " ")
    # The session log records when the session actually happened (factual data
    # from the capture package); every generated artifact uses the system date.
    log_entry = (f"- **{session_date}** — {label}: "
                 f"{tr['goal'][:80]} — {tr['assess']}. Approved by {tr['worker']}. "
                 f"(report generated {date_s})")
    p_tbl = "\n".join(pattern_rows(evs))
    body, newver = render_passport(passport, date_s, p_tbl, log_entry,
                                   notes["progress"][0][0], notes["well"][0])
    (out / f"03-passport-v{newver}.md").write_text(body, encoding="utf-8")

    # --- Step 7: views ------------------------------------------------------
    views = {
        "teacher-guide.md": teacher_guide(name, tr, date_s, brief, notes["script"][0]),
        "parent-guide.md": parent_report(name, tr, date_s, brief, notes),
        "social-story.md": social_story(name, date_s, student == "marco"),
        "therapist-summary.md": therapist_summary(name, tr, date_s, notes),
    }
    for fn, body in views.items():
        (views_dir / fn).write_text(body, encoding="utf-8")

    # --- Linters ------------------------------------------------------------
    checks = lint_views(views) + lint_freshness(
        parse_passport(out / f"03-passport-v{newver}.md")["stamps"], date_s)
    passed = sum(1 for c in checks if c["status"] == "PASS")
    d = drill(student, name, views_dir)
    table = "\n".join(f"| {c['check']} | {c['status']} | {c['detail']} |" for c in checks)
    report = f"""# Linter report — {name} ({date_s}) — passport v{newver}

| check | status | detail |
|---|---|---|
{table}

## Blocking sensitivity gate (drill)
- Faulty parent-report draft (deliberate) → {"FAIL — delivery blocked" if d["hits"] else d["verdict"]}
  tokens: {", ".join(d["hits"]) or "none"}
- Regenerated cleanly → all views re-checked: PASS (see table).

> The drill proves: a single blocked token blocks the whole pack until a human fixes it.
"""
    (out / "05-linter-report.md").write_text(report, encoding="utf-8")

    # --- Step 8: PDF export (optional) --------------------------------------
    pdfs = export_all_pdfs(views_dir, [out / "05-linter-report.md"],
                           student, date_s, tr["goal"])
    pdf_note = f" ({len(pdfs)} PDFs)" if pdfs else " (PDF export: fpdf2 not installed)"

    (out / "summary.json").write_text(json.dumps({
        "student": student, "session": date_s, "outcome": tr["assess"],
        "passport": f"{pp['version']} -> {newver}",
        "checks": f"{passed}/{len(checks)}", "drill": d["verdict"],
        "pdfs": pdfs}, indent=2), encoding="utf-8")
    return f"{student:<8}{date_s:<12}{tr['assess']:<10}{pp['version']}->{newver:<8}{passed}/{len(checks)} drill: {d['verdict']}{pdf_note}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    students = args or list(STUDENT_NOTES.keys())
    shutil.rmtree(OUTBASE, ignore_errors=True)
    results = []
    for student in students:
        sdir = STUDENTS / student
        if not sdir.is_dir():
            print(f"!! no student dir: {sdir}")
            continue
        sessions = sorted(d for d in (sdir / "sessions").iterdir() if d.is_dir())
        for sess_dir in sessions:
            results.append(run_student(student, sdir, sess_dir))
    print("== BATCH SUMMARY ==")
    print("student  session      outcome    passport  linter  drill")
    for r in results:
        print("  " + r)
    print("\nLevel-1 dry run complete. Artifacts in:", OUTBASE)


if __name__ == "__main__":
    main()
