import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document

# Configure the Google Gemini API with your API key
genai.configure(api_key="AIzaSyBNKJ5UoqldD8BwNVCwbDHs3GquaZ9OIjM")

# Set up the model configuration
generation_config = {
    "temperature": 0.8,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

# Initialize the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file_path):
    pdf_reader = PdfReader(pdf_file_path)
    raw_text = ''
    
    for page in pdf_reader.pages:
        text = page.extract_text()
        raw_text += text + "\n"
    
    return raw_text

# Function to extract text from a DOCX file
def extract_text_from_docx(docx_file_path):
    doc = Document(docx_file_path)
    raw_text = ''
    
    for paragraph in doc.paragraphs:
        raw_text += paragraph.text + "\n"
    
    return raw_text

# Function to process the text using Gemini API
def process_text_with_gemini(text, reference_content):
    prompt = f"""You must refer strictly to the reference template provided below and perform the following tasks:

1. **Contraindications**:
    Provide **Contraindications** of related that device.
    
2. **Device Description**:
    - Write a detailed description of the device based **solely** on the provided content.
    - The description must include relevant facts, numbers, figures, features, and any other significant information found in the content.
    - Include any potential adverse effects, as well as important warnings and precautions related to the device.
    - The description should be written in **3-4 paragraphs**.

3. **Warnings and Cautions**:
    - **Extract every single warning and caution** from the content and list them separately under the following format:
        - **Warnings List**:
            - WARNING: [extracted warning]
        - **Cautions List**:
            - CAUTION: [extracted caution]
    - Ensure **every** warning and caution present in the input PDFcontent is included.

4. **Trimming Sentences with 'Risk of...'**:
    -Extract Each and Every sentence of WARNING AND CAUTIONS LIST MENTIONED
    - **Before** listing the warnings and cautions, carefully check every sentence in these sections.*. 
    - After removing "Risk of...", the remaining sentence must still be grammatically correct.
    - **Example**:
        - Original: "WARNING: Risk of Shock. Your unit must be properly grounded in conformity with national and local electrical codes."
        - After trimming: "WARNING: Your unit must be properly grounded in conformity with national and local electrical codes."

**Important**: Ensure that all warnings and cautions are processed this way, and the output strictly follows the format, structure, and style of the reference template.



Reference Template:\n{reference_content}\n
Content to Process:\n{text}
"""

    
    # Send the prompt to the Gemini model
    response = model.generate_content(prompt)
    
    return response.text if response else None

# Function to save generated response to a Word document
def save_to_word(generated_text, output_docx_path):
    doc = Document()
    doc.add_paragraph(generated_text)
    doc.save(output_docx_path)

# Main function to run the entire process
def extract_and_generate_response(pdf_file_path, reference_docx_path, output_docx_path):
    # Extract text from the main PDF
    raw_text = extract_text_from_pdf(pdf_file_path)
    
    # Extract text from the reference DOCX file
    reference_content = extract_text_from_docx(reference_docx_path)
    
    if raw_text and reference_content:
        # Process the extracted text with Gemini for generating response
        generated_response = process_text_with_gemini(raw_text, reference_content)
        
        if generated_response:
            # Save the generated response to a Word document
            save_to_word(generated_response, output_docx_path)
            print(f"Generated response saved to {output_docx_path}")
        else:
            print("Failed to generate a response using Gemini.")
    else:
        print("No text extracted from one or both documents.")

# Example usage:
pdf_file_path = "Data Input Document 1_User Manual.pdf"  # Path to your input PDF
reference_docx_path = "Refernce-Template-Extract.docx"  # Path to your reference DOCX
output_docx_path = "Generated_Response(3).docx"  # Path to save the generated Word document

extract_and_generate_response(pdf_file_path, reference_docx_path, output_docx_path)
