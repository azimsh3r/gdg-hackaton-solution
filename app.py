from flask import Flask, render_template, request
from document_processing.gemini_apy import GeminiAPI, call_gemini_model
from document_processing.google_vision import GoogleVision
from document_processing.image_utils import ImageUtils
import uuid
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["document"]
        if file:
            filename = f"{uuid.uuid4().hex}.jpg"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            google_vision = GoogleVision()
            ocr_data = google_vision.extract_text_with_boxes(filepath)

            if not ocr_data:
                return render_template("result.html", error="No OCR data found.")

            gemini_api = GeminiAPI()
            gemini_result = call_gemini_model(ocr_data, "name")

            image_utils = ImageUtils()
            output_pdf_path = image_utils.draw_boxes(filepath, gemini_result)

            return render_template(
                "result.html",
                pdf_path=output_pdf_path,
                ocr_data=ocr_data,
                gemini_result=gemini_result,
            )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
