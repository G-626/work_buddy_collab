#!/usr/bin/env python3
"""
CaseCraft styled PDF renderer (Level-1, fpdf2).

Design rules (v2):
- ONE accent colour (deep blue). Hierarchy is carried by font weight/size
  (band title > H1 > section H2 > body > muted notes), not by colour.
- Every text frame uses MIRRORED padding: text is vertically centred inside
  its cell/box, so top padding == bottom padding (nothing clashes with the
  next cell).
- Status values (Met / Progressing / Needs attention / PASS / FAIL) are
  emphasised with bold + the accent colour — never a status colour.
- Dated by the SYSTEM date supplied by the caller (never assumed inside).

Markdown handled: `# title`, `## section`, `| table |`, `> callout`,
`- bullets`, `**label:** paragraphs`, `*italics*`, plain paragraphs.

Usage:
    from pdfrender import render_markdown_to_pdf
    render_markdown_to_pdf("view.md", "out.pdf",
                           doc_type="Parent Report", student="Marco L.",
                           date_s="2026-08-10")
"""

from __future__ import annotations

import re
from pathlib import Path

# ------------------------------------------------------------------ palette
# Single accent colour; everything else is ink/gray/white.
PRIMARY = (31, 78, 121)      # the ONE accent — bands, bars, header rows, status text
INK = (35, 42, 50)           # body text (near-black)
MUTED = (125, 133, 140)      # secondary text (notes, footer)
WHITE = (255, 255, 255)
BAND_SUB = (200, 216, 232)   # light blue-grey text on the primary band (still the accent family)

FONT_CANDIDATES = [
    ("C:/Windows/Fonts/calibri.ttf", "C:/Windows/Fonts/calibrib.ttf"),
    ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf"),
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
]
CJK_CANDIDATES = ["C:/Windows/Fonts/msyh.ttc",
                  "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]

# Status words emphasised with bold + accent (no status colours).
STATUS_WORDS = ["met", "progressing", "needs attention", "pass", "fixed",
                "flag", "fail", "blocked"]


def _is_status(text: str) -> bool:
    t = text.strip().lower()
    return any(t == s or t.startswith(s) for s in STATUS_WORDS)


def _strip_inline(md: str) -> str:
    """Strip **bold**, *italic*, `code` markers — keep the text."""
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", md)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    return s


class StyledPDF:
    def __init__(self, doc_type: str, student: str, date_s: str,
                 situation: str = ""):
        from fpdf import FPDF

        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.set_auto_page_break(auto=True, margin=18)
        self.doc_type = doc_type
        self.student = student
        self.date_s = date_s
        self.situation = situation
        self._font_ok = self._load_fonts()
        self._add_header_band()

    # ------------------------------------------------------------- fonts
    def _load_fonts(self) -> bool:
        for cand, cand_b in FONT_CANDIDATES:
            if Path(cand).is_file():
                try:
                    self.pdf.add_font("Body", "", cand)
                    if Path(cand_b).is_file():
                        self.pdf.add_font("Body", "B", cand_b)
                    self.pdf.set_font("Body", "", 10.5)
                    return True
                except Exception:
                    continue
        return False

    def _cjk(self) -> bool:
        """Add a CJK fallback font so 中文 renders (HK bilingual reports)."""
        for cand in CJK_CANDIDATES:
            if Path(cand).is_file():
                try:
                    self.pdf.add_font("CJK", "", cand)
                    return True
                except Exception:
                    continue
        return False

    # ------------------------------------------------------------- helpers
    def _color(self, rgb): self.pdf.set_text_color(*rgb)
    def _fill(self, rgb): self.pdf.set_fill_color(*rgb)
    def _draw(self, rgb): self.pdf.set_draw_color(*rgb)

    def _write(self, text: str, size: float = 10.5, style: str = "",
               color=INK, lh: float = 5.2):
        self.pdf.set_font("Body", style, size)
        self._color(color)
        self.pdf.multi_cell(0, lh, text, new_x="LMARGIN", new_y="NEXT")

    def _space(self, h: float = 2.5):
        self.pdf.ln(h)

    def _wrap_lines(self, text: str, avail: float, style: str = "",
                    fs: float = 10.5) -> int:
        """Exact wrapped-line count for text within avail width."""
        self.pdf.set_font("Body", style, fs)
        words = text.split()
        if not words:
            return 1
        lines, cur = 1, words[0]
        for word in words[1:]:
            trial = f"{cur} {word}"
            if self.pdf.get_string_width(trial) <= avail:
                cur = trial
            else:
                lines += 1
                cur = word
        return lines

    # ------------------------------------------------------------- header
    def _add_header_band(self):
        self.pdf.add_page()
        self._fill(PRIMARY)
        self.pdf.rect(0, 0, 210, 26, style="F")
        self.pdf.set_xy(14, 7)
        self.pdf.set_font("Body", "B", 15)
        self._color(WHITE)
        self.pdf.cell(0, 8, self.doc_type, new_x="LMARGIN", new_y="NEXT")
        self.pdf.set_xy(14, 15.5)
        self.pdf.set_font("Body", "", 10)
        self._color(BAND_SUB)
        self.pdf.cell(0, 5, f"{self.student}  ·  {self.date_s}",
                      new_x="LMARGIN", new_y="NEXT")
        self.pdf.set_y(30)

    # ------------------------------------------------------------- blocks
    def title(self, md: str):
        self._write(_strip_inline(md), size=13, style="B", color=PRIMARY, lh=6)
        self._space(2.5)

    def section(self, md: str):
        txt = _strip_inline(md)
        y = self.pdf.get_y()
        self._fill(PRIMARY)
        self.pdf.rect(10, y + 0.6, 1.6, 6.4, style="F")
        self.pdf.set_x(14)
        self._write(txt, size=12, style="B", color=PRIMARY, lh=6.2)
        self._space(1.6)

    def callout(self, lines: list[str]):
        """`>` blockquote as a single-accent callout box (mirrored padding)."""
        body = " ".join(_strip_inline(l.lstrip(">")).strip() for l in lines)
        if not body:
            return
        x0, w = 12, 186
        inner = w - 14
        label_h = 4.6
        pad_top = 3.5
        gap = 0.8
        pad_bottom = 3.5
        body_lh = 5.0
        n = self._wrap_lines(body, inner, fs=10.5)
        body_h = n * body_lh
        h = pad_top + label_h + gap + body_h + pad_bottom
        y0 = self.pdf.get_y()
        if y0 + h > 275:
            self.pdf.add_page()
            y0 = self.pdf.get_y()
        self._fill(WHITE)
        self._draw(PRIMARY)
        self.pdf.rect(x0, y0, w, h, style="DF")
        # label (top, mirrored by bottom pad)
        self.pdf.set_xy(x0 + 7, y0 + pad_top)
        self.pdf.set_font("Body", "B", 9.5)
        self._color(PRIMARY)
        self.pdf.cell(0, label_h, "SAME WORDS — SAY IT EXACTLY",
                      new_x="LMARGIN", new_y="NEXT")
        # body
        self.pdf.set_xy(x0 + 7, y0 + pad_top + label_h + gap)
        self.pdf.set_font("Body", "", 10.5)
        self._color(INK)
        self.pdf.multi_cell(inner, body_lh, body, new_x="LMARGIN", new_y="NEXT")
        self.pdf.set_y(y0 + h + 2)

    def table(self, rows: list[list[str]]):
        """Markdown table — header row in accent, body wrapped with mirrored
        vertical padding, status emphasised via bold + accent text."""
        rows = [[_strip_inline(c).strip() for c in r] for r in rows]
        if not rows:
            return
        rows = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c) for c in r)]
        header, data = rows[0], rows[1:]
        ncols = len(header)
        if ncols == 0:
            return
        page_w, margin = 210, 10
        usable = page_w - 2 * margin
        if ncols == 3:
            widths = [usable * 0.32, usable * 0.40, usable * 0.28]
        elif ncols == 4:
            widths = [usable * 0.30, usable * 0.36, usable * 0.18, usable * 0.16]
        else:
            widths = [usable / ncols] * ncols
        pad, line_h, fs = 2.6, 4.4, 9.5

        def cell_lines(text: str, w: float, bold: bool = False) -> int:
            return self._wrap_lines(text, w - 2 * pad - 2, "B" if bold else "", fs)

        def cell_height(row: list[str], bold: bool = False) -> float:
            h = 0.0
            for ci, cval in enumerate(row):
                n = cell_lines(cval, widths[ci], bold or _is_status(cval))
                h = max(h, n * line_h + 2 * pad)  # mirrored pad top+bottom
            return h

        def draw_row(row: list[str], y: float, h: float, is_header: bool):
            x = margin
            for ci, cval in enumerate(row):
                if is_header:
                    fill, txt_color, fstyle = PRIMARY, WHITE, "B"
                    align = "C"
                else:
                    fill, txt_color = WHITE, INK
                    fstyle = "B" if _is_status(cval) else ""
                    txt_color = PRIMARY if _is_status(cval) else INK
                    align = "C" if _is_status(cval) else "L"
                self._fill(fill)
                self.pdf.rect(x, y, widths[ci], h, style="F")
                n = cell_lines(cval, widths[ci], fstyle == "B")
                # mirrored vertical centering
                y_text = y + (h - n * line_h) / 2
                self.pdf.set_font("Body", fstyle, fs)
                self._color(txt_color)
                self.pdf.set_xy(x + pad, y_text)
                self.pdf.multi_cell(widths[ci] - 2 * pad, line_h, cval,
                                    align=align, new_x="LMARGIN", new_y="NEXT")
                x += widths[ci]

        self._space(0.5)
        y = self.pdf.get_y()
        h = cell_height(header, bold=True)
        if y + h > 275:
            self.pdf.add_page()
            y = self.pdf.get_y()
        draw_row(header, y, h, is_header=True)
        self.pdf.set_y(y + h)
        for row in data:
            y = self.pdf.get_y()
            h = cell_height(row)
            if y + h > 275:
                self.pdf.add_page()
                y = self.pdf.get_y()
            draw_row(row, y, h, is_header=False)
            self.pdf.set_y(y + h)
        self._space(2)

    def bullets(self, items: list[str], numbered: bool = False):
        for i, item in enumerate(items):
            marker = f"{i+1}. " if numbered else "•  "
            txt = _strip_inline(item)
            self.pdf.set_font("Body", "", 10.5)
            self._color(PRIMARY)
            self.pdf.set_x(13)
            self.pdf.cell(7, 4.8, marker, new_x="END")
            self.pdf.set_x(20)
            self._color(INK)
            self.pdf.multi_cell(180, 4.8, txt, new_x="LMARGIN", new_y="NEXT")
            self._space(0.4)

    def para(self, md: str, small: bool = False):
        txt = _strip_inline(md)
        if not txt:
            return
        is_note = txt.startswith("*") and txt.endswith("*")
        if is_note:
            self._write(txt.strip("*").strip(), size=9, color=MUTED, lh=4.4)
            self._space(1.5)
            return
        if txt.startswith("**") and "**" in txt[2:]:
            label, _, rest = txt[2:].partition("**")
            self.pdf.set_font("Body", "B", 10.5)
            self._color(PRIMARY)
            self.pdf.set_x(13)
            self.pdf.cell(0, 5, label, new_x="LMARGIN", new_y="NEXT")
            self.pdf.set_font("Body", "", 10.5)
            self._color(INK)
            if rest.strip():
                self.pdf.set_x(13)
                self.pdf.multi_cell(0, 5, rest.strip(), new_x="LMARGIN", new_y="NEXT")
            self._space(1.2)
            return
        self._write(txt, size=10.5, color=INK, lh=5)

    def footer(self):
        """Draw the footer on every page (content may span multiple pages)."""
        total = self.pdf.page_no()
        self.pdf.set_auto_page_break(auto=False)
        for page_no in range(1, total + 1):
            self.pdf.page = page_no
            self.pdf.set_y(-16)
            self.pdf.set_font("Body", "", 8)
            self._color(MUTED)
            self.pdf.cell(0, 4,
                          "CaseCraft · Draft for professional review — please edit and sign before use",
                          align="C")
            self.pdf.set_y(-11)
            self.pdf.cell(0, 4, f"Page {page_no} of {total}", align="C")
        self.pdf.page = total
        self.pdf.set_auto_page_break(auto=True, margin=18)
        self.pdf.set_y(30)


def render_markdown_to_pdf(md_path: Path, out_path: Path, doc_type: str,
                           student: str, date_s: str, situation: str = "") -> Path | None:
    """Render one markdown view to a styled PDF. Returns out_path or None."""
    try:
        from fpdf import FPDF  # noqa: F401 — ensure importable
    except ImportError:
        return None
    if not Path(md_path).is_file():
        return None

    sp = StyledPDF(doc_type, student, date_s, situation)
    if not sp._font_ok:
        return None
    if re.search(r"[\u4e00-\u9fff]", Path(md_path).read_text(encoding="utf-8")):
        sp._cjk()

    lines = Path(md_path).read_text(encoding="utf-8").splitlines()
    i, n = 0, len(lines)
    in_table = False
    table_rows: list[list[str]] = []
    in_callout = False
    callout_lines: list[str] = []
    in_list = False
    list_items: list[str] = []
    numbered = False

    def flush_table():
        nonlocal in_table, table_rows
        if table_rows:
            sp.table(table_rows)
        in_table, table_rows = False, []

    def flush_callout():
        nonlocal in_callout, callout_lines
        if callout_lines:
            sp.callout(callout_lines)
        in_callout, callout_lines = False, []

    def flush_list():
        nonlocal in_list, list_items
        if list_items:
            sp.bullets(list_items, numbered=numbered)
        in_list, list_items = False, []

    while i < n:
        raw = lines[i]
        ln = raw.strip()
        i += 1

        if ln.startswith("|") and ln.endswith("|"):
            if not in_table:
                flush_callout(); flush_list()
                in_table = True
                table_rows = []
            cells = [c for c in ln.strip("|").split("|")]
            table_rows.append(cells)
            continue
        if in_table:
            flush_table()
        if ln.startswith(">"):
            if not in_callout:
                flush_list()
                in_callout = True
                callout_lines = []
            callout_lines.append(ln)
            continue
        if in_callout:
            flush_callout()
        m = re.match(r"^(?:(\d+)\.|[-•])\s+(.*)$", ln)
        if m:
            if not in_list:
                in_list = True
                list_items = []
                numbered = bool(m.group(1))
            list_items.append(m.group(2))
            continue
        if in_list:
            flush_list()
        if ln.startswith("# "):
            sp.title(ln[2:])
            continue
        if ln.startswith("## "):
            sp.section(ln[3:])
            continue
        if ln == "":
            continue
        sp.para(ln)

    flush_table(); flush_callout(); flush_list()
    sp.footer()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sp.pdf.output(str(out_path))
    return out_path
