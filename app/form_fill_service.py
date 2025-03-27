import io

import fitz  # PyMuPDF
from pdfrw import PdfReader, PdfWriter
from app.field_mapping import FIELD_MAPPING  # Import the mapping from the separate file


def rewrite_pdf(input_path, output_path):
    """Rewrite PDF using pdfrw to fix reference issues."""
    reader = PdfReader(input_path)
    writer = PdfWriter(output_path)
    writer.addpages(reader.pages)
    writer.write()
    print(f"Rewritten PDF saved as: {output_path}")


def fill_pdf(pdf_stream, json_data):
    """Modify and list all form field names in a PDF."""
    # Open the PDF document
    doc = fitz.open("pdf", pdf_stream.read())

    # Iterate through all pages and widgets
    for page in doc:
        for widget in page.widgets():
            if widget.field_name:  # If it's a valid form field
                # Check if the widget name exists in the FIELD_MAPPING
                if widget.field_name in FIELD_MAPPING:
                    json_key = FIELD_MAPPING[widget.field_name]
                    # Retrieve the value from JSON data
                    value = json_data.get(json_key, None)

                    # If the value is not None, set it in the widget
                    if value is not None:
                        widget.field_value = str(value)  # Ensure the value is a string
                        widget.update()  # Apply the change

    # Save the modified PDF with editable fields
    output_stream = io.BytesIO()
    doc.save(output_stream, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()  # Close the document to release resources
    output_stream.seek(0)
    print(f"Updated PDF")
    return output_stream

