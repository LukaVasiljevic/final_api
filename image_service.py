from PIL import Image
import os
import uuid
import numpy as np
from app import app
import cv2
from io import BytesIO
from nst_implementation import stylize
from werkzeug.utils import secure_filename
from enums.Style import StyleModel
from enums.TransferMode import Mode

# TODO points:
# add new models 
# additional parameters
#   for nst: (add if needed)
#   for yolo: check documentation and see if we need something else
# reformat code and comment lines


# !done add a mode feature : apply nst either for class, inverse class or full style application
# !done think of enum for style_images
# !done find a way to save unique filename not to have it overwritten (if processed images are not going to be just temp) uuid?

PROCESSED_IMAGES_PATH = "processed_images/"


def get_segmentation_classes():
    return app.yolo_model.names


def get_styles():
    return StyleModel.read_collection()


def process_image(image_file, style_model_name, transfer_mode):
    img_bytes = image_file.read()
    res = predict_object(
        img_bytes
    )  # yolo obj detection. return type ultralytics.yolo.engine.results.Results
    res_img = create_mask(
        img_bytes, res, style_model_name, transfer_mode
    )  # apply nst and replace pixels of detected object with styled image

    processed_image_filename = str(uuid.uuid4()) + get_extension(image_file)
    img_path = PROCESSED_IMAGES_PATH + processed_image_filename

    cv2.imwrite(os.path.join(app.static_folder, img_path), res_img)
    return img_path


def predict_object(img_bytes):
    img = Image.open(BytesIO(img_bytes))
    res = app.yolo_model.predict(img)
    img.close()
    return res


def create_mask(image_bytes, res, style_model_name, transfer_mode):
    nparr = np.frombuffer(image_bytes, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    generated_img = stylize(image_bytes, style_model_name)

    mask_img = (
        res[0].masks.data[0].numpy() * 255
    )  # this works only for the first detected object. To be modified later
    mask_img = cv2.resize(mask_img, (cv2_img.shape[1], cv2_img.shape[0]))

    res_array = np.copy(cv2_img)
    indices = calculate_indices(mask_img, transfer_mode)
    output_img_arr = mask_original_image(
        res_array, generated_img, indices, transfer_mode
    )

    return output_img_arr

def mask_original_image(original_img_arr, generated_img_arr, indices, transfer_mode):
    if transfer_mode is Mode.FULL_STYLE_MODE:
        return generated_img_arr
    else:
        original_img_arr[indices] = generated_img_arr[indices]
        return original_img_arr

# # # HELPER FUNCTIONS

def calculate_indices(mask_img, transfer_mode):
    if transfer_mode is Mode.CLASS_MODE:
        return np.where(mask_img > 0)
    elif transfer_mode is Mode.INVERSE_MODE:
        return np.where(mask_img <= 0)

def get_extension(image_file):
    filename = secure_filename(image_file.filename)
    return os.path.splitext(filename)[1]
