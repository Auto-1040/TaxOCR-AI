import fitz
import pytesseract
from PIL import Image
import io
import os
import json
import requests
import re
import platform

from flask import jsonify

# Set Tesseract OCR path
if platform.system() == "Windows":
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
    "taxYear": number,
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
    """Generate structured JSON output using Gemini AI via HTTP request."""
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.0,
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        response_json = response.json()

        # Extract JSON from response using regex to find text between {}
        try:
            raw_text = response_json['candidates'][0]['content']['parts'][0]['text']
            print(raw_text)
            json_text_match = re.search(r'(\{.*\})', raw_text.strip(), re.DOTALL)  # Match content between {}

            if json_text_match:
                json_text = json_text_match.group(0)  # Extract the matched JSON text
                return json_text  # Return only the extracted JSON
            else:
                print("No JSON structure found in the response.")
                return None
        except (KeyError, IndexError, json.JSONDecodeError, re.error) as e:
            print(f"Error extracting JSON: {e}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error generating text: {e}")
        return None


def process_ocr_and_ai(pdf_bytes):
    """Extracts text using OCR and sends it to Gemini, returning JSON with custom field names."""
    ocr_text = extract_text_from_pdf(pdf_bytes)
    full_prompt = COMBINED_PROMPT + ocr_text
    json_response = generate_text_from_gemini(full_prompt)
    print("3", json_response)
    # Attempt to parse the response as JSON
    try:
        original_data = json.loads(json_response)  # Parse the JSON string

        # Create a new dictionary with different field names
        custom_json_response = {
            "taxYear": original_data.get("taxYear", None),
            "field158_172": original_data.get("158/172", None),
            "field218_219": original_data.get("218/219", None),
            "field248_249": original_data.get("248/249", None),
            "field36": original_data.get("36", None)
        }

        return custom_json_response  # Return the new JSON object with custom field names
    except json.JSONDecodeError:
        print("Error: Response is not valid JSON")
        return None  # Return None if JSON parsing fails


