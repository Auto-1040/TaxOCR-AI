from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from app.exchange_rate_service import get_irs_exchange_rate_israel
from app.form_fill_service import fill_pdf
from app.ocr_service import process_ocr_and_ai
from app.s3_service import fetch_s3_file
from app.config import S3_BUCKET_NAME, EMPTY_FORM_S3_KEY

app = Flask(__name__)
CORS(app)


@app.route("/payslip-data", methods=["POST"])
def extract_payslip_data_from_s3():
    """Receives an S3 URL of a payslip PDF, extracts relevant financial data using OCR and AI,
     and returns structured JSON."""
    data = request.json
    bucket_name = data.get("bucket_name")
    file_key = data.get("file_key")

    if not bucket_name or not file_key:
        return jsonify({"error": "No file URL provided"}), 400

    pdf_bytes = fetch_s3_file(bucket_name, file_key)
    if not pdf_bytes:
        return jsonify({"error": "Failed to fetch file"}), 500

    try:
        json_result = process_ocr_and_ai(pdf_bytes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return json_result


@app.route("/exchange-rate-israel", methods=["GET"])
def exchange_rate():
    """Retrieves the average exchange rate for Israel for a specified year.

        Expects a query parameter 'year' (integer). Returns the exchange rate
        if found, or appropriate error messages if the parameter is missing
        or the rate is not found.
    """
    year = request.args.get("year", type=int)
    if not year:
        return jsonify({"error": "Year parameter is required"}), 400

    rate = get_irs_exchange_rate_israel(year)
    if rate:
        return jsonify({"year": year, "exchange_rate": rate})
    else:
        return jsonify({"error": "Exchange rate not found"}), 404


@app.route("/form-1040", methods=["POST"])
def fill_pdf_endpoint():
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "Invalid JSON"}), 400

        form_key = EMPTY_FORM_S3_KEY
        bucket_name = S3_BUCKET_NAME
        # Fetch PDF from S3
        pdf_stream = fetch_s3_file(bucket_name, form_key)
        if pdf_stream is None:
            return {"error": "Failed to fetch PDF from S3"}, 500
        output_stream = fill_pdf(pdf_stream, json_data)

        # Return filled PDF as response
        return send_file(
            output_stream,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="filled_form.pdf",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
