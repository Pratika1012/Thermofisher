import fitz  # PyMuPDF
from PIL import Image
import io
import os
import re

def extract_image_titles_from_page(page):
    titles = []
    text = page.get_text("text")
    for line in text.split('\n'):
        match = re.match(r"Figure \d+\. .+", line)
        if match:
            titles.append(match.group(0))
    return titles

def extract_images_from_pdf(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    image_count = 0

    # Create the output directory if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)
        titles = extract_image_titles_from_page(page)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert CMYK to RGB if needed
            if image.mode == "CMYK":
                image = image.convert("RGB")
            
            # Use the title or a default name if title is not available
            title = titles[img_index] if img_index < len(titles) else f"Figure_{page_number + 1}_{img_index + 1}"
            title = title.replace(':', '')  # Remove invalid characters for filenames
            image_filename = os.path.join(output_folder, f"{title}.png")
            image.save(image_filename)
            image_count += 1

    return image_count

def main():
    pdf_path = r"Data Input Document 2_User Manual.pdf"
    output_folder = "ExtractedImages2"
    image_count = extract_images_from_pdf(pdf_path, output_folder)
    print(f"Extracted {image_count} images and saved in {output_folder}.")

if __name__ == "__main__":
    main()
