import torch
from fst import utils
from fst import transformer
import os
from torchvision import transforms
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

STYLE_TRANSFORM_PATH = "fst/transforms/galatea_1.pth"
PRESERVE_COLOR = False

def stylize(content_img_bytes):
    if content_img_bytes is None:
        print("Error: Invalid image bytes.")
        return None

    file_bytes = np.frombuffer(content_img_bytes, np.uint8)
    content_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if content_image is None:
        print("Error: Failed to decode image.")
        return None

    # Device
    device = ("cuda" if torch.cuda.is_available() else "cpu")

    # Load Transformer Network
    net = transformer.TransformerNetwork()
    net.load_state_dict(torch.load(STYLE_TRANSFORM_PATH))
    net = net.to(device)

    with torch.no_grad():
        torch.cuda.empty_cache()
        starttime = time.time()
        content_tensor = utils.itot(content_image).to(device)
        generated_tensor = net(content_tensor)
        generated_image = utils.ttoi(generated_tensor.detach())
        if (PRESERVE_COLOR):
            generated_image = utils.transfer_color(content_image, generated_image)
        print("Transfer Time: {}".format(time.time() - starttime))
        
        cv2.imwrite('lukaTest.jpg', generated_image)
        utils.saveimg(generated_image, "helloworld.jpg")
        return np.copy(generated_image)