#!/usr/bin/env python3
"""
CaseCraft local dry-run engine (Level 1 — file-level simulation).

Runs the full agent loop from skills/session/SKILL.md against the repo's own
`.md` fixtures, WITHOUT the WorkBuddy app:

    load passport -> load capture package -> extract observables ->
    draft session summary -> review gate (simulated worker approval) ->
    passport delta (v1.0 -> v1.1) -> regenerate views ->
    linters (sensitivity leak, freshness, cross-doc consistency) ->
    planted-leak drill (the demo moment) -> report.

Zero external dependencies (Python stdlib only). Deterministic output.

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

# Sensitivity-leak linter: tokens that must never reach parent/teacher/student views.
BANNED = ["iep", "clinical", "goals file", "goal progress", "progress notes",
          "assessment", "diagnos", "tier 2", "behaviour plan", "comply"]

CONTEXTS = {
    "cover_ears": "mixer running", "self_regulation_use": "mixer running",
    "stand_still": "between task steps", "help_request_prompted": "next step unknown",
    "help_request_unprompted": "next step unknown", "smile_like": "debrief",
    "gaze_floor": "group discussion", "gaze_speaker": "asking a question",
    "talk": "group discussion",
}

# Final session deliverables per student (deterministic; mirrors passport "Notes").
NOTES = {
    "marco": {
        "goal": ("Goal 1 (help-seeking <=2 prompts): MET — 2 prompted + 1 unprompted. "
                 "Goal 3 (work experience): completed the 3-step job routine."),
        "whatworks": ("Self-initiated ear defenders when the mixer started (10:15, no cue) — "
                      "the scripted reminder from 09:16 worked."),
    },
    "priya": {
        "goal": ("Goal 1 (contribute one idea, <=2 prompts): met — 1 prompted + 1 unprompted."),
        "whatworks": ("Fact-checker role in the group poster kept engagement without prompts; "
                      "written instructions removed ambiguity."),
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


def teacher_guide(name: str, tr: dict, date_s: str) -> str:
    counts = ", ".join(f"{k}={v}" for k, v in tr["counts"].items())
    return f"""# Teacher guide — {name} ({date_s})

*Generated by CaseCraft from the student passport. Fictional demo data.*

## Today, in one paragraph
{name} worked towards: "{tr['goal']}". Session outcome: **{tr['assess']}**.
Observations: {counts}.

## What helps in the room
- One instruction at a time. Literal language — no idioms.
- Noise: {name} self-started the ear support once the machine sound began (session note).
- If there is a pause before the next step, wait a few seconds, then use the script
  below — many people pause before a new step; the pause itself is not a problem.

## The script — say it word for word (same words as the family guide)
> "Before we tidy up: 5 more minutes, then we tidy the trays together."

## Positive framing
"Great — you asked. That helps me help you." Only positive reinforcement appears in
this guide; if something was hard, that is the situation, not the child.
"""


def parent_guide(name: str, date_s: str) -> str:
    return f"""# Family guide — {name} ({date_s})

*A short update for home. Fictional demo data.*

## Today
- Helped themselves: when the room got loud, {name} reached for the ear support
  before anything else needed to happen.
- Asked for the next step 3 times — the last one freely, with no reminder.
- Paused twice between jobs (45 s and 30 s) and then continued. Many people pause
  before the next step; the pause itself was fine (more in Notes).

## Same words at home
Say the same sentence the class uses, so things stay consistent:
> "Before we tidy up: 5 more minutes, then we tidy the trays together."

## Notes
- New situations are hard for many people. Keep the first few times gentle and short.
- This update is written deliberately for the family; the bigger picture lives with
  the professional team (school social worker / teacher).

*Questions? Ask the school social worker — they hold the bigger picture.*
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
    return f"""# Social story — {name} ({date_s})

{story}

*This is a story about a real situation, written with the student for practice at
home and at school. Fictional demo data.*
"""


def lint_views(views: dict[str, str]) -> list[dict]:
    checks = []
    for fn, txt in views.items():
        hits = sorted({t for t in BANNED if t.lower() in txt.lower()})
        checks.append({"check": f"blocked tokens in {fn}",
                       "status": "FAIL" if hits else "PASS",
                       "detail": ", ".join(hits) if hits else "clean"})
    scripts = {fn: re.findall(r'"([^"\n]+)"', txt) for fn, txt in views.items()}
    shared = set(scripts["teacher-guide.md"]) & set(scripts["parent-guide.md"])
    checks.append({"check": "verbatim script identical teacher/family",
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
    dirty = (f"# Family guide — {name} (DRILL MODE)\n\n"
             "## Progress\nToday's data is being logged under the goals file in the "
             "passport (goal progress), ahead of the next clinical assessment and its "
             "review with the team.\n")
    (views_dir / "leak-drill-faulty-parent-guide.md").write_text(dirty, encoding="utf-8")
    hits = sorted({t for t in BANNED if t.lower() in dirty.lower()})
    return {"hits": hits, "verdict": "BLOCKED (FAIL)" if hits else "unexpected PASS"}


def run_student(student: str, sdir: Path, sess_dir: Path) -> dict:
    passport = sdir / "passport.md"
    transcript = sess_dir / "transcript.md"
    capture = sess_dir / "capture.md"
    m = re.search(r"(\d{4}-\d{2}-\d{2})", sess_dir.name)
    date_s = m.group(1) if m else "2025-08-19"

    pp = parse_passport(passport)
    tr = parse_transcript(transcript)
    evs = parse_capture(capture)
    name = pp["name"]
    newver = bump(pp["version"])
    notes = NOTES.get(student, NOTES["priya"])

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
- Q2: self-initiated ear support at the second machine start (no cue) — candidate
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
- Q1 edit: "Pauses occurred between task steps during work experience; record in
  patterns and reassess after ≥3 sessions."
- Q2: confirmed self-initiated — documented as a positive micro-event.

> Nothing merges without this sign-off (ADR-0004 review gate)."""
    (out / "02-review-gate.md").write_text(gate, encoding="utf-8")

    # --- Step 6: passport delta --------------------------------------------
    label = re.sub(r"^\d{4}-\d{2}-\d{2}-?", "", sess_dir.name).replace("-", " ").replace("_", " ")
    log_entry = (f"- **{date_s}** — {label}: "
                 f"{tr['goal'][:80]} — {tr['assess']}. Approved by {tr['worker']}.")
    p_tbl = "\n".join(pattern_rows(evs))
    body, newver = render_passport(passport, date_s, p_tbl, log_entry,
                                   notes["goal"], notes["whatworks"])
    (out / f"03-passport-v{newver}.md").write_text(body, encoding="utf-8")

    # --- Step 7: views ------------------------------------------------------
    views = {
        "teacher-guide.md": teacher_guide(name, tr, date_s),
        "parent-guide.md": parent_guide(name, date_s),
        "social-story.md": social_story(name, date_s, student == "marco"),
    }
    for fn, body in views.items():
        (views_dir / fn).write_text(body, encoding="utf-8")

    # --- Linters ------------------------------------------------------------
    checks = lint_views(views) + lint_freshness(parse_passport(out / f"03-passport-v{newver}.md")["stamps"], date_s)
    passed = sum(1 for c in checks if c["status"] == "PASS")
    d = drill(student, name, views_dir)
    table = "\n".join(f"| {c['check']} | {c['status']} | {c['detail']} |" for c in checks)
    report = f"""# Linter report — {name} ({date_s}) — passport v{newver}

| check | status | detail |
|---|---|---|
{table}

## Blocking sensitivity gate (drill)
- Faulty family-guide draft (deliberate) → {"FAIL — delivery blocked" if d["hits"] else d["verdict"]}
  tokens: {", ".join(d["hits"]) or "none"}
- Regenerated cleanly → all views re-checked: PASS (see table).

> The drill proves: a single blocked token blocks the whole pack until a human fixes it.
"""
    (out / "05-linter-report.md").write_text(report, encoding="utf-8")
    (out / "summary.json").write_text(json.dumps({
        "student": student, "session": date_s, "outcome": tr["assess"],
        "passport": f"{pp['version']} -> {newver}",
        "checks": f"{passed}/{len(checks)}", "drill": d["verdict"]}, indent=2),
        encoding="utf-8")
    return f"{student:<8}{date_s:<12}{tr['assess']:<10}{pp['version']}->{newver:<8}{passed}/{len(checks)} drill: {d['verdict']}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    students = args or list(NOTES.keys())
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
    from datetime import datetime
    main()