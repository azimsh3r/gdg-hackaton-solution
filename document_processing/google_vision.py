import os

from google.cloud import vision
import io
from config import Config

class GoogleVision:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = Config.GOOGLE_CREDENTIALS
        self.client = vision.ImageAnnotatorClient()

    def extract_text_with_boxes(self, image_path):
        """Extract text and bounding boxes from an image."""
        with io.open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.client.document_text_detection(image=image)
        annotations = []

        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        word_text = ''.join([symbol.text for symbol in word.symbols])
                        vertices = [(v.x, v.y) for v in word.bounding_box.vertices]
                        annotations.append({"text": word_text, "bbox": vertices})

        return annotations
