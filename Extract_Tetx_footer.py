import fitz  # PyMuPDF
from docx import Document

def extract_pdf_text(pdf_path):
    """
    Extract text from a PDF while ignoring the text that appears near the bottom of the page (likely footers).
    """
    doc = fitz.open(pdf_path)
    extracted_text = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        page_height = page.rect.height
        blocks = page.get_text("blocks")  # Extract text blocks along with their positions
        cleaned_lines = []

        for block in blocks:
            block_text = block[4]  # Text content of the block
            block_y0 = block[1]    # Y-coordinate (top) of the block
            block_y1 = block[3]    # Y-coordinate (bottom) of the block

            # Only keep text blocks that are not too close to the bottom (footer area)
            if block_y0 > page_height * 0.85 or block_y1 > page_height * 0.85:
                continue  # Skip this block if it is near the bottom of the page

            cleaned_lines.append(block_text)

        # Combine all non-footer blocks into a single page's text
        page_text = "\n".join(cleaned_lines)
        extracted_text.append(page_text)

    doc.close()
    return extracted_text

def save_to_word(text_list, output_path):
    """
    Save the extracted text into a Word document.
    """
    document = Document()
    
    for page_text in text_list:
        document.add_paragraph(page_text)
    
    document.save(output_path)

# Path to the uploaded PDF file
pdf_path = 'Data Input Document 1_User Manual.pdf'
word_output_path = 'extracted_text.docx'

# Extract text from PDF and save to Word
extracted_text = extract_pdf_text(pdf_path)
save_to_word(extracted_text, word_output_path)

print(f"Extracted text has been saved to {word_output_path}")
