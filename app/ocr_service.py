import fitz
import pytesseract
from PIL import Image
import io
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
my_model = "models/gemini-1.5-flash"

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

COMBINED_PROMPT = """
As an AI assistant specializing in data extraction from scanned documents, 
your task is to process the following OCR-extracted text from an Israeli 106 form.
You are to return the values of specific fields as numbers within a JSON object.

Your response MUST FOLLOW THESE STRICT RULES:
1.  Return ONLY a valid JSON object.
2.  Do NOT include any text, explanations, or formatting outside of the JSON.
3.  If a field is not found, set its value to null.

The JSON structure you MUST use is:
{
    "158/172": number,
    "218/219": number,
    "248/249": number,
    "36": number
}

Here is the OCR text:
"""


def extract_text_from_pdf(pdf_bytes):
    """Convert PDF pages to images and perform OCR directly from bytes."""
    text = ""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")  # Open PDF from memory

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=300)  # Convert page to high-resolution image
        img = Image.open(io.BytesIO(pix.tobytes("png")))  # Convert to PIL format

        # Perform OCR on the image
        page_text = pytesseract.image_to_string(img, lang="eng+heb", config="--psm 6")
        text += f"\n--- Page {page_num + 1} ---\n" + page_text.strip()

    return text


def generate_text_from_gemini(prompt):
    """Generate structured JSON output using Gemini AI"""
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel(my_model)

        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.0,
                response_mime_type="application/json"
            ),
        )
        return response.text

    except Exception as e:
        print(f"Error generating text: {e}")
        return None


def process_ocr_and_ai(pdf_bytes):
    """Extracts text using OCR and sends it to Gemini."""
    ocr_text = extract_text_from_pdf(pdf_bytes)
    full_prompt = COMBINED_PROMPT + ocr_text
    json_response = generate_text_from_gemini(full_prompt)
    return json_response
