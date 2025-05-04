from PIL import Image, ImageDraw, UnidentifiedImageError
import os

class ImageUtils:
    @staticmethod
    def draw_boxes(image_path, extracted):
        """Draw bounding boxes and text on the image and save as PDF."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        try:
            image = Image.open(image_path).convert("RGB")
        except UnidentifiedImageError:
            raise UnidentifiedImageError(f"Cannot identify image file: {image_path}")

        draw = ImageDraw.Draw(image)

        for item in extracted:
            if "bbox" in item and "answer" in item:
                try:
                    draw.polygon(item["bbox"], outline="red", width=2)
                    draw.text(item["bbox"][0], item["answer"], fill="blue")
                except Exception as e:
                    print(f"Error drawing on image for item {item}: {e}")

        output_path = "static/output.pdf"
        image.save(output_path, "PDF", resolution=100.0)
        return output_path
