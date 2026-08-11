#!/usr/bin/env python3
"""CaseCraft 10-slide hackathon deck (fpdf2, A4 landscape).

Design rules (shared with casecraft/tools/pdfrender.py):
- ONE accent colour (deep blue 31,78,121); hierarchy via font weight/size only.
- Mirrored padding: every text frame is vertically centred, top pad == bottom pad.
- Real system dates only (2026-08-12). No status colours, no zebra.
"""
from fpdf import FPDF

PRIMARY = (31, 78, 121)
BAND_SUB = (200, 216, 232)
INK = (34, 40, 46)
MUTED = (110, 118, 126)
PAPER = (255, 255, 255)
W, H = 297, 210
ML, MR = 18, 18          # side margins (mirrored)
MT = 34                   # content starts below the band
MB = 16                   # bottom margin (mirrored with slide-footer gap)

class Deck(FPDF):
    def __init__(self):
        super().__init__(orientation="L", unit="mm", format="A4")
        self.set_auto_page_break(False)
        self.slide_no = 0
        self.set_margins(ML, MT, MR)
        fdir = r"C:\Windows\Fonts"
        self.add_font("Arial", "", fdir + r"\arial.ttf")
        self.add_font("Arial", "B", fdir + r"\arialbd.ttf")
        self.add_font("Arial", "I", fdir + r"\ariali.ttf")
        self.add_font("Arial", "BI", fdir + r"\arialbi.ttf")
        self.set_font("Arial", "", 10.5)

    def header(self):
        self.slide_no += 1
        self.set_fill_color(*PRIMARY)
        self.rect(0, 0, W, 14, "F")
        self.set_font("Arial", "B", 11)
        self.set_text_color(*BAND_SUB)
        self.set_xy(ML, 3.4)
        self.cell(0, 7, f"{self.section_label}  ·  CASECRAFT", align="L")
        self.set_font("Arial", "", 9)
        self.set_xy(W - ML - 30, 3.4)
        self.cell(30, 7, f"{self.slide_no:02d} / 10", align="R")

    def footer(self):
        self.set_y(H - 10)
        self.set_font("Arial", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 5, "CaseCraft — Agent Creativity Hackathon 2026 (WorkBuddy track) — 2026-08-12", align="C")

    def title_slide(self, kicker, title, subtitle, meta, note):
        self.section_label = "CASECRAFT"
        self.add_page()
        # centered block with mirrored padding
        block_h = 110
        y0 = (H - block_h) / 2
        self.set_xy(ML, y0)
        self.set_font("Arial", "B", 12)
        self.set_text_color(*PRIMARY)
        self.cell(0, 8, kicker, align="C")
        self.ln(14)
        self.set_font("Arial", "B", 34)
        self.set_text_color(*INK)
        self.multi_cell(W - ML - MR, 16, title, align="C")
        self.ln(4)
        self.set_font("Arial", "", 13.5)
        self.set_text_color(*MUTED)
        self.multi_cell(W - ML - MR, 8, subtitle, align="C")
        self.ln(10)
        self.set_font("Arial", "B", 11.5)
        self.set_text_color(*PRIMARY)
        self.multi_cell(W - ML - MR, 7, meta, align="C")
        self.ln(6)
        self.set_font("Arial", "I", 9.5)
        self.set_text_color(*MUTED)
        self.multi_cell(W - ML - MR, 6, note, align="C")

    def slide(self, label, title, blocks, image=None, img_w=0, img_h=0, img_cap=""):
        self.section_label = label
        self.add_page()
        # title
        self.set_xy(ML, 22)
        self.set_font("Arial", "B", 20)
        self.set_text_color(*INK)
        self.multi_cell(W - ML - MR, 11, title, align="L")
        y = self.get_y() + 3
        # optional image (left) or full-width blocks
        if image:
            self.set_xy(ML, y + 2)
            self.image(image, w=img_w, h=img_h)
            if img_cap:
                self.set_font("Arial", "I", 8.5)
                self.set_text_color(*MUTED)
                self.set_xy(ML, y + 2 + img_h + 1.5)
                self.multi_cell(img_w, 4.5, img_cap, align="C")
            tx = ML + img_w + 10
            tw = W - ML - MR - img_w - 10
            self.render_blocks(blocks, tx, y, tw)
        else:
            self.render_blocks(blocks, ML, y, W - ML - MR)
        # mirrored bottom padding: equal space below content
        self.set_y(H - MB - 4)

    def render_blocks(self, blocks, x, y, w):
        self.set_xy(x, y)
        for kind, text in blocks:
            if kind == "h":
                self.set_font("Arial", "B", 12.5)
                self.set_text_color(*PRIMARY)
                self.multi_cell(w, 7, text, align="L")
                self.ln(1.2)
            elif kind == "b":
                self.set_font("Arial", "", 10.5)
                self.set_text_color(*INK)
                self.multi_cell(w, 6.1, text, align="L", markdown=True)
                self.ln(0.8)
            elif kind == "gap":
                self.ln(3)
            elif kind == "note":
                self.set_font("Arial", "I", 9)
                self.set_text_color(*MUTED)
                self.multi_cell(w, 5.2, text, align="L")
                self.ln(1)

def main():
    d = Deck()
    d.title_slide(
        "AGENT CREATIVITY HACKATHON 2026 · WORKBUDDY TRACK",
        "CaseCraft",
        "Coordinated Support Packs from an Autism Passport —\none agent run, four audiences, one audited record.",
        "Team CaseCraft · enochfyw@gmail.com · github.com/G-626/work_buddy_collab",
        "Verified in the real WorkBuddy app on 2026-08-12 (Level-2). Demo data is fictional.",
    )
    d.slide(
        "PROBLEM",
        "One child. Five adults. Five partial pictures.",
        [
            ("b", "An autism student is supported by parents, a class teacher, subject teachers, a social worker and a therapist. Each keeps **their own notes** — different names for the same trigger, different instructions for the same transition."),
            ("b", "Reports arrive **late, duplicated and inconsistent**; a teacher gets a strategy memo, the parent gets a clinical phrase no one explained."),
            ("b", "And the same sensitive detail can leak into the wrong audience's document — eroding trust, or worse."),
            ("gap", ""),
            ("h", "The cost"),
            ("b", "Support depends on the **memory of whoever is in the room** — not on a shared, versioned record of what actually works for this child."),
            ("note", "Demo data in this deck is fictional (Marco L., 14). No real child's information is shown anywhere."),
        ],
    )
    d.slide(
        "SOLUTION",
        "The passport: one curated record, four coordinated views.",
        [
            ("b", "**CaseCraft** keeps a single **autism passport** per student — what supports them, their communication profile, triggers & sensory needs — curated by a human social worker, **versioned** (v1.0 → v1.1 → v1.2)."),
            ("b", "Every session adds a **passport delta**; every delivery renders four **audience-specific views** from the same source of truth:"),
            ("b", "**Parent report** — plain language · **Teacher guide** — classroom strategies · **Social story** — first person, for the student · **Therapist summary** — session evidence."),
            ("gap", ""),
            ("h", "Observables, not verdicts"),
            ("b", "The machine extracts **what was observed** (\"covered ears ×3 when the mixer started\") and the **therapist interprets** (\"builds tolerance with ear defenders\"). No automated diagnosis, no microexpression-to-emotion claims."),
        ],
    )
    d.slide(
        "AGENT LOOP",
        "Plan · Execute · Review · Deliver — one run, audited.",
        [
            ("b", "A WorkBuddy agent runs the **session skill** end to end from a capture package (transcript + observables):"),
            ("b", "**1 · Draft** — session summary with timestamps, counts, quotes, open questions for the worker."),
            ("b", "**2 · Two-pass linter** — blocked-token scan + cross-audience parity (teacher & parent must say the same thing, never verbatim-identical script)."),
            ("b", "**3 · Review gate** — nothing merges without the social worker's sign-off (ADR-0004)."),
            ("b", "**4 · Passport delta** — v1.0 → v1.1 — then regenerate all four views + the linter report."),
            ("gap", ""),
            ("h", "Human stays in the loop"),
            ("b", "The gate is **APPROVED with one edit** in the verified run — the machine proposes, the professional disposes."),
        ],
    )
    d.slide(
        "LEVEL-2 VERIFIED",
        "Imported into the real WorkBuddy app — and it ran.",
        [
            ("b", "Both skills were **imported into WorkBuddy v4.10.4** (logged in as enochfyw@gmail.com) via their native skill store."),
            ("b", "**casecraft** — \"Generate coordinated, audited support packs…\" · **session** — \"Turn session capture packages into approved summaries and passport deltas.\""),
            ("b", "Install count went **8 → 10**; the skill descriptions shown in-app come straight from the YAML frontmatter."),
            ("b", "A task invoking the session skill for Marco's bakery session was created in the app and **ran to completion on 2026-08-12**."),
            ("b", "The full artifact chain landed in the student's session folder (next slide)."),
        ],
        image=r"C:\Users\admin\casecraft-media\skills-installed.png",
        img_w=118, img_h=70,
        img_cap="WorkBuddy app — Skills tab, INSTALLED: 10 (casecraft, session highlighted). Captured 2026-08-12.",
    )
    d.slide(
        "ARTIFACT CHAIN",
        "What the agent produced — every file verified.",
        [
            ("h", "students/marco/sessions/2026-08-08-bakery/"),
            ("b", "**01-session-draft.md** — observed events w/ timestamps, counts, quotes, open questions."),
            ("b", "**02-review-gate.md** — Decision: **APPROVED with one edit** (K. Wong, School Social Worker)."),
            ("b", "**03-passport-v1.1.md** — passport delta (1.0 → 1.1, Last updated 2026-08-12)."),
            ("b", "**05-linter-report.md** — **6/6 checks PASS**; leak drill **BLOCKED (FAIL)** as designed."),
            ("b", "**summary.json** — outcome MET · checks 6/6 · drill BLOCKED."),
            ("b", "**views/** — parent guide, teacher guide, social story, therapist summary + linter report, rendered to PDF (34–43 KB each)."),
            ("gap", ""),
            ("note", "Draft content is agent-written (LLM variance); the linter + gate + engine make the output auditable regardless of that variance."),
        ],
    )
    d.slide(
        "THE MOAT",
        "Deterministic quality gates against LLM variance.",
        [
            ("b", "A pure-LLM pipeline drifts. CaseCraft's linter is **code, not vibes** — it runs the same checks every time."),
            ("b", "**Blocked-token scan** — clinical vocabulary (\"assessment\", \"clinical\", \"goals file\") is caught in every audience view."),
            ("b", "**Verbatim-script parity** — teacher and parent guides must reference the same script but never share verbatim sentences."),
            ("b", "**Freshness** — passport sections untouched >30 days are flagged for review."),
            ("gap", ""),
            ("h", "The leak drill"),
            ("b", "A deliberately faulty parent draft was fed to the gate: **FAIL — delivery blocked** (tokens: assessment, clinical, goal progress, goals file). One blocked token blocks the whole pack until a human fixes it."),
            ("b", "Then the pack was regenerated cleanly: **all views PASS** (see the 6/6 table)."),
        ],
    )
    d.slide(
        "WORKBUDDY USAGE",
        "Native skills, automation, and per-person delivery.",
        [
            ("b", "**skill.yml manifests** — each skill ships with the WorkBuddy-native metadata file (name, description, allowed-tools, config) plus SKILL.md — uploadable as a folder or .zip."),
            ("b", "**allowed-tools: Read, Write, Bash** — the agent reads the session folder, writes the artifacts, and runs the engine scripts."),
            ("b", "**Automation tasks** — a daily task checks each student's **next-session marker**; the day before a session it collects parent/teacher replies and drafts the pre-session brief (T-1 feedback loop)."),
            ("b", "**Per-person delivery** — each stakeholder receives only their view via their own messenger DM (Slack per-user DM = the per-login document, read-only by construction; replies feed the next hypothesis)."),
        ],
    )
    d.slide(
        "HONEST LIMITS",
        "Secure by design — disclosed, not hidden.",
        [
            ("b", "**Local transcription** — audio is transcribed on-device (Whisper); the audio file never leaves the machine."),
            ("b", "**Remote summarisation, disclosed** — WorkBuddy sends content to third-party LLMs (retention up to 14 days; Singapore/PRC transfer). We say **\"secure by design\"** — human-in-the-loop review + pseudonymised data + local transcription — never \"everything stays local\"."),
            ("b", "**Observables only** — no microexpression→emotion claims; the machine reports events, the therapist interprets."),
            ("b", "**Fictional demo data** — Marco L. and Priya are fixtures; no real child's audio or identity is used."),
            ("gap", ""),
            ("h", "Not in scope (stated, not hidden)"),
            ("b", "No hosted web app or logins — delivery is per-role files + messenger DMs. No automated diagnosis — the passport is a support record, not a clinical document."),
        ],
    )
    d.slide(
        "NEXT",
        "From verified loop to pilot.",
        [
            ("b", "**Capture** — phone/tablet recording on the worker's device (the stop button lives there); whisper transcribes, the skill ingests."),
            ("b", "**Observables** — MediaPipe landmarks → posture/gaze events in the capture package."),
            ("b", "**Delivery** — Slack per-user DMs live; Automation feedback loop wired to next-session markers."),
            ("b", "**Pilot** — one partner school, 3–5 students, 4 weeks: measure report turnaround (days → hours) and cross-audience consistency."),
            ("gap", ""),
            ("h", "Today, verified"),
            ("b", "Level-1 engine (deterministic dry-run, 6/6 checks) **and** Level-2 in-app run — both green on 2026-08-12. Skills are uploadable to the portal as-is (folder or .zip with SKILL.md + YAML)."),
            ("note", "Team CaseCraft · enochfyw@gmail.com · github.com/G-626/work_buddy_collab"),
        ],
    )
    d.output(r"C:\Users\admin\hackathon_submit\casecraft-deck.pdf")
    print("deck written")

if __name__ == "__main__":
    main()
