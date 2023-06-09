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
    res = predict_object(img_bytes) # yolo obj detection. return type ultralytics.yolo.engine.results.Results
    res_img = create_mask(img_bytes, res) # apply nst and replace pixels of detected object with styled image

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
    image = Image.open(BytesIO(image_bytes))
    original_array = np.array(image)

    cv2.imwrite('lukaOrig.jpg', original_array)


    generated_img = stylize(image_bytes)
    cv2.imwrite('lukaTestServ.jpg', generated_img)

    styled_test_img = Image.open("helloworld.jpg")
    styled_test_img = styled_test_img.resize((original_array.shape[1], original_array.shape[0]))
    styled_test_array = np.array(styled_test_img)

    mask_img = res[0].masks.data[0].numpy() * 255 # this works only for 1st detected object. to be modified later 
    mask_img = cv2.resize(mask_img, (original_array.shape[1], original_array.shape[0]))

    res_array = np.copy(original_array)

    indices = np.where(mask_img > 0)
    res_array[indices]  = generated_img[indices]

    cv2.imwrite('testRes.jpg', res_array)
    return cv2.cvtColor(res_array, cv2.COLOR_BGR2RGB)


# # # HELPER FUNCTIONS

def get_extension(image_file):
    filename = secure_filename(image_file.filename)
    return os.path.splitext(filename)[1]
