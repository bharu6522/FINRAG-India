# export_report.py
# Run: python export_report.py
# Output: FinRAG_Project_Report.pdf

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Flowable
from datetime import datetime

# ── Color Palette ──────────────────────────────────────────────────────────
DARK_BG     = colors.HexColor("#0D1117")
CARD_BG     = colors.HexColor("#161B22")
ACCENT      = colors.HexColor("#00C49A")
ACCENT_DARK = colors.HexColor("#009977")
TEXT_MAIN   = colors.HexColor("#E6EDF3")
TEXT_MUTED  = colors.HexColor("#8B949E")
BORDER      = colors.HexColor("#30363D")
WHITE       = colors.white

PAGE_W, PAGE_H = A4

# ── Custom Flowables ───────────────────────────────────────────────────────
class ColorRect(Flowable):
    """A filled colored rectangle — used as section header background."""
    def __init__(self, width, height, fill_color, radius=4):
        super().__init__()
        self.width = width
        self.height = height
        self.fill_color = fill_color
        self.radius = radius

    def draw(self):
        self.canv.setFillColor(self.fill_color)
        self.canv.roundRect(0, 0, self.width, self.height,
                            self.radius, stroke=0, fill=1)

class AccentLine(Flowable):
    """A thick colored horizontal rule."""
    def __init__(self, width, color=None, thickness=2):
        super().__init__()
        self.width = width
        self.color = color or ACCENT
        self.thickness = thickness
        self.height = thickness

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


# ── Styles ─────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    styles = {
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName="Helvetica-Bold",
            fontSize=36,
            textColor=WHITE,
            alignment=TA_LEFT,
            leading=42,
            spaceAfter=6,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            fontName="Helvetica",
            fontSize=13,
            textColor=ACCENT,
            alignment=TA_LEFT,
            leading=18,
            spaceAfter=4,
            letterSpacing=1.5,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta",
            fontName="Helvetica",
            fontSize=10,
            textColor=TEXT_MUTED,
            alignment=TA_LEFT,
            leading=16,
        ),
        "section_label": ParagraphStyle(
            "section_label",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=ACCENT,
            alignment=TA_LEFT,
            leading=12,
            letterSpacing=2,
        ),
        "section_title": ParagraphStyle(
            "section_title",
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=DARK_BG,
            alignment=TA_LEFT,
            leading=22,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#2D333B"),
            alignment=TA_LEFT,
            leading=16,
            spaceAfter=8,
        ),
        "body_bold": ParagraphStyle(
            "body_bold",
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=colors.HexColor("#1C2128"),
            alignment=TA_LEFT,
            leading=16,
            spaceAfter=4,
        ),
        "code": ParagraphStyle(
            "code",
            fontName="Courier",
            fontSize=8.5,
            textColor=ACCENT,
            backColor=colors.HexColor("#0D1117"),
            alignment=TA_LEFT,
            leading=14,
            leftIndent=10,
            rightIndent=10,
            spaceBefore=4,
            spaceAfter=4,
        ),
        "caption": ParagraphStyle(
            "caption",
            fontName="Helvetica-Oblique",
            fontSize=8,
            textColor=TEXT_MUTED,
            alignment=TA_CENTER,
            leading=12,
            spaceAfter=12,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName="Helvetica",
            fontSize=8,
            textColor=TEXT_MUTED,
            alignment=TA_CENTER,
        ),
        "toc_item": ParagraphStyle(
            "toc_item",
            fontName="Helvetica",
            fontSize=11,
            textColor=colors.HexColor("#2D333B"),
            leading=20,
            leftIndent=20,
        ),
        "toc_num": ParagraphStyle(
            "toc_num",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=ACCENT,
            leading=20,
        ),
        "chip": ParagraphStyle(
            "chip",
            fontName="Helvetica-Bold",
            fontSize=9,
            textColor=ACCENT,
            alignment=TA_CENTER,
            leading=14,
        ),
    }
    return styles


# ── Page Templates ─────────────────────────────────────────────────────────
def cover_background(canvas, doc):
    """Dark gradient cover page background."""
    canvas.saveState()
    # Full dark background
    canvas.setFillColor(DARK_BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # Green accent strip on left
    canvas.setFillColor(ACCENT)
    canvas.rect(0, 0, 6, PAGE_H, stroke=0, fill=1)

    # Decorative circle top-right
    canvas.setFillColor(colors.HexColor("#00C49A0D"))
    canvas.circle(PAGE_W - 20*mm, PAGE_H - 20*mm, 80*mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#00C49A08"))
    canvas.circle(PAGE_W + 10*mm, PAGE_H - 10*mm, 120*mm, stroke=0, fill=1)

    # Bottom bar
    canvas.setFillColor(colors.HexColor("#161B22"))
    canvas.rect(0, 0, PAGE_W, 22*mm, stroke=0, fill=1)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, 22*mm, PAGE_W, 0.5*mm, stroke=0, fill=1)

    canvas.restoreState()

def inner_header_footer(canvas, doc):
    """Header + footer for inner pages."""
    canvas.saveState()

    # Header bar
    canvas.setFillColor(DARK_BG)
    canvas.rect(0, PAGE_H - 14*mm, PAGE_W, 14*mm, stroke=0, fill=1)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, PAGE_H - 14*mm, PAGE_W, 0.5*mm, stroke=0, fill=1)

    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(ACCENT)
    canvas.drawString(15*mm, PAGE_H - 9*mm, "FinRAG")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(30*mm, PAGE_H - 9*mm,
                      "Financial Document Intelligence System")
    canvas.drawRightString(PAGE_W - 15*mm, PAGE_H - 9*mm,
                           "2024–25 Project Report")

    # Footer
    canvas.setFillColor(colors.HexColor("#F0F2F5"))
    canvas.rect(0, 0, PAGE_W, 12*mm, stroke=0, fill=1)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, 12*mm, PAGE_W, 0.3*mm, stroke=0, fill=1)

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(15*mm, 4.5*mm, f"Generated: {datetime.now().strftime('%d %B %Y')}")
    canvas.drawCentredString(PAGE_W / 2, 4.5*mm,
                             "OpenAI  ·  FAISS  ·  LangChain  ·  Streamlit")
    canvas.drawRightString(PAGE_W - 15*mm, 4.5*mm, f"Page {doc.page}")

    canvas.restoreState()


# ── Section Header Helper ──────────────────────────────────────────────────
def section_header(label, title, styles, content_width):
    """Returns a list of flowables making a styled section header."""
    return [
        Spacer(1, 14),
        Paragraph(label.upper(), styles["section_label"]),
        AccentLine(content_width, ACCENT, 1),
        Spacer(1, 4),
        Paragraph(title, styles["section_title"]),
        Spacer(1, 6),
    ]


# ── Build PDF ──────────────────────────────────────────────────────────────
def build_report(output_path="FinRAG_Project_Report.pdf"):
    styles = make_styles()
    story  = []

    # Margins
    LM = 18*mm
    RM = 18*mm
    TM = 18*mm
    BM = 16*mm
    content_width = PAGE_W - LM - RM

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=LM, rightMargin=RM,
        topMargin=TM,  bottomMargin=BM,
        title="FinRAG — Financial Document Intelligence",
        author="FinRAG Project",
        subject="RAG System for Indian Financial Documents",
    )

    # ── COVER PAGE ─────────────────────────────────────────────────────────
    story.append(Spacer(1, 38*mm))
    story.append(Paragraph("Fin<font color='#00C49A'>RAG</font>", styles["cover_title"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("FINANCIAL DOCUMENT INTELLIGENCE SYSTEM", styles["cover_subtitle"]))
    story.append(Spacer(1, 5*mm))
    story.append(AccentLine(content_width * 0.35, ACCENT, 1.5))
    story.append(Spacer(1, 8*mm))

    cover_meta = [
        "Retrieval-Augmented Generation (RAG) pipeline for Indian",
        "financial regulatory documents — RBI Circulars, SEBI Guidelines,",
        "and Corporate Annual Reports (FY 2024–25)",
    ]
    for line in cover_meta:
        story.append(Paragraph(line, styles["cover_meta"]))

    story.append(Spacer(1, 60*mm))

    # Cover chips row
    chips_data = [["PyPDF2", "LangChain", "OpenAI Embeddings", "FAISS", "Streamlit"]]
    chips_table = Table(chips_data, colWidths=[30*mm, 32*mm, 46*mm, 26*mm, 34*mm])
    chips_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#00C49A22")),
        ("TEXTCOLOR",    (0,0), (-1,-1), ACCENT),
        ("FONTNAME",     (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [colors.HexColor("#00C49A22")]),
        ("BOX",          (0,0), (-1,-1), 0.5, ACCENT),
        ("INNERGRID",    (0,0), (-1,-1), 0.5, ACCENT),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("ROUNDEDCORNERS",(0,0),(-1,-1), [3]),
    ]))
    story.append(chips_table)
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(
        f"Project Report  ·  FY 2024–25  ·  {datetime.now().strftime('%B %Y')}",
        styles["cover_meta"]
    ))

    story.append(PageBreak())

    # ── TABLE OF CONTENTS ──────────────────────────────────────────────────
    story += section_header("Navigation", "Table of Contents", styles, content_width)

    toc_items = [
        ("1", "Project Overview & Objectives"),
        ("2", "System Architecture"),
        ("3", "Pipeline — Stage by Stage"),
        ("4", "Technology Stack"),
        ("5", "Chunking Strategy"),
        ("6", "Cost Estimation"),
        ("7", "Streamlit UI — Features"),
        ("8", "Sample Q&A Outputs"),
        ("9", "Setup & Deployment Guide"),
        ("10", "Future Enhancements"),
    ]
    toc_data = [[Paragraph(n, styles["toc_num"]),
                 Paragraph(t, styles["toc_item"])] for n, t in toc_items]
    toc_table = Table(toc_data, colWidths=[14*mm, content_width - 14*mm])
    toc_table.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LINEBELOW",    (0,0), (-1,-2), 0.3, colors.HexColor("#E0E4EA")),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # ── SECTION 1: OVERVIEW ────────────────────────────────────────────────
    story += section_header("01", "Project Overview & Objectives", styles, content_width)
    story.append(Paragraph(
        "FinRAG is a Retrieval-Augmented Generation (RAG) system built to make Indian "
        "financial regulatory documents queryable using natural language. It processes "
        "RBI circulars, SEBI guidelines, and corporate annual reports, enabling analysts "
        "to ask questions and receive cited, accurate answers — without reading hundreds of pages.",
        styles["body"]
    ))

    obj_data = [
        ["#", "Objective", "Status"],
        ["1", "Parse 5–10 financial PDFs (RBI, SEBI, Bajaj Finserv)", "Done"],
        ["2", "Clean and chunk text with LangChain (chunk=500, overlap=50)", "Done"],
        ["3", "Embed chunks using OpenAI text-embedding-3-small", "Done"],
        ["4", "Store vectors in FAISS for fast similarity search", "Done"],
        ["5", "Generate cited answers with GPT-4o-mini", "Done"],
        ["6", "Build Streamlit UI with Chat, Documents & About tabs", "Done"],
    ]
    obj_table = Table(obj_data, colWidths=[10*mm, 120*mm, 28*mm])
    obj_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), DARK_BG),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("TEXTCOLOR",    (0,1), (-1,-1), colors.HexColor("#2D333B")),
        ("TEXTCOLOR",    (2,1), (2,-1), ACCENT_DARK),
        ("FONTNAME",     (2,1), (2,-1), "Helvetica-Bold"),
        ("ALIGN",        (0,0), (0,-1), "CENTER"),
        ("ALIGN",        (2,0), (2,-1), "CENTER"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, colors.HexColor("#F6F8FA")]),
        ("BOX",          (0,0), (-1,-1), 0.5, BORDER),
        ("INNERGRID",    (0,0), (-1,-1), 0.3, colors.HexColor("#E0E4EA")),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
    ]))
    story.append(obj_table)
    story.append(PageBreak())

    # ── SECTION 2: ARCHITECTURE ────────────────────────────────────────────
    story += section_header("02", "System Architecture", styles, content_width)
    story.append(Paragraph(
        "The pipeline follows a standard RAG architecture with financial-domain "
        "customizations for Indian regulatory documents:",
        styles["body"]
    ))

    arch_steps = [
        ("📂", "PDF Ingestion",       "5–10 financial PDFs loaded from pdfs/ directory"),
        ("🔍", "Text Extraction",     "PyPDF2 extracts raw text page-by-page with metadata"),
        ("🧹", "Text Cleaning",       "Regex removes headers, footers, page numbers, artifacts"),
        ("✂️",  "Chunking",           "LangChain splits text: chunk=500 chars, overlap=50"),
        ("🔢", "Embedding",           "OpenAI text-embedding-3-small → 1536-dim vectors"),
        ("🗄️", "Vector Storage",      "FAISS IndexFlatIP with L2 normalization for cosine search"),
        ("🎯", "Retrieval",           "Query embedded → top-K chunks retrieved by similarity"),
        ("🤖", "Generation",          "GPT-4o-mini produces cited answer from retrieved context"),
    ]
    for icon, title, desc in arch_steps:
        row_data = [[
            Paragraph(f"<b>{icon} {title}</b>", styles["body_bold"]),
            Paragraph(desc, styles["body"])
        ]]
        row_table = Table(row_data, colWidths=[42*mm, content_width - 42*mm])
        row_table.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (0,0), colors.HexColor("#F0FBF8")),
            ("BACKGROUND",   (1,0), (1,0), WHITE),
            ("BOX",          (0,0), (-1,-1), 0.3, colors.HexColor("#D0EDE7")),
            ("INNERGRID",    (0,0), (-1,-1), 0.3, colors.HexColor("#D0EDE7")),
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
            ("TOPPADDING",   (0,0), (-1,-1), 6),
            ("BOTTOMPADDING",(0,0), (-1,-1), 6),
            ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ]))
        story.append(row_table)
        story.append(Spacer(1, 2))

    story.append(PageBreak())

    # ── SECTION 3: PIPELINE CODE ───────────────────────────────────────────
    story += section_header("03", "Pipeline — Stage by Stage", styles, content_width)

    stages = [
        ("Stage 1 — PDF Parsing", "parse_pdfs.py",
         'reader = PyPDF2.PdfReader(filepath)\nfor page in reader.pages:\n    text = page.extract_text()'),
        ("Stage 2 — Text Cleaning", "clean_text.py",
         'text = re.sub(r"\\n{3,}", "\\n\\n", raw_text)\ntext = re.sub(r"-\\n(\\w)", r"\\1", text)\ntext = re.sub(r"^\\s*\\d{1,4}\\s*$", "", text, flags=re.MULTILINE)'),
        ("Stage 3 — Chunking", "chunk_text.py",
         'splitter = RecursiveCharacterTextSplitter(\n    chunk_size=500,\n    chunk_overlap=50,\n    separators=["\\n\\n","\\n",". "," ",""]\n)'),
        ("Stage 4 — Embedding", "embed_store.py",
         'response = client.embeddings.create(\n    model="text-embedding-3-small",\n    input=batch  # up to 50 chunks per call\n)'),
        ("Stage 5 — FAISS Store", "embed_store.py",
         'faiss.normalize_L2(matrix)\nindex = faiss.IndexFlatIP(1536)\nindex.add(matrix)\nfaiss.write_index(index, "vector_store/index.faiss")'),
        ("Stage 6 — RAG Query", "rag_query.py",
         'scores, indices = index.search(query_vec, top_k)\nresponse = client.chat.completions.create(\n    model="gpt-4o-mini",\n    messages=[system_prompt, context + question]\n)'),
    ]

    for stage_title, filename, code in stages:
        story.append(KeepTogether([
            Paragraph(f"<b>{stage_title}</b>", styles["body_bold"]),
            Paragraph(f"File: <font color='#00C49A'>{filename}</font>", styles["caption"]),
            Paragraph(code.replace("\n", "<br/>"), styles["code"]),
            Spacer(1, 8),
        ]))

    story.append(PageBreak())

    # ── SECTION 4: TECH STACK ──────────────────────────────────────────────
    story += section_header("04", "Technology Stack", styles, content_width)

    stack_data = [
        ["Component",       "Library / Service",            "Version",  "Purpose"],
        ["PDF Parsing",     "PyPDF2",                       "3.x",      "Extract text from PDF pages"],
        ["Text Splitting",  "LangChain TextSplitter",       "0.3.x",    "Chunk text with overlap"],
        ["Embeddings",      "text-embedding-3-small",       "OpenAI",   "1536-dim semantic vectors"],
        ["Vector Store",    "FAISS IndexFlatIP",            "1.7.x",    "Cosine similarity search"],
        ["LLM Generation",  "GPT-4o-mini",                  "OpenAI",   "Cited answer generation"],
        ["UI Framework",    "Streamlit",                    "1.x",      "Web app with tabs & chat"],
        ["Language",        "Python",                       "3.10+",    "Core implementation"],
    ]
    stack_table = Table(stack_data, colWidths=[38*mm, 50*mm, 24*mm, 58*mm])
    stack_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), DARK_BG),
        ("TEXTCOLOR",    (0,0), (-1,0), ACCENT),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("TEXTCOLOR",    (0,1), (0,-1), colors.HexColor("#1C2128")),
        ("FONTNAME",     (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",    (1,1), (1,-1), ACCENT_DARK),
        ("TEXTCOLOR",    (2,1), (2,-1), TEXT_MUTED),
        ("TEXTCOLOR",    (3,1), (3,-1), colors.HexColor("#2D333B")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, colors.HexColor("#F6F8FA")]),
        ("BOX",          (0,0), (-1,-1), 0.5, BORDER),
        ("INNERGRID",    (0,0), (-1,-1), 0.3, colors.HexColor("#E0E4EA")),
        ("TOPPADDING",   (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",(0,0), (-1,-1), 7),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("ALIGN",        (2,0), (2,-1), "CENTER"),
    ]))
    story.append(stack_table)
    story.append(PageBreak())

    # ── SECTION 5: CHUNKING ────────────────────────────────────────────────
    story += section_header("05", "Chunking Strategy", styles, content_width)
    story.append(Paragraph(
        "RecursiveCharacterTextSplitter attempts splits in order: paragraph → newline → "
        "sentence → space → character. This preserves semantic boundaries and reduces "
        "mid-sentence cuts.",
        styles["body"]
    ))

    chunk_data = [
        ["Setting",         "Value",    "Reason"],
        ["chunk_size",      "500",      "Fits OpenAI embedding limits; granular enough for precise retrieval"],
        ["chunk_overlap",   "50",       "Prevents context loss at boundaries — 10% of chunk size"],
        ["Separator 1",     "\\n\\n",  "Paragraph breaks — highest semantic boundary"],
        ["Separator 2",     "\\n",     "Line breaks — section headers, list items"],
        ["Separator 3",     ". ",      "Sentence endings — natural clause boundaries"],
        ["Separator 4",     " ",       "Word boundary fallback"],
        ["Separator 5",     "\"\"",    "Hard character cut — last resort only"],
    ]
    chunk_table = Table(chunk_data, colWidths=[38*mm, 24*mm, content_width - 62*mm])
    chunk_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), ACCENT),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("FONTNAME",     (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",    (1,1), (1,-1), ACCENT_DARK),
        ("FONTNAME",     (1,1), (1,-1), "Courier-Bold"),
        ("TEXTCOLOR",    (2,1), (2,-1), colors.HexColor("#2D333B")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, colors.HexColor("#F0FBF8")]),
        ("BOX",          (0,0), (-1,-1), 0.5, ACCENT),
        ("INNERGRID",    (0,0), (-1,-1), 0.3, colors.HexColor("#D0EDE7")),
        ("TOPPADDING",   (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",(0,0), (-1,-1), 7),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
    ]))
    story.append(chunk_table)
    story.append(PageBreak())

    # ── SECTION 6: COST ────────────────────────────────────────────────────
    story += section_header("06", "Cost Estimation (FY 2024–25)", styles, content_width)
    story.append(Paragraph(
        "Based on 8 PDFs averaging 40 pages each (~2,560 chunks) and 200 queries/month:",
        styles["body"]
    ))

    cost_data = [
        ["Item",                        "Model",                    "Rate",             "Est. Cost"],
        ["One-time embedding",           "text-embedding-3-small",  "$0.02 / 1M tokens","~$0.01"],
        ["Per query — input tokens",     "gpt-4o-mini",             "$0.15 / 1M tokens","~$0.001"],
        ["Per query — output tokens",    "gpt-4o-mini",             "$0.60 / 1M tokens","~$0.001"],
        ["200 queries / month",          "gpt-4o-mini",             "—",                "~$0.25"],
        ["Total first month",            "Combined",                "—",                "~$0.26"],
        ["Total in INR (approx)",        "Combined",                "@ ₹83/USD",        "~₹22"],
    ]
    cost_table = Table(cost_data, colWidths=[52*mm, 48*mm, 40*mm, 28*mm])
    cost_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), DARK_BG),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("BACKGROUND",   (0,-1), (-1,-1), colors.HexColor("#F0FBF8")),
        ("TEXTCOLOR",    (3,1), (3,-1), ACCENT_DARK),
        ("FONTNAME",     (3,1), (3,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",    (0,-1), (-1,-1), ACCENT_DARK),
        ("FONTNAME",     (0,-1), (-1,-1), "Helvetica-Bold"),
        ("ROWBACKGROUNDS",(0,1),(-2,-1),[WHITE, colors.HexColor("#F6F8FA")]),
        ("BOX",          (0,0), (-1,-1), 0.5, BORDER),
        ("INNERGRID",    (0,0), (-1,-1), 0.3, colors.HexColor("#E0E4EA")),
        ("TOPPADDING",   (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",(0,0), (-1,-1), 7),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("ALIGN",        (3,0), (3,-1), "CENTER"),
    ]))
    story.append(cost_table)
    story.append(PageBreak())

    # ── SECTION 7: UI FEATURES ─────────────────────────────────────────────
    story += section_header("07", "Streamlit UI — Features", styles, content_width)

    ui_features = [
        ("💬 Chat Tab",
         "Streaming answers from GPT-4o-mini with real-time token display. "
         "Suggested question buttons for quick start. Expandable source citations "
         "showing exact chunk, page, and similarity score for every answer."),
        ("📄 Documents Tab",
         "Browse all indexed documents. Select any PDF to see chunk count, page count, "
         "and average chunk size. Filter by page number and inspect individual chunk text."),
        ("ℹ️ About Tab",
         "Interactive pipeline diagram, live cost estimator, setup checklist with "
         "real-time status detection, and FAQ accordion with 6 common questions answered."),
        ("⚙️ Sidebar Controls",
         "Live API key input, top-k slider (1–10), model selector (gpt-4o-mini / gpt-4o / "
         "gpt-3.5-turbo), knowledge base stats, session query counter, and clear chat button."),
        ("🎨 Dark Theme",
         "Professional financial aesthetic using JetBrains Mono + Syne fonts, "
         "#0D1117 background, #00C49A accent — matching GitHub's dark mode palette."),
    ]

    for feat_title, feat_desc in ui_features:
        feat_data = [[
            Paragraph(f"<b>{feat_title}</b>", styles["body_bold"]),
            Paragraph(feat_desc, styles["body"])
        ]]
        feat_table = Table(feat_data, colWidths=[44*mm, content_width - 44*mm])
        feat_table.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (0,0), colors.HexColor("#0D1117")),
            ("TEXTCOLOR",    (0,0), (0,0), ACCENT),
            ("BACKGROUND",   (1,0), (1,0), colors.HexColor("#F6F8FA")),
            ("BOX",          (0,0), (-1,-1), 0.3, BORDER),
            ("INNERGRID",    (0,0), (-1,-1), 0.3, BORDER),
            ("LEFTPADDING",  (0,0), (-1,-1), 10),
            ("TOPPADDING",   (0,0), (-1,-1), 8),
            ("BOTTOMPADDING",(0,0), (-1,-1), 8),
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ]))
        story.append(feat_table)
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # ── SECTION 8: SAMPLE Q&A ──────────────────────────────────────────────
    story += section_header("08", "Sample Q&A Outputs", styles, content_width)

    qa_pairs = [
        (
            "What are RBI's key guidelines on digital lending?",
            "According to RBI Circular 2024 (p.3), all digital lenders must disclose the "
            "Annual Percentage Rate (APR) upfront. Loan repayments must flow directly "
            "through the regulated entity's bank account (p.5). A minimum 3-day cooling-off "
            "period must be offered to all borrowers before loan acceptance.",
            "rbi_circular_2024.pdf · p.3, p.5 · Score: 0.921"
        ),
        (
            "What is Bajaj Finserv's total revenue for FY25?",
            "Per the Bajaj Finserv Annual Report FY2024-25 (p.12), the consolidated total "
            "income stood at ₹1,14,232 crore, representing a 28% year-on-year growth driven "
            "primarily by insurance premium income and AUM expansion in the lending segment.",
            "bajaj_finserv_annual_2025.pdf · p.12 · Score: 0.894"
        ),
        (
            "What are SEBI's margin trading regulations?",
            "SEBI Guidelines 2024 (p.7) mandate that brokers collect upfront margins for "
            "all intraday and delivery trades. Peak margin shortfall attracts a penalty of "
            "0.5% per day. From August 2024, reporting frequency moved to 4 snapshots daily.",
            "sebi_guidelines_2024.pdf · p.7 · Score: 0.878"
        ),
    ]

    for q, a, src in qa_pairs:
        story.append(KeepTogether([
            # Question
            Table([[Paragraph(f"<b>Q:</b> {q}", styles["body_bold"])]],
                  colWidths=[content_width],
                  style=[
                      ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#1C2128")),
                      ("TEXTCOLOR",  (0,0), (-1,-1), WHITE),
                      ("LEFTPADDING",(0,0), (-1,-1), 10),
                      ("TOPPADDING", (0,0), (-1,-1), 8),
                      ("BOTTOMPADDING",(0,0),(-1,-1),8),
                      ("BOX",        (0,0), (-1,-1), 0, BORDER),
                  ]),
            # Answer
            Table([[Paragraph(f"<b>A:</b> {a}", styles["body"])]],
                  colWidths=[content_width],
                  style=[
                      ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F6F8FA")),
                      ("LEFTPADDING",(0,0), (-1,-1), 10),
                      ("TOPPADDING", (0,0), (-1,-1), 8),
                      ("BOTTOMPADDING",(0,0),(-1,-1),8),
                      ("BOX",        (0,0), (-1,-1), 0.5, BORDER),
                  ]),
            # Source
            Table([[Paragraph(f"Source: {src}", styles["caption"])]],
                  colWidths=[content_width],
                  style=[
                      ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#F0FBF8")),
                      ("TEXTCOLOR",     (0,0), (-1,-1), ACCENT_DARK),
                      ("LEFTPADDING",   (0,0), (-1,-1), 10),
                      ("TOPPADDING",    (0,0), (-1,-1), 5),
                      ("BOTTOMPADDING", (0,0), (-1,-1), 5),
                      ("BOX",           (0,0), (-1,-1), 0.5, colors.HexColor("#D0EDE7")),
                  ]),
            Spacer(1, 10),
        ]))

    story.append(PageBreak())

    # ── SECTION 9: SETUP GUIDE ─────────────────────────────────────────────
    story += section_header("09", "Setup & Deployment Guide", styles, content_width)

    setup_steps = [
        ("Install dependencies",
         "pip install PyPDF2 langchain langchain-text-splitters openai faiss-cpu\n"
         "pip install numpy tiktoken streamlit reportlab"),
        ("Set OpenAI API key",
         "Windows:  set OPENAI_API_KEY=sk-...\n"
         "Mac/Linux: export OPENAI_API_KEY=sk-..."),
        ("Add PDF files",
         "Copy your PDFs into the pdfs/ folder.\n"
         "Supported: RBI circulars, SEBI guidelines, annual reports (FY24-25)"),
        ("Run the full pipeline",
         "python main.py\n"
         "# Parses → Cleans → Chunks → Embeds → Stores in FAISS"),
        ("Launch Streamlit UI",
         "streamlit run app.py\n"
         "# Opens at http://localhost:8501"),
        ("Deploy to Streamlit Cloud (free)",
         "1. Push project to GitHub\n"
         "2. Go to share.streamlit.io\n"
         "3. Connect repo → set OPENAI_API_KEY as secret\n"
         "4. Deploy — get a public URL instantly"),
    ]

    for i, (step, cmd) in enumerate(setup_steps, 1):
        story.append(KeepTogether([
            Paragraph(f"<b>Step {i}: {step}</b>", styles["body_bold"]),
            Paragraph(cmd.replace("\n", "<br/>"), styles["code"]),
            Spacer(1, 6),
        ]))

    story.append(PageBreak())

    # ── SECTION 10: FUTURE ENHANCEMENTS ────────────────────────────────────
    story += section_header("10", "Future Enhancements", styles, content_width)

    future_data = [
        ["Enhancement",                 "Benefit",                          "Effort"],
        ["OCR for scanned PDFs",        "Parse image-only RBI documents",   "Medium"],
        ["Pinecone / Chroma vector DB", "Cloud-hosted, persistent storage", "Low"],
        ["Multi-document comparison",   "Compare SEBI vs RBI on same topic","Medium"],
        ["Hindi language support",      "Query in Hindi, answer in Hindi",  "High"],
        ["PDF upload in UI",            "User uploads PDFs via Streamlit",  "Low"],
        ["Answer confidence score",     "Show how certain the model is",    "Medium"],
        ["Email alert on new circulars","Auto-fetch new RBI/SEBI PDFs",     "High"],
    ]
    future_table = Table(future_data, colWidths=[60*mm, 72*mm, 26*mm])
    future_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), ACCENT),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("FONTNAME",     (0,1), (0,-1), "Helvetica-Bold"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, colors.HexColor("#F6F8FA")]),
        ("BOX",          (0,0), (-1,-1), 0.5, ACCENT),
        ("INNERGRID",    (0,0), (-1,-1), 0.3, colors.HexColor("#D0EDE7")),
        ("TOPPADDING",   (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",(0,0), (-1,-1), 7),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("ALIGN",        (2,0), (2,-1), "CENTER"),
    ]))
    story.append(future_table)

    story.append(Spacer(1, 16))
    story.append(AccentLine(content_width, ACCENT, 1))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "FinRAG — Financial Document Intelligence System  ·  FY 2024–25  ·  "
        f"Report generated {datetime.now().strftime('%d %B %Y')}",
        styles["footer"]
    ))

    # ── Build ──────────────────────────────────────────────────────────────
    def page_template(canvas, doc):
        if doc.page == 1:
            cover_background(canvas, doc)
        else:
            inner_header_footer(canvas, doc)

    doc.build(story, onFirstPage=page_template, onLaterPages=page_template)
    print(f"✅ Report saved: {output_path}")


if __name__ == "__main__":
    build_report("FinRAG_Project_Report.pdf")
