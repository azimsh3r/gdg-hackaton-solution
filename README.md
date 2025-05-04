# Document Processing Web App

A Flask web application for extracting and analyzing text from uploaded documents using Google Vision OCR and Gemini API, with optional bounding box visualization.

## Features

- Upload an image document (e.g., JPG).
- Extract text and bounding boxes using Google Vision OCR.
- Use Gemini API to analyze and extract specific fields (e.g., name).
- Optionally highlight specific bounding boxes and generate a PDF with visual markup.
- View OCR output and analysis results on a simple web interface.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/document-processing-app.git
   cd document-processing-app
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Add your API credentials:**

   * Create a `config.py` file and add necessary keys (not tracked by Git):

     ```python
     GOOGLE_CREDENTIALS_PATH = "path/to/your/credentials.json"
     GEMINI_API_KEY = "your-gemini-api-key"
     ```

4. **Run the app:**

   ```bash
   flask run
   ```

5. **Open in your browser:**

   ```
   http://localhost:5000
   ```

## Notes

* Results are rendered in `result.html`.
* Uploaded and processed files are saved in the `static/` directory.
