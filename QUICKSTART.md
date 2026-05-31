# Quickstart Guide

Follow these steps to generate your book PDF.

## 1. Prepare chapters

Put your manuscript chapters as `.md` files in:

```bash
book/chapters/
```

Each chapter can start with either `#`, `##`, or a plain first-line title. The builder will use the first heading or first non-empty line as the chapter title.

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Build the standard PDF

```bash
python3 scripts/build_book_reportlab.py
```

That writes:

```bash
exports/final-reportlab.pdf
```

## 4. Optional sample build

To build only the first few chapters:

```bash
python3 scripts/build_book_reportlab.py --max-chapters 3 --output exports/free-sample.pdf
```

## 5. Optional custom title fields

```bash
python3 scripts/build_book_reportlab.py \
  --title "From the Storm to the Fire" \
  --subtitle "Understanding CPTSD, Survival Mode, Shame, Addiction, and Recovery" \
  --author "Bret Lingar" \
  --output exports/final-payhip.pdf
```

## Legacy WeasyPrint build

The older HTML/CSS build is still available:

```bash
python3 scripts/build_pdf.py --input-dir book/chapters --output exports/final-payhip.pdf --title "From the Storm to the Fire" --author "Bret Lingar"
```

For distribution, use the newest file you intentionally generated from your real manuscript chapters. Do not upload placeholder or sample exports to Payhip.
