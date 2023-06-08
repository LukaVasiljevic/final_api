from PIL import Image
import os
import numpy as np
from ultralytics import YOLO
from app import app
import cv2
from io import BytesIO
from nst_implementation import stylize
import torchvision.transforms.functional as TF
from fst import utils


DETECTION_PATH = "./static/results/" # ???

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
# exec time: 40.44 s 
# find a way to save unique filename not to have it overwritten (if processed images are not going to be just temp)

def process_image(image):
    img_bytes = image.read()
    res = predict_object(img_bytes) # yolo obj detection. return type ultralytics.yolo.engine.results.Results
    res_img = create_mask(img_bytes, res) # apply nst and replace pixels of detected object with styled image

    # Create the 'processed_images' directory if it doesn't exist
    processed_images_dir = os.path.join(app.static_folder, "processed_images")
    os.makedirs(processed_images_dir, exist_ok=True)

    
    processed_image_filename = "processed_" + image.filename
    processed_image_path = os.path.join("processed_images", processed_image_filename).replace("\\", "/")
    processed_image_fullpath = os.path.join(app.static_folder, processed_image_path)

    # res_img.save(processed_image_fullpath)
    cv2.imwrite(processed_image_fullpath, res_img)
    return processed_image_path


def predict_object(img_bytes):
    img = Image.open(BytesIO(img_bytes))
    yolo_model = YOLO("yolov8n-seg.pt")
    res = yolo_model.predict(img)
    img.close()
    return res

def create_mask(image_bytes, res):
    original_array = np.array(BytesIO(image_bytes)) # transform image to a numpy array 
    styled_img = stylize(original_array)

    # styled_array_resized = styled_img.resize(original_array.size, Image.BICUBIC)
    styled_array_resized_uint8 = np.array(styled_img).astype(np.uint8)



    mask_img = res[0].masks.data[0].numpy() * 255 # this works only for 1st detected object. to be modified later 
    mask_img = cv2.resize(mask_img, (original_array.size[1], original_array.size[0]))

    res_array = np.copy(original_array)

    indices = np.where(mask_img > 0)
    res_array[indices] = styled_array_resized_uint8[indices] # apply styled_img pixel to original image where an object is detected

    res_img = Image.fromarray(res_array)
    return res_img