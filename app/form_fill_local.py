import fitz  # PyMuPDF
from pdfrw import PdfReader, PdfWriter
from field_mapping import FIELD_MAPPING  # Import the mapping from the separate file


def rewrite_pdf(input_path, output_path):
    """Rewrite PDF using pdfrw to fix reference issues."""
    reader = PdfReader(input_path)
    writer = PdfWriter(output_path)
    writer.addpages(reader.pages)
    writer.write()
    print(f"Rewritten PDF saved as: {output_path}")


def list_pdf_fields(pdf_path, output_path, json_data):
    """Modify and list all form field names in a PDF."""
    # Open the PDF document
    doc = fitz.open(pdf_path)

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
    doc.save(output_path, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()  # Close the document to release resources
    print(f"Updated PDF saved as: {output_path}")


json_data = {
    "first_name": "John",
    "last_name": "Doe",
    "ssn": "123-45-6789",
    "spouse_first_name": "Jane",
    "spouse_last_name": "Doe",
    "spouse_ssn": "987-65-4321",
    "address": "123 Main St",
    "apt_no": "4A",
    "city": "Los Angeles",
    "state": "CA",
    "zip_code": "90001",
    "foreign_country": "Canada",
    "foreign_state": "Ontario",
    "foreign_postal_code": "M5H 2N2",
    "campaign_you": True,
    "campaign_spouse": False,
    "total_income": 100000
}
# Run this to modify and list field names
list_pdf_fields("../files/f1040_fixed.pdf", "../files/f1040_modified.pdf", json_data)
