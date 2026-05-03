import argparse
import os
import glob
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "interior" / "templates"

def load_chapters(input_dir, max_chapters=None):
    chapter_files = sorted(glob.glob(os.path.join(input_dir, "*.md")))
    chapters = []

    if max_chapters is not None:
        chapter_files = chapter_files[:max_chapters]

    for idx, filepath in enumerate(chapter_files, start=1):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        lines = text.splitlines()
        title = None
        body_lines = []

        for line in lines:
            if line.startswith("## ") and title is None:
                title = line[3:].strip()
            else:
                body_lines.append(line)

        if title is None:
            title = f"Chapter {idx}"

        body_md = "\n".join(body_lines).strip()
        body_html = markdown.markdown(body_md)

        chapters.append(
            {
                "number": idx,
                "title": title,
                "subtitle": "",
                "html_body": body_html,
            }
        )

    return chapters

def build_html(title, author, chapters):
    html_parts = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        f"<meta charset='UTF-8' />",
        f"<title>{title}</title>",
        "</head>",
        "<body>",
    ]

    for chapter in chapters:
        # Chapter opener
        html_parts.append("<section class='page page--chapter-opener'>")
        html_parts.append("<div class='content'>")
        html_parts.append(
            f"<div class='chapter-label'>Chapter {chapter['number']}</div>"
        )
        html_parts.append(f"<h1>{chapter['title']}</h1>")
        if chapter.get("subtitle"):
            html_parts.append(f"<div class='subtitle'>{chapter['subtitle']}</div>")
        html_parts.append("</div></section>")

        # Normal reading page
        html_parts.append("<section class='page page--normal'>")
        html_parts.append("<div class='content'>")
        html_parts.append(chapter["html_body"])
        html_parts.append("</div></section>")

    html_parts.append("</body></html>")
    return "\n".join(html_parts)

def main():
    parser = argparse.ArgumentParser(description="Build styled PDF from chapters.")
    parser.add_argument("--input-dir", required=True, help="Directory with .md chapters")
    parser.add_argument("--output", required=True, help="Output PDF path")
    parser.add_argument("--title", required=True, help="Book title")
    parser.add_argument("--author", required=True, help="Author name")
    parser.add_argument(
        "--max-chapters",
        type=int,
        default=None,
        help="Optional: limit number of chapters (for samples)",
    )

    args = parser.parse_args()

    chapters = load_chapters(args.input_dir, args.max_chapters)
    if not chapters:
        print(f"No .md files found in {args.input_dir}")
        return

    html_content = build_html(args.title, args.author, chapters)

    css_path = TEMPLATES_DIR / "ebook-style.css"
    if not css_path.exists():
        print(f"CSS file not found: {css_path}")
        return

    html = HTML(string=html_content, base_url=str(TEMPLATES_DIR))
    css = CSS(filename=str(css_path))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    html.write_pdf(str(output_path), stylesheets=[css])
    print(f"Successfully generated PDF at: {output_path}")

if __name__ == "__main__":
    main()
