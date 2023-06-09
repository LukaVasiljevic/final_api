from flask import Flask, request, url_for
import image_service
import time
import os

STATIC_FOLDER = "static"

app = Flask(__name__, static_folder=STATIC_FOLDER)


@app.route("/process-image", methods=["POST"])
def process_image_controller():
    start_time = time.time()

    image = request.files["image"]
    processed_image_path = image_service.process_image(image)

    processed_image_url = url_for(
        STATIC_FOLDER, filename=processed_image_path, _external=True
    )

    end_time = time.time()
    execution_time = format(end_time - start_time, ".2f")
    return {
        "processed_image_path": processed_image_url,
        "execution_time": execution_time,
    }


if __name__ == "__main__":
    processed_images_dir = os.path.join(app.static_folder, "processed_images")
    os.makedirs(processed_images_dir, exist_ok=True)
    app.run()
