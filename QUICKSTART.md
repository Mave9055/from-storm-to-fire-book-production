# Quickstart Guide

Follow these steps to generate your book:

1. **Prepare Chapters:** Put your manuscript chapters as `.md` files in `/book/chapters`.
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Build the PDF:**
   - For the standard cinematic version:
     ```bash
     python3 scripts/build_book_reportlab.py
     ```
   - For the legacy WeasyPrint version:
     ```bash
     python3 scripts/build_pdf.py --input-dir book/chapters --output exports/final-payhip.pdf --title "From Storm to Fire" --author "Bret Lingar"
     ```
4. **Distribute:** Upload `exports/final-payhip.pdf` to Payhip.
