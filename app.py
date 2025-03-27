from flask import Flask, request, jsonify
from flask_cors import CORS

from app.exchange_rate_service import get_irs_exchange_rate_israel
from app.ocr_service import process_ocr_and_ai
from app.s3_service import fetch_s3_file

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
