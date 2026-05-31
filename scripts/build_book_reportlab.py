#!/usr/bin/env python3
"""Build the From the Storm to the Fire ebook PDF from Markdown chapters.

This script is intentionally plain and local: it reads Markdown files from
book/chapters, applies a clean white/gold/purple interior, and writes a PDF to
exports/final-reportlab.pdf by default.
"""

from __future__ import annotations

import argparse
import html
import os
import re
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer

# ── COLOR PALETTE ─────────────────────────────────────────────
WHITE = colors.HexColor("#FFFFFF")
GOLD = colors.HexColor("#C9A84C")
PURPLE = colors.HexColor("#4B1D6E")
DEEP_PURPLE = colors.HexColor("#2A0A45")
BLACK = colors.HexColor("#0D0D0D")
LIGHT_GOLD = colors.HexColor("#E8D5A3")
MID_PURPLE = colors.HexColor("#7B4FA6")

# ── PAGE SETUP ────────────────────────────────────────────────
PAGE_W, PAGE_H = letter
MARGIN = 0.85 * inch

TITLE_DEFAULT = "From the Storm to the Fire"
SUBTITLE_DEFAULT = "Understanding CPTSD, Survival Mode, Shame, Addiction, and Recovery"
AUTHOR_DEFAULT = "Bret Lingar"


def make_body_canvas(c, doc):
    """White page with a subtle gold rule and purple page number."""
    c.saveState()
    c.setFillColor(WHITE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(MARGIN, PAGE_H - 0.45 * inch, PAGE_W - MARGIN, PAGE_H - 0.45 * inch)
    c.line(MARGIN, 0.45 * inch, PAGE_W - MARGIN, 0.45 * inch)

    c.setFont("Times-Roman", 9)
    c.setFillColor(PURPLE)
    c.drawCentredString(PAGE_W / 2, 0.28 * inch, str(doc.page))
    c.restoreState()


def make_cover_canvas(c, doc):
    """Full-page deep purple cover background."""
    c.saveState()
    c.setFillColor(DEEP_PURPLE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 0.35 * inch, PAGE_W, 0.35 * inch, fill=1, stroke=0)
    c.rect(0, 0, PAGE_W, 0.35 * inch, fill=1, stroke=0)
    c.rect(0, 0, 0.18 * inch, PAGE_H, fill=1, stroke=0)
    c.rect(PAGE_W - 0.18 * inch, 0, 0.18 * inch, PAGE_H, fill=1, stroke=0)
    c.restoreState()


def get_styles():
    return {
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName="Times-Bold",
            fontSize=36,
            leading=43,
            textColor=WHITE,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            fontName="Times-Italic",
            fontSize=14,
            leading=20,
            textColor=GOLD,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "cover_author": ParagraphStyle(
            "cover_author",
            fontName="Times-Roman",
            fontSize=15,
            leading=20,
            textColor=LIGHT_GOLD,
            alignment=TA_CENTER,
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
            spaceAfter=18,
        ),
        "heading": ParagraphStyle(
            "heading",
            fontName="Times-Bold",
            fontSize=14,
            leading=18,
            textColor=PURPLE,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=8,
            firstLineIndent=0,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Times-Roman",
            fontSize=11,
            leading=18,
            textColor=BLACK,
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            firstLineIndent=22,
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
            spaceAfter=5,
            leftIndent=28,
            firstLineIndent=0,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Times-Roman",
            fontSize=10.5,
            leading=16,
            textColor=BLACK,
            alignment=TA_LEFT,
            spaceAfter=5,
            leftIndent=24,
            firstLineIndent=-12,
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
    }


S = get_styles()


def clean_text(text: str) -> str:
    """Convert lightweight Markdown/typographic text into ReportLab-safe text."""
    text = text.strip()
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.*?)\*(?!\*)", r"<i>\1</i>", text)

    # Escape only the text outside the simple tags we intentionally allow.
    placeholders = {
        "<b>": "@@B_OPEN@@",
        "</b>": "@@B_CLOSE@@",
        "<i>": "@@I_OPEN@@",
        "</i>": "@@I_CLOSE@@",
        "<br/>": "@@BR@@",
    }
    for tag, marker in placeholders.items():
        text = text.replace(tag, marker)
    text = html.escape(text, quote=False)
    for tag, marker in placeholders.items():
        text = text.replace(marker, tag)
    return text.replace("\n", "<br/>")


def gold_rule(width: float = 0.4):
    return HRFlowable(width="80%", thickness=width, color=GOLD, spaceAfter=14, spaceBefore=6)


def split_blocks(markdown_text: str) -> List[str]:
    """Split text into paragraph-like blocks while keeping single-line fragments."""
    text = markdown_text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return []
    return [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]


def parse_chapter(content: str, fallback_num: int) -> Tuple[str, str, str]:
    """Return chapter number, title, body for a chapter markdown file."""
    lines = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    title_line = ""
    title_index: Optional[int] = None

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            title_line = stripped.lstrip("#").strip()
            title_index = index
            break
        if stripped:
            title_line = stripped
            title_index = index
            break

    if title_index is None:
        return str(fallback_num), f"Chapter {fallback_num}", ""

    body = "\n".join(lines[title_index + 1 :]).strip()
    num_match = re.search(r"\bchapter\s+([0-9ivxlcdm]+)\b", title_line, re.IGNORECASE)
    chapter_num = num_match.group(1).upper() if num_match else str(fallback_num)
    clean_title = re.sub(
        r"^chapter\s+[0-9ivxlcdm]+\s*[:\-–—]*\s*",
        "",
        title_line,
        flags=re.IGNORECASE,
    ).strip()
    clean_title = clean_title or f"Chapter {chapter_num}"
    return chapter_num, clean_title, body


def split_mechanism(body: str) -> Tuple[str, Optional[str]]:
    match = re.search(r"(^|\n)\s*(?:#{1,4}\s*)?THE MECHANISM\s*\n", body, re.IGNORECASE)
    if not match:
        return body, None
    return body[: match.start()].strip(), body[match.end() :].strip()


def add_cover(story: list, title: str, subtitle: str, author: str):
    display_title = clean_text(title.upper().replace(" TO THE ", "<br/>TO THE "))
    story.append(Spacer(1, 1.75 * inch))
    story.append(Paragraph(display_title, S["cover_title"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(gold_rule(1.2))
    story.append(Paragraph(clean_text(subtitle), S["cover_subtitle"]))
    story.append(Spacer(1, 0.55 * inch))
    story.append(Paragraph(clean_text(author), S["cover_author"]))
    story.append(PageBreak())


def chapter_opener(num: str, title: str):
    return [
        Spacer(1, 0.55 * inch),
        Paragraph(clean_text(f"CHAPTER {num}"), S["chapter_num"]),
        Paragraph(clean_text(title), S["chapter_title"]),
        gold_rule(),
        Spacer(1, 0.1 * inch),
    ]


def add_markdown_blocks(story: list, text: str):
    first_body = True
    for block in split_blocks(text):
        stripped = block.strip()
        if not stripped:
            continue
        if stripped.startswith("###") or stripped.startswith("##"):
            story.append(Paragraph(clean_text(stripped.lstrip("#").strip()), S["heading"]))
            first_body = True
            continue
        if re.match(r"^[-*]\s+", stripped):
            for line in stripped.split("\n"):
                item = re.sub(r"^[-*]\s+", "", line.strip())
                if item:
                    story.append(Paragraph("• " + clean_text(item), S["bullet"]))
            continue
        if stripped.startswith(">"):
            quote = re.sub(r"^>\s?", "", stripped, flags=re.MULTILINE)
            story.append(Paragraph(clean_text(quote), S["fragment"]))
            continue
        if "\n" in stripped and all(len(line.strip()) < 90 for line in stripped.split("\n") if line.strip()):
            for line in stripped.split("\n"):
                if line.strip():
                    story.append(Paragraph(clean_text(line), S["fragment"]))
            continue

        style = S["body_first"] if first_body else S["body"]
        story.append(Paragraph(clean_text(stripped), style))
        first_body = False


def add_mechanism(story: list, text: str):
    if not text.strip():
        return
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="60%", thickness=0.4, color=PURPLE, spaceAfter=8, spaceBefore=0))
    story.append(Paragraph("THE MECHANISM", S["mechanism_header"]))
    for block in split_blocks(text):
        story.append(Paragraph(clean_text(block), S["mechanism_body"]))
    story.append(HRFlowable(width="60%", thickness=0.4, color=PURPLE, spaceAfter=12, spaceBefore=8))


def chapter_files(chapters_dir: Path, max_chapters: Optional[int] = None) -> Sequence[Path]:
    files = sorted(path for path in chapters_dir.iterdir() if path.suffix.lower() == ".md")
    return files[:max_chapters] if max_chapters else files


def build_book(
    output_path: Path,
    chapters_dir: Path,
    title: str,
    subtitle: str,
    author: str,
    max_chapters: Optional[int] = None,
):
    if not chapters_dir.exists():
        raise FileNotFoundError(f"Chapter directory not found: {chapters_dir}")

    files = chapter_files(chapters_dir, max_chapters)
    if not files:
        raise FileNotFoundError(f"No .md chapter files found in: {chapters_dir}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=0.72 * inch,
        bottomMargin=0.72 * inch,
        title=title,
        author=author,
    )

    story: list = []
    add_cover(story, title, subtitle, author)

    for index, file_path in enumerate(files, start=1):
        content = file_path.read_text(encoding="utf-8")
        num, chapter_title, body = parse_chapter(content, index)
        main_body, mechanism_text = split_mechanism(body)

        story.extend(chapter_opener(num, chapter_title))
        add_markdown_blocks(story, main_body)
        if mechanism_text:
            add_mechanism(story, mechanism_text)
        story.append(PageBreak())

    doc.build(story, onFirstPage=make_cover_canvas, onLaterPages=make_body_canvas)
    print(f"Successfully generated PDF at: {output_path}")


def parse_args(argv: Optional[Iterable[str]] = None):
    parser = argparse.ArgumentParser(description="Build the From the Storm to the Fire ebook PDF.")
    parser.add_argument("--input-dir", default="book/chapters", help="Directory containing .md chapter files")
    parser.add_argument("--output", default="exports/final-reportlab.pdf", help="Output PDF path")
    parser.add_argument("--title", default=TITLE_DEFAULT, help="Book title")
    parser.add_argument("--subtitle", default=SUBTITLE_DEFAULT, help="Book subtitle")
    parser.add_argument("--author", default=AUTHOR_DEFAULT, help="Author name")
    parser.add_argument("--max-chapters", type=int, default=None, help="Optional chapter limit for samples")
    return parser.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None):
    args = parse_args(argv)
    build_book(
        output_path=Path(args.output),
        chapters_dir=Path(args.input_dir),
        title=args.title,
        subtitle=args.subtitle,
        author=args.author,
        max_chapters=args.max_chapters,
    )


if __name__ == "__main__":
    main()
