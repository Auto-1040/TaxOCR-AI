import json
import fitz  # PyMuPDF
from field_mapping import FIELD_MAPPING  # Import the mapping from the separate file


def fill_pdf_form(input_pdf_path, output_pdf_path, data_json_path):
    """
    Fill a PDF form with data from a JSON file using PyMuPDF.

    :param input_pdf_path: Path to the original PDF form
    :param output_pdf_path: Path to save the filled PDF
    :param data_json_path: Path to JSON file containing form data
    """
    # Read JSON data
    with open(data_json_path, 'r', encoding='utf-8') as json_file:
        form_data = json.load(json_file)

    # Open the PDF
    doc = fitz.open(input_pdf_path)

    # Iterate through pages and widgets
    for page in doc:
        # Get all widgets on the page
        widgets = page.widgets()

        # Fill each widget
        for widget in widgets:
            # Iterate through field mapping
            for key, mapping in FIELD_MAPPING.items():
                # Handle simple string mappings (direct fields)
                if isinstance(mapping, str):
                    if key in form_data and widget.field_name == mapping:
                        widget.field_value = str(form_data[key])
                        widget.update()

                # Handle nested dictionary mappings (filing status, digital assets, etc.)
                elif isinstance(mapping, dict):
                    # Handle checkbox-type fields with nested dictionary
                    if key in form_data:
                        # For fields like FilingStatus or DigitalAssets
                        if form_data[key] in mapping:
                            if widget.field_name == mapping[form_data[key]]:
                                widget.field_value = "Yes"
                                widget.update()

                        # For nested fields like Income, Payments, etc.
                        for subkey, subvalue in mapping.items():
                            # Handle nested account types
                            if isinstance(subvalue, dict):
                                for subsubkey, subsubvalue in subvalue.items():
                                    if (isinstance(form_data[key], dict) and
                                            subkey in form_data[key] and
                                            form_data[key][subkey] == subsubkey and
                                            widget.field_name == subsubvalue):
                                        widget.field_value = "Yes"
                                        widget.update()

                            # Handle other nested fields
                            elif (isinstance(form_data[key], dict) and
                                  subkey in form_data[key] and
                                  widget.field_name == subvalue):
                                widget.field_value = str(form_data[key][subkey])
                                widget.update()

                # Handle Dependents (list of dictionaries)
                elif key == "Dependents" and key in form_data:
                    for dependent_index, dependent in enumerate(form_data[key], 1):
                        for dep_mapping in mapping:
                            for dep_field, dep_field_name in dep_mapping.items():
                                if (dep_field in dependent and
                                        widget.field_name == dep_field_name):
                                    # Special handling for boolean fields
                                    if isinstance(dependent[dep_field], bool):
                                        widget.field_value = "Yes" if dependent[dep_field] else ""
                                    else:
                                        widget.field_value = str(dependent[dep_field])
                                    widget.update()

    # Save the filled PDF
    doc.save(output_pdf_path, incremental=False)
    doc.close()

    print(f"PDF form filled and saved to {output_pdf_path}")


# Example usage
input_pdf = "../files/f1040_fixed.pdf"
output_pdf = "../files/f1040_modified.pdf"
json_data = "tax_form_data.json"

fill_pdf_form(input_pdf, output_pdf, json_data)
