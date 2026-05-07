# from-storm-to-fire-book-production

This repository is a simple, free, repeatable workflow for turning your manuscript into a polished, branded PDF ebook with a dark storm/fire visual style.

The goals:
- Keep the manuscript readable and easy to edit.
- Never delete or overwrite source files.
- Produce professional, cinematic chapter openers with a darker style.
- Keep normal reading pages clean and highly readable.
- Export final PDFs you can upload to Payhip.

---

## Folder overview

- **`/book`** – Your manuscript source files.
  - `manuscript.md`: Optional single-file version of the whole book.
  - `chapters/`: Individual chapter files (`chapter-01.md`, `chapter-02.md`, etc.).
- **`/design`** – Visual assets and references.
  - `cover/`: Final cover image(s) for Payhip and promo.
  - `promo/`: Social media and marketing images.
  - `style-reference.md`: Notes and references for the dark storm/fire style.
- **`/interior`** – Ebook interior design.
  - `templates/`: HTML/CSS templates used to generate the PDF.
  - `samples/`: Sample PDFs generated from placeholder text.
  - `sample-chapters/`: Example chapter files used for testing.
- **`/scripts`** – Build and formatting scripts.
  - `build_pdf.py`: Script to turn chapter text into a styled PDF.
  - `README-scripts.md`: Notes on how to run the scripts.
- **`/exports`** – Final output PDFs.
  - `free-sample.pdf`: The free sample you give away.
  - `final-payhip.pdf`: The final full ebook you upload to Payhip.

---

## Where to put things

### Manuscript

- Put your **full manuscript** in:
  - `book/manuscript.md` (optional, single-file version), and/or
  - `book/chapters/chapter-XX.md` (recommended, one file per chapter).

- Use simple Markdown:
  - `#` for the book title (once).
  - `##` for chapter titles.
  - Normal paragraphs for body text.

The build script will read from `book/chapters/` by default.

### Cover

- Put your **final cover image** in:
  - `design/cover/`

- Recommended:
  - `design/cover/cover-final.png`
  - Keep any alternate versions in the same folder with clear names.

---

## How to export the book

This repo uses a **free, local workflow** based on HTML/CSS and a Python script. You’ll need:

- Python 3 installed
- The `weasyprint` and `markdown` libraries

### 1. Install dependencies

```bash
pip install weasyprint markdown
```

### 2. Prepare your chapters

Make sure your chapters are in `book/chapters/` as Markdown files:
`chapter-01.md`, `chapter-02.md`, etc.
Each chapter should start with a level-2 heading:
`## Chapter One – From Storm to Spark`

### 3. Build the book

Run the build script from the root:
```bash
python3 scripts/build_pdf.py --input-dir book/chapters --output exports/final-payhip.pdf --title "From Storm to Fire" --author "Bret Lingar"
```

---

## Principles

- Do not delete or overwrite source files in `/book`.
- Keep the manuscript readable (plain Markdown).
- Use the dark storm/fire style for branding, but keep body pages clean and easy to read.
- Chapter openers are cinematic; normal pages are calmer and more minimal.

---

> [!WARNING]
> **Do not upload placeholder exports to Payhip.** Ensure you have replaced the sample chapters in `/book/chapters` with your actual manuscript before generating the final files for distribution.
