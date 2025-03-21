import fitz  # PyMuPDF


def list_pdf_fields(pdf_path, output_path):
    """Modify and list all form field names in a PDF."""
    doc = fitz.open(pdf_path)  # Open the PDF

    for page in doc:
        for widget in page.widgets():  # Iterate through all form widgets on the page
            if widget.field_name:  # Check if it's a valid form field
                print(f"Updating field: {widget.field_name} (Type: {widget.field_type_string})")
                widget.field_value = "Miriam"  # Change field value
                widget.update()  # Apply the change

    # Save the modified PDF with editable fields
    doc.save(output_path, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()  # Close the document to release resources
    print(f"Updated PDF saved as: {output_path}")


# Run this to modify and list field names
list_pdf_fields("../f1040_fixed.pdf", "../f1040_modified.pdf")


