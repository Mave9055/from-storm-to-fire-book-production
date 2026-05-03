# From Storm to Fire: Book Production Repo

This repository is designed to manage the production and maintenance of the ebook **"From the Storm to the Fire"**. It provides a repeatable workflow to turn a manuscript into a polished, branded PDF ebook with a cinematic dark storm/fire visual style.

## Repository Structure

- `/book`: Source files for the manuscript (e.g., `.docx`, `.pdf`).
- `/design`: Visual assets including the cover, promo images, and style references.
- `/interior`: Page templates and styled sample PDFs.
- `/scripts`: Python scripts for formatting and building the final PDF.
- `/exports`: Final production-ready PDFs for distribution (e.g., Payhip).

## Workflow Instructions

### 1. Update the Manuscript
Place your latest manuscript in the `/book` folder. The build script currently expects a text-based input or can be modified to parse specific formats.

### 2. Update the Cover
Replace `/design/cover.png` with your high-resolution cover art.

### 3. Style Guide
The book uses a "Dark Storm/Fire" aesthetic:
- **Background:** Charcoal/Black (#121212)
- **Headers:** Gold/Orange (#FFD700 / #FF8C00)
- **Text:** White/Off-white (#E0E0E0) for readability.
- **Accents:** Cinematic storm and fire textures.

### 4. Exporting the Book
Run the build script located in `/scripts`:
```bash
python3 scripts/build_pdf.py
```
The output will be generated in the `/exports` folder.

### 5. Updating Payhip
Once the files in `/exports` are ready, upload them to your Payhip dashboard to update the files for your customers.

## AI Agent / Copilot Prompt
If you are using an AI agent to help with this repo, use the following prompt:
> I need you to help me maintain this ebook production repo. Goal: Keep the dark storm/fire visual style consistent. Do not overwrite source files. Ensure the final PDF is professional, readable, and branded.
