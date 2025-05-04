import google.generativeai as genai
from config import Config


def call_gemini_model(ocr_data, target_text):
    """Call the Gemini API to analyze the OCR data."""
    prompt = f"""
    You are given OCR data extracted from a document image. Your task is to:
    1. Identify the most relevant answer to the query: "{target_text}".
    2. Return the bounding box location and the answer in a strict JSON format.

    ### RESPONSE FORMAT (IMPORTANT)
    Respond ONLY with raw JSON. DO NOT use triple backticks (```), the word 'json', or any markdown formatting.

    Return exactly this format:
    {{
      "answer": "<extracted_answer>",
      "bbox": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    }}

    Example:
    {{
      "answer": "John Doe",
      "bbox": [[10, 10], [100, 20], [100, 100], [10, 100]]
    }}

    DO NOT explain your answer. DO NOT add extra text or formatting.
    Just output raw JSON.
    """

    ocr_text = "\n".join([item["text"] for item in ocr_data])

    content = {
        "parts": [
            {
                "text": prompt
            },
            {
                "text": ocr_text
            }
        ]
    }

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(content)

    return extract_clean_json(response.text)

import re
import json

def extract_clean_json(text):
    """
    Extracts and parses JSON content from a model response with markdown formatting.
    Returns a Python dictionary.
    """
    cleaned = re.sub(r"```[a-zA-Z]*", "", text).replace("```", "")

    # Find the first '{' and the last '}'
    start = cleaned.find("{")
    end = cleaned.rfind("}") + 1

    if start == -1 or end == -1:
        raise ValueError("Valid JSON block not found.")

    json_str = cleaned[start:end]

    # Convert to dictionary
    return json.loads(json_str)


class GeminiAPI:
    def __init__(self):
        genai.api_key = Config.GEMINI_API_KEY
