import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, KeepTogether, BaseDocTemplate, Frame, PageTemplate
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ── COLOR PALETTE ─────────────────────────────────────────────
WHITE = colors.HexColor("#FFFFFF")
GOLD = colors.HexColor("#C9A84C")
PURPLE = colors.HexColor("#4B1D6E")
DEEP_PURPLE = colors.HexColor("#2A0A45")
BLACK = colors.HexColor("#0D0D0D")
LIGHT_GOLD = colors.HexColor("#E8D5A3")
MID_PURPLE = colors.HexColor("#7B4FA6")
SMOKE = colors.HexColor("#F5F0FF")

# ── PAGE SETUP ────────────────────────────────────────────────
PAGE_W, PAGE_H = letter
MARGIN = 1.0 * inch

def make_canvas_bg(c, doc):
    """White page with subtle purple border rule at top and bottom."""
    c.saveState()
    c.setFillColor(WHITE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # gold top rule
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(MARGIN, PAGE_H - 0.45*inch, PAGE_W - MARGIN, PAGE_H - 0.45*inch)
    # gold bottom rule
    c.line(MARGIN, 0.45*inch, PAGE_W - MARGIN, 0.45*inch)
    # page number
    pg = doc.page
    c.setFont("Times-Roman", 9)
    c.setFillColor(PURPLE)
    c.drawCentredString(PAGE_W/2, 0.28*inch, str(pg))
    c.restoreState()

def make_cover_canvas(c, doc):
    """Full bleed deep purple cover."""
    c.saveState()
    # deep purple background
    c.setFillColor(DEEP_PURPLE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # gold ornamental bars
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 0.35*inch, PAGE_W, 0.35*inch, fill=1, stroke=0)
    c.rect(0, 0, PAGE_W, 0.35*inch, fill=1, stroke=0)
    # thin side bars
    c.rect(0, 0, 0.18*inch, PAGE_H, fill=1, stroke=0)
    c.rect(PAGE_W - 0.18*inch, 0, 0.18*inch, PAGE_H, fill=1, stroke=0)
    c.restoreState()

# ── STYLES ────────────────────────────────────────────────────
def get_styles():
    return {
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName="Times-Bold",
            fontSize=38,
            leading=46,
            textColor=WHITE,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            fontName="Times-Italic",
            fontSize=16,
            leading=22,
            textColor=GOLD,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "cover_author": ParagraphStyle(
            "cover_author",
            fontName="Times-Roman",
            fontSize=14,
            leading=18,
            textColor=LIGHT_GOLD,
            alignment=TA_CENTER,
        ),
        "cover_memoir": ParagraphStyle(
            "cover_memoir",
            fontName="Times-Italic",
            fontSize=11,
            leading=14,
            textColor=MID_PURPLE,
            alignment=TA_CENTER,
        ),
        "part_label": ParagraphStyle(
            "part_label",
            fontName="Times-Bold",
            fontSize=11,
            leading=14,
            textColor=GOLD,
            alignment=TA_CENTER,
            spaceBefore=6,
            spaceAfter=4,
        ),
        "part_title": ParagraphStyle(
            "part_title",
            fontName="Times-Bold",
            fontSize=26,
            leading=32,
            textColor=PURPLE,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "part_sub": ParagraphStyle(
            "part_sub",
            fontName="Times-Italic",
            fontSize=12,
            leading=16,
            textColor=MID_PURPLE,
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "chapter_num": ParagraphStyle(
            "chapter_num",
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            textColor=GOLD,
            alignment=TA_CENTER,
            spaceBefore=0,
            spaceAfter=4,
        ),
        "chapter_title": ParagraphStyle(
            "chapter_title",
            fontName="Times-Bold",
            fontSize=22,
            leading=28,
            textColor=PURPLE,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "chapter_sub": ParagraphStyle(
            "chapter_sub",
            fontName="Times-Italic",
            fontSize=11,
            leading=15,
            textColor=MID_PURPLE,
            alignment=TA_CENTER,
            spaceAfter=20,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Times-Roman",
            fontSize=11,
            leading=18,
            textColor=BLACK,
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            firstLineIndent=24,
        ),
        "body_first": ParagraphStyle(
            "body_first",
            fontName="Times-Roman",
            fontSize=11,
            leading=18,
            textColor=BLACK,
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            firstLineIndent=0,
        ),
        "fragment": ParagraphStyle(
            "fragment",
            fontName="Times-Roman",
            fontSize=11,
            leading=16,
            textColor=BLACK,
            alignment=TA_LEFT,
            spaceAfter=4,
            leftIndent=36,
            firstLineIndent=0,
        ),
        "mechanism_header": ParagraphStyle(
            "mechanism_header",
            fontName="Times-Bold",
            fontSize=10,
            leading=13,
            textColor=GOLD,
            alignment=TA_CENTER,
            spaceBefore=16,
            spaceAfter=8,
            letterSpacing=2,
        ),
        "mechanism_body": ParagraphStyle(
            "mechanism_body",
            fontName="Times-Italic",
            fontSize=10.5,
            leading=16,
            textColor=DEEP_PURPLE,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            leftIndent=18,
            rightIndent=18,
            firstLineIndent=0,
        ),
        "dedication": ParagraphStyle(
            "dedication",
            fontName="Times-Italic",
            fontSize=12,
            leading=20,
            textColor=PURPLE,
            alignment=TA_CENTER,
            spaceAfter=10,
        ),
        "content_note": ParagraphStyle(
            "content_note",
            fontName="Times-Roman",
            fontSize=10,
            leading=16,
            textColor=BLACK,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "toc_part": ParagraphStyle(
            "toc_part",
            fontName="Times-Bold",
            fontSize=11,
            leading=16,
            textColor=PURPLE,
            spaceBefore=10,
            spaceAfter=2,
        ),
        "toc_chapter": ParagraphStyle(
            "toc_chapter",
            fontName="Times-Roman",
            fontSize=10,
            leading=15,
            textColor=BLACK,
            leftIndent=18,
            spaceAfter=1,
        ),
    }

S = get_styles()

def gold_rule(width=0.4):
    return HRFlowable(width="80%", thickness=width, color=GOLD, spaceAfter=14, spaceBefore=6)

def chapter_opener(num, title, subtitle=None):
    items = [
        Spacer(1, 0.6*inch),
        Paragraph(f"CHAPTER {num}", S["chapter_num"]),
        Paragraph(title, S["chapter_title"]),
    ]
    if subtitle:
        items.append(Paragraph(subtitle, S["chapter_sub"]))
    items.append(gold_rule())
    items.append(Spacer(1, 0.1*inch))
    return items

def mechanism(text_paras):
    items = [
        Spacer(1, 16),
        HRFlowable(width="60%", thickness=0.4, color=PURPLE, spaceAfter=8, spaceBefore=0),
        Paragraph("THE MECHANISM", S["mechanism_header"]),
    ]
    for p in text_paras:
        items.append(Paragraph(p, S["mechanism_body"]))
    items.append(HRFlowable(width="60%", thickness=0.4, color=PURPLE, spaceAfter=12, spaceBefore=8))
    return items

def build_book(output_path, chapters_dir):
    doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=MARGIN)
    story = []

    # ═══ COVER PAGE ════════════════════════════════════════════
    story.append(Spacer(1, 1.8*inch))
    story.append(Paragraph("FROM THE STORM<br/>TO THE FIRE", S["cover_title"]))
    story.append(Spacer(1, 0.2*inch))
    story.append(gold_rule(1.2))
    story.append(Paragraph("The Machinery Behind the Silence", S["cover_subtitle"]))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Daniel \u201cBret\u201d Lingar", S["cover_author"]))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("A Memoir", S["cover_memoir"]))
    story.append(PageBreak())

    # ═══ CHAPTERS ══════════════════════════════════════════════
    chapter_files = sorted([f for f in os.listdir(chapters_dir) if f.endswith('.md')])
    
    for filename in chapter_files:
        with open(os.path.join(chapters_dir, filename), 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Basic parsing for chapter title and body
        lines = content.split('\n')
        title = lines[0].replace('## ', '').strip()
        body = '\n'.join(lines[1:]).strip()
        
        # Identify "The Mechanism" section
        mechanism_match = re.search(r'THE MECHANISM(.*?)$', body, re.DOTALL | re.IGNORECASE)
        if mechanism_match:
            main_body = body[:mechanism_match.start()].strip()
            mechanism_text = mechanism_match.group(1).strip()
        else:
            main_body = body
            mechanism_text = None
            
        # Add chapter opener
        if 'CHAPTER' in title.upper():
            num_match = re.search(r'CHAPTER\s+(\d+)', title, re.IGNORECASE)
            num = num_match.group(1) if num_match else "?"
            clean_title = re.sub(r'CHAPTER\s+\d+\s*[\u2014-]*\s*', '', title, flags=re.IGNORECASE).strip()
            story += chapter_opener(num, clean_title)
        else:
            story.append(Spacer(1, 0.5*inch))
            story.append(Paragraph(title, S["chapter_title"]))
            story.append(gold_rule())
            
        # Add body text
        for p in main_body.split('\n\n'):
            if p.strip():
                story.append(Paragraph(p.strip(), S["body"]))
                
        # Add mechanism if present
        if mechanism_text:
            story += mechanism([p.strip() for p in mechanism_text.split('\n\n') if p.strip()])
            
        story.append(PageBreak())

    doc.build(story, onFirstPage=make_canvas_bg, onLaterPages=make_canvas_bg)
    print(f"Successfully generated PDF at: {output_path}")

if __name__ == "__main__":
    build_book('exports/final-reportlab.pdf', 'book/chapters')
