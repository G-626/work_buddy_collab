#!/usr/bin/env python3
"""
CaseCraft styled PDF renderer (Level-1, fpdf2).

Renders the pack's `.md` views into professional-looking PDFs with visual
hierarchy: header band, colour-coded status badges, accent-bar section
headings, callout boxes for shared scripts, zebra tables, and a footer with
page numbers + "Draft for professional review" watermark note.

Markdown handled: `# title`, `## section`, `| table |`, `> callout`,
`- bullets`, `**label:** paragraphs`, `*italics*`, plain paragraphs.

Usage:
    from pdfrender import render_markdown_to_pdf
    render_markdown_to_pdf("view.md", "out.pdf",
                           doc_type="Parent Report", student="Marco L.",
                           date_s="2025-08-19")
"""

from __future__ import annotations

import re
from pathlib import Path

# ------------------------------------------------------------------ palette
INK = (30, 42, 56)          # near-black body text
MUTED = (110, 120, 130)     # secondary text
PRIMARY = (31, 78, 121)     # deep blue — headers, bands
ACCENT = (208, 121, 36)     # amber — focus callouts
LIGHT_BAND = (230, 240, 248)   # page-1 header band fill
LIGHT_ROW = (245, 248, 251)    # zebra row fill
OK_GREEN = (22, 128, 72)
OK_GREEN_BG = (226, 242, 232)
BLUE = (25, 110, 170)
BLUE_BG = (227, 240, 250)
WARN = (176, 108, 24)
WARN_BG = (252, 243, 224)
BAD_RED = (168, 44, 44)
BAD_RED_BG = (252, 230, 230)

FONT_CANDIDATES = [
    ("C:/Windows/Fonts/calibri.ttf", "C:/Windows/Fonts/calibrib.ttf"),
    ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf"),
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
]
CJK_CANDIDATES = ["C:/Windows/Fonts/msyh.ttc",
                  "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]

STATUS_COLORS = {
    "met": (OK_GREEN, OK_GREEN_BG),
    "progressing": (BLUE, BLUE_BG),
    "needs attention": (WARN, WARN_BG),
    "needs attention / review": (WARN, WARN_BG),
    "pass": (OK_GREEN, OK_GREEN_BG),
    "fixed": (BLUE, BLUE_BG),
    "flag": (WARN, WARN_BG),
    "fail": (BAD_RED, BAD_RED_BG),
    "blocked": (BAD_RED, BAD_RED_BG),
}


def _status_style(text: str) -> tuple | None:
    t = text.strip().lower()
    for key in STATUS_COLORS:
        if t == key or t.startswith(key):
            return STATUS_COLORS[key]
    return None


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

    # ------------------------------------------------------------- header
    def _add_header_band(self):
        self.pdf.add_page()
        # band
        self._fill(PRIMARY)
        self.pdf.rect(0, 0, 210, 26, style="F")
        self.pdf.set_xy(14, 7)
        self.pdf.set_font("Body", "B", 15)
        self._color((255, 255, 255))
        self.pdf.cell(0, 8, self.doc_type, new_x="LMARGIN", new_y="NEXT")
        self.pdf.set_xy(14, 15.5)
        self.pdf.set_font("Body", "", 10)
        self._color((205, 222, 240))
        who = f"{self.student}  ·  {self.date_s}"
        self.pdf.cell(0, 5, who, new_x="LMARGIN", new_y="NEXT")
        self.pdf.set_y(30)

    # ------------------------------------------------------------- blocks
    def title(self, md: str):
        # The header band already carries doc type + student + date — the
        # markdown H1 is rendered as a muted subtitle to avoid duplication.
        self._write(_strip_inline(md), size=13, style="B", color=PRIMARY, lh=6)
        self._space(2.5)

    def section(self, md: str):
        txt = _strip_inline(md)
        # accent bar
        y = self.pdf.get_y()
        self._fill(ACCENT)
        self.pdf.rect(10, y + 0.6, 1.6, 6.4, style="F")
        self.pdf.set_x(14)
        self._write(txt, size=12, style="B", color=PRIMARY, lh=6.2)
        self._space(1.6)

    def callout(self, lines: list[str]):
        """Render a `>` blockquote as a tinted callout box."""
        body = " ".join(_strip_inline(l.lstrip(">")).strip() for l in lines)
        if not body:
            return
        self._space(0.5)
        x0, w = 12, 186
        # measure height
        self.pdf.set_font("Body", "", 10.5)
        lines_est = max(1, int(self.pdf.get_string_width(body) / (w - 18)) + 1)
        h = lines_est * 5.0 + 7
        y0 = self.pdf.get_y()
        if y0 + h > 275:
            self.pdf.add_page()
            y0 = self.pdf.get_y()
        self._fill(LIGHT_BAND)
        self._draw(ACCENT)
        self.pdf.rect(x0, y0, w, h, style="DF")
        self.pdf.set_xy(x0 + 7, y0 + 3.5)
        self.pdf.set_font("Body", "B", 9.5)
        self._color(ACCENT)
        self.pdf.cell(0, 4.6, "SAME WORDS — SAY IT EXACTLY", new_x="LMARGIN", new_y="NEXT")
        self.pdf.set_xy(x0 + 7, y0 + 8.6)
        self.pdf.set_font("Body", "", 10.5)
        self._color(INK)
        self.pdf.multi_cell(w - 14, 5.0, body, new_x="LMARGIN", new_y="NEXT")
        self.pdf.set_y(y0 + h + 2)

    def table(self, rows: list[list[str]]):
        """Render a markdown table with header + zebra + status colours.

        Cells use multi_cell so text wraps; row height is computed from the
        tallest wrapped cell. Status cells (Met/Progressing/Needs attention/
        PASS/FAIL) get a coloured fill + bold centred text.
        """
        rows = [[_strip_inline(c).strip() for c in r] for r in rows]
        if not rows:
            return
        # drop markdown separator row (|---|---|)
        rows = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c) for c in r)]
        header, data = rows[0], rows[1:]
        ncols = len(header)
        if ncols == 0:
            return
        page_w, margin = 210, 10
        usable = page_w - 2 * margin
        # Weight columns: give the middle (evidence) column more room.
        if ncols == 3:
            widths = [usable * 0.32, usable * 0.40, usable * 0.28]
        elif ncols == 4:
            widths = [usable * 0.30, usable * 0.36, usable * 0.18, usable * 0.16]
        else:
            widths = [usable / ncols] * ncols
        pad, line_h, fs = 2.2, 4.4, 9.5

        def wrap_count(text: str, w: float, style: str = "") -> int:
            """Approximate wrapped line count for text in a cell of width w."""
            self.pdf.set_font("Body", style, fs)
            avail = max(w - 2 * pad - 2, 8)
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

        def cell_height(row: list[str], style_row: bool = False) -> float:
            h = 0.0
            for ci, cval in enumerate(row):
                st = "B" if (style_row and _status_style(cval)) else ""
                n = wrap_count(cval, widths[ci], st)
                h = max(h, n * line_h + 2 * pad)
            return max(h, 7.0)

        def draw_row(row: list[str], y: float, h: float, is_header: bool,
                     is_status_row: bool):
            x = margin
            for ci, cval in enumerate(row):
                style = _status_style(cval)
                if is_header:
                    fill, txt_color, fstyle = PRIMARY, (255, 255, 255), "B"
                elif style:
                    fill, txt_color, fstyle = style[1], style[0], "B"
                else:
                    fill = LIGHT_ROW if (is_status_row and is_status_row) else (255, 255, 255)
                    txt_color, fstyle = INK, ""
                self._fill(fill)
                self.pdf.rect(x, y, widths[ci], h, style="F")
                self.pdf.set_font("Body", fstyle, fs)
                self._color(txt_color)
                align = "C" if (is_header or style) else "L"
                self.pdf.set_xy(x + pad, y + pad - 0.4)
                self.pdf.multi_cell(widths[ci] - 2 * pad, line_h, cval, align=align,
                                    new_x="LMARGIN", new_y="NEXT")
                x += widths[ci]

        self._space(0.5)
        # header
        y = self.pdf.get_y()
        h = cell_height(header, style_row=False)
        if y + h > 275:
            self.pdf.add_page()
            y = self.pdf.get_y()
        draw_row(header, y, h, is_header=True, is_status_row=False)
        self.pdf.set_y(y + h)
        # data rows
        for ri, row in enumerate(data):
            y = self.pdf.get_y()
            h = cell_height(row, style_row=True)
            if y + h > 275:
                self.pdf.add_page()
                y = self.pdf.get_y()
            draw_row(row, y, h, is_header=False, is_status_row=(ri % 2 == 1))
            self.pdf.set_y(y + h)
        self._space(2)

    def bullets(self, items: list[str], numbered: bool = False):
        for i, item in enumerate(items):
            marker = f"{i+1}. " if numbered else "•  "
            txt = _strip_inline(item)
            self.pdf.set_font("Body", "", 10.5)
            self._color(ACCENT if not numbered else PRIMARY)
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
    # Best-effort CJK fallback — only load when content actually has 中文,
    # so English-only packs don't trigger the TTC subsetter noise.
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

        # table rows
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
        # callout
        if ln.startswith(">"):
            if not in_callout:
                flush_list()
                in_callout = True
                callout_lines = []
            callout_lines.append(ln)
            continue
        if in_callout:
            flush_callout()
        # list
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
        # headings
        if ln.startswith("# "):
            sp.title(ln[2:])
            continue
        if ln.startswith("## "):
            sp.section(ln[3:])
            continue
        if ln == "":
            continue
        # paragraph
        sp.para(ln)

    flush_table(); flush_callout(); flush_list()
    sp.footer()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sp.pdf.output(str(out_path))
    return out_path
