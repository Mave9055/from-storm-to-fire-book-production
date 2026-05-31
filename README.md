# from-storm-to-fire-book-production

This repository is a simple, free, repeatable workflow for turning your manuscript into a polished, branded PDF ebook.

The goals:
- Keep the manuscript readable and easy to edit.
- Never delete or overwrite source files.
- Produce professional chapter openers in the white, gold, purple, and black book style.
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
  - `style-reference.md`: Notes and references for the visual style.
- **`/interior`** – Ebook interior design.
  - `templates/`: HTML/CSS templates used by the legacy WeasyPrint build.
  - `samples/`: Sample PDFs.
  - `sample-chapters/`: Example chapter files used for testing.
- **`/scripts`** – Build and formatting scripts.
  - `build_book_reportlab.py`: Current standard PDF builder.
  - `build_pdf.py`: Legacy HTML/CSS PDF builder.
  - `README-scripts.md`: Notes on how to run the scripts.
- **`/exports`** – Final output PDFs.
  - `free-sample.pdf`: Optional free sample.
  - `final-reportlab.pdf`: Default full PDF from the current standard builder.
  - `final-payhip.pdf`: Optional distribution filename if you choose that output name.

---

## Where to put things

### Manuscript

Put your full manuscript in:

- `book/manuscript.md` for an optional single-file version, and/or
- `book/chapters/chapter-XX.md` for the recommended one-file-per-chapter workflow.

Use simple Markdown:

- `#` or `##` for chapter titles.
- Normal paragraphs for body text.
- `THE MECHANISM` as its own section heading when you want the builder to style that section separately.
- `>` for short quoted/fragment blocks.
- `-` or `*` for bullet lists.

The standard build script reads from `book/chapters/` by default.

### Cover

Put final cover images in:

```bash
design/cover/
```

Recommended filename:

```bash
design/cover/cover-final.png
```

---

## How to export the book

You need Python 3 and the dependencies in `requirements.txt`.

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Build the standard PDF

```bash
python3 scripts/build_book_reportlab.py
```

Default output:

```bash
exports/final-reportlab.pdf
```

### 3. Build a sample PDF

```bash
python3 scripts/build_book_reportlab.py --max-chapters 3 --output exports/free-sample.pdf
```

### 4. Build with a Payhip filename

```bash
python3 scripts/build_book_reportlab.py --output exports/final-payhip.pdf
```

---

## Legacy WeasyPrint build

The older HTML/CSS builder is still available:

```bash
python3 scripts/build_pdf.py --input-dir book/chapters --output exports/final-payhip.pdf --title "From the Storm to the Fire" --author "Bret Lingar"
```

---

## Principles

- Do not delete or overwrite source files in `/book`.
- Keep the manuscript readable in plain Markdown.
- Use the branded white, gold, purple, and black style for the book package.
- Keep body pages clean and easy to read.
- Use generated files from `/exports` only after confirming the manuscript chapters are final.

---

> [!WARNING]
> **Do not upload placeholder exports to Payhip.** Ensure you have replaced any sample chapters in `/book/chapters` with your actual manuscript before generating final distribution files.
