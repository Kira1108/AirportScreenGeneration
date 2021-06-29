from abnormal import make_window
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from config import ABNORMAL_FODER, IMAGE_FOLDER
import glob
import os
import uuid 


def overlay(smaller, larger, x_offset = 0, y_offset = 0):
    """Overlay a smaller image onto the larger image"""
    y_end = y_offset + smaller.shape[0]
    x_end = x_offset + smaller.shape[1]

    larger[y_offset:y_end, x_offset:x_end] = smaller[:y_end-y_offset,:x_end - x_offset]
    return larger

def read_abnormal(ratio = None):
    ratio = ratio if ratio else 0.4 + (0.4) * np.random.random()
    img = make_window()
    new_img = cv2.resize(img, (0,0), img, ratio, ratio)
    return new_img


def read_image(path):
    return np.array(Image.open(path))

def generate_abnormal(normal, abnormal):
    y0, x0, _ = abnormal.shape
    y1, x1, _ = normal.shape
    x_offset = np.random.randint(0, x1 - x0)
    y_offset = np.random.randint(0, y1 - y0)
    im = overlay(abnormal, normal, x_offset = x_offset, y_offset = y_offset)
    return im

def nameit():
    return uuid.uuid4().hex[:12].upper() + '.jpg'


if __name__ == "__main__":
    image_files = glob.glob(os.path.join(IMAGE_FOLDER,"*.jpg"))
    for p in image_files:
        normal = read_image(p)
        abnormal = read_abnormal()
        img = generate_abnormal(normal, abnormal)
        cv2.imwrite(os.path.join(ABNORMAL_FODER, nameit()),cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
