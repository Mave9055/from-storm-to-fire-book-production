import os
from fpdf import FPDF

class DarkEbookPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author_name = "Bret Lingar"
        self.book_title = "From the Storm to the Fire"
        self.subtitle = "A Peer-Written Trauma-Informed Survival Resource"

    def header(self):
        if self.page_no() > 1:
            self.set_font('Arial', 'I', 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, f'{self.book_title} - {self.author_name}', 0, 0, 'R')

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.add_page()
        # Dark background for chapter opener
        self.set_fill_color(18, 18, 18) # Charcoal
        self.rect(0, 0, 210, 297, 'F')
        
        # Gold border for chapter opener
        self.set_draw_color(255, 215, 0) # Gold
        self.set_line_width(1)
        self.rect(10, 10, 190, 277)
        
        self.set_y(100)
        self.set_font('Arial', 'B', 24)
        self.set_text_color(255, 140, 0) # Orange/Fire
        self.multi_cell(0, 15, title.upper(), 0, 'C')
        
        self.set_y(250)
        self.set_font('Arial', '', 10)
        self.set_text_color(255, 215, 0) # Gold
        self.cell(0, 10, self.subtitle, 0, 1, 'C')
        self.cell(0, 10, self.author_name, 0, 1, 'C')

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.set_text_color(224, 224, 224) # Off-white
        self.multi_cell(0, 10, body)
        self.ln()

    def add_styled_page(self):
        self.add_page()
        self.set_fill_color(18, 18, 18) # Charcoal
        self.rect(0, 0, 210, 297, 'F')

def create_sample_pdf(output_path, title_text):
    pdf = DarkEbookPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Chapter 1
    pdf.chapter_title("Chapter 1: The Gathering Storm")
    pdf.add_styled_page()
    content = (
        "The sky turned a bruised purple, the kind of color that promised nothing but destruction. "
        "Lightning arced across the horizon, a jagged gold vein in the heart of the darkness. "
        "This was the beginning. From the storm, the fire would rise.\n\n"
        "Placeholder text for the manuscript. The readability is maintained with off-white text "
        "against a dark charcoal background, ensuring a cinematic feel without sacrificing the "
        "reader's experience. This resource is trauma-informed and peer-written for survival."
    )
    pdf.chapter_body(content * 5) # Repeat to fill page
    
    # Chapter 2
    pdf.chapter_title("Chapter 2: The Rising Fire")
    pdf.add_styled_page()
    content_2 = (
        "Embers danced in the wind, carrying the scent of scorched earth. What the storm had "
        "broken, the fire would now consume. It was a cycle as old as time itself. "
        "Bret Lingar's journey through the trial by fire leads to a new purpose."
    )
    pdf.chapter_body(content_2 * 5)
    
    pdf.output(output_path)

if __name__ == "__main__":
    exports_dir = "exports"
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
        
    print("Generating Early Reader Edition...")
    create_sample_pdf(os.path.join(exports_dir, "From-the-Storm-to-the-Fire-Early-Reader-Edition.pdf"), "Full Edition")
    
    print("Generating Free Sample...")
    create_sample_pdf(os.path.join(exports_dir, "From-the-Storm-to-the-Fire-Free-Sample.pdf"), "Free Sample")
    
    print("Done!")
