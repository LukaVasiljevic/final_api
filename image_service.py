from PIL import Image
import os
import uuid
import numpy as np
from ultralytics import YOLO
from app import app
import cv2
from io import BytesIO
from nst_implementation import stylize
from werkzeug.utils import secure_filename

# TODO points:
# replace model with a custom one
# additional parameters
#   for nst: (add if needed)
#   for yolo: check documentation and see if we need something else
# custom obj class num/name
# style picture (can be selected from the list for a start)
# extract hyperparameters
# distinct methods for debugging and usage
# think of enum for style_images
# reformat code and comment lines
# exec time: ~1.3 s


# !done find a way to save unique filename not to have it overwritten (if processed images are not going to be just temp) uuid?

PROCESSED_IMAGES_PATH = "processed_images/"
YOLO_MODEL_PATH = "models/yolov8n-seg.pt"


def process_image(image_file):
    img_bytes = image_file.read()
    res = predict_object(
        img_bytes
    )  # yolo obj detection. return type ultralytics.yolo.engine.results.Results
    res_img = create_mask(
        img_bytes, res
    )  # apply nst and replace pixels of detected object with styled image

    processed_image_filename = str(uuid.uuid4()) + get_extension(image_file)
    img_path = PROCESSED_IMAGES_PATH + processed_image_filename

    cv2.imwrite(os.path.join(app.static_folder, img_path), res_img)
    return img_path


def predict_object(img_bytes):
    img = Image.open(BytesIO(img_bytes))
    yolo_model = YOLO(YOLO_MODEL_PATH)
    res = yolo_model.predict(img)
    img.close()
    return res


def create_mask(image_bytes, res):
    nparr = np.frombuffer(image_bytes, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    generated_img = stylize(image_bytes)

    mask_img = (
        res[0].masks.data[0].numpy() * 255
    )  # this works only for the first detected object. To be modified later
    mask_img = cv2.resize(mask_img, (cv2_img.shape[1], cv2_img.shape[0]))

    res_array = np.copy(cv2_img)

    indices = np.where(mask_img > 0)
    res_array[indices] = generated_img[indices]

    return res_array


# # # HELPER FUNCTIONS

def get_extension(image_file):
    filename = secure_filename(image_file.filename)
    return os.path.splitext(filename)[1]
