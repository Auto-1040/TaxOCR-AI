from flask import Flask, request, jsonify
from flask_cors import CORS
from app.ocr_service import process_ocr_and_ai
from app.s3_service import fetch_s3_file

app = Flask(__name__)
CORS(app)


@app.route("/process-s3-file", methods=["POST"])
def process_s3_file():
    """API endpoint that takes an S3 URL, fetches the file in-memory, and processes it."""
    data = request.json
    file_url = data.get("file_url")

    if not file_url:
        return jsonify({"error": "No file URL provided"}), 400

    pdf_bytes = fetch_s3_file(file_url)

    if not pdf_bytes:
        return jsonify({"error": "Failed to fetch file"}), 500

    try:
        json_result = process_ocr_and_ai(pdf_bytes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return json_result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
