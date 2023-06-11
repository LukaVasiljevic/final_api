from flask import Flask, request, url_for, g
import image_service
import time
import os
from ultralytics import YOLO
import json


STATIC_FOLDER = "static"
YOLO_MODEL_PATH = "models/seg/yolov8n-seg.pt"

app = Flask(__name__, static_folder=STATIC_FOLDER)
app.yolo_model = YOLO(YOLO_MODEL_PATH)

@app.route("/process-image", methods=["POST"])
def process_image_controller():
    start_time = time.time()

    image_file = request.files["image"]
    style_model_name = parse_style(request.files["style"])

    processed_image_path = image_service.process_image(image_file, style_model_name)

    processed_image_url = url_for(
        STATIC_FOLDER, filename=processed_image_path, _external=True
    )

    end_time = time.time()
    execution_time = format(end_time - start_time, ".2f")
    return {
        "processed_image_path": processed_image_url,
        "execution_time": execution_time,
    }


@app.route("/get-classes", methods=["GET"])
def read_collection_classes_controller():
    return image_service.get_segmentation_classes()

@app.route("/get-styles", methods=["GET"])
def read_collection_styles_controller():
    return image_service.get_styles()


def parse_style(style_file):
    style_content = style_file.read()
    style_data = json.loads(style_content)

    return style_data.get("style")


if __name__ == "__main__":
    processed_images_dir = os.path.join(app.static_folder, "processed_images")
    os.makedirs(processed_images_dir, exist_ok=True)
    app.run()
