import torch
from . import utils
from . import transformer
import os
from torchvision import transforms
import time
import cv2

STYLE_TRANSFORM_PATH = "fst/transforms/galatea_1.pth"
PRESERVE_COLOR = False

def stylize():
    # Device
    device = ("cuda" if torch.cuda.is_available() else "cpu")

    # Load Transformer Network
    net = transformer.TransformerNetwork()
    net.load_state_dict(torch.load(STYLE_TRANSFORM_PATH))
    net = net.to(device)

    with torch.no_grad():
        while(1):
            torch.cuda.empty_cache()
            print("Stylize Image~ Press Ctrl+C and Enter to close the program")
            content_image_path = input("Enter the image path: ")
            content_image = utils.load_image(content_image_path)
            starttime = time.time()
            content_tensor = utils.itot(content_image).to(device)
            generated_tensor = net(content_tensor)
            generated_image = utils.ttoi(generated_tensor.detach())
            if (PRESERVE_COLOR):
                generated_image = utils.transfer_color(content_image, generated_image)
            print("Transfer Time: {}".format(time.time() - starttime))
            utils.show(generated_image)
            utils.saveimg(generated_image, "helloworld.jpg")