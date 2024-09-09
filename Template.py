import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document

# Configure the Google Gemini API with your API key
genai.configure(api_key="AIzaSyBNKJ5UoqldD8BwNVCwbDHs3GquaZ9OIjM")

# Set up the model configuration
generation_config = {
    "temperature": 0.7,
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

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_file_path):
    pdf_reader = PdfReader(pdf_file_path)
    raw_text = ''
    
    for page in pdf_reader.pages:
        text = page.extract_text()
        raw_text += text + "\n"
    
    return raw_text

# Function to process the text using Gemini API
def process_text_with_gemini(text, reference_content):
    prompt = f"""Using the reference content provided below, generate a detailed description of the product in question, for example a blood bank refrigerator.
    The description must include contraindications, relevant facts, and any other information related to the content. Extract each WARNING and CAUTION exactly as provided in pdf file 
    example:-WARNING:-,CAUTION:-in wherever relevant
    .
    
    Reference Content:\n{reference_content}\n
    Content to Process:\n{text}"""
    
    # Send the prompt to the Gemini model
    response = model.generate_content(prompt)
    
    return response.text if response else None

# Function to save generated response to a Word document
def save_to_word(generated_text, output_docx_path):
    doc = Document()
    doc.add_paragraph(generated_text)
    doc.save(output_docx_path)

# Main function to run the entire process
def extract_and_generate_response(pdf_file_path, reference_pdf_path, output_docx_path):
    # Extract text from the main PDF
    raw_text = extract_text_from_pdf(pdf_file_path)
    
    # Extract text from the reference PDF
    reference_content = extract_text_from_pdf(reference_pdf_path)
    
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
        print("No text extracted from one or both PDFs.")

# Example usage:
pdf_file_path = "Data Input Document 1_User Manual.pdf"  # Path to your input PDF
 # Path to your reference PDF
output_docx_path = "Generated_Response.docx"  # Path to save the generated Word document

extract_and_generate_response(pdf_file_path,output_docx_path)
