import cv2
import numpy as np
import os
from random import choice
from glob import glob


def save_rgb_array_as_png(array: np.ndarray, filepath: str) -> None:
    bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filepath, bgr)


def save_segmentation_array_as_png(array: np.ndarray, filepath: str) -> None:
    different_objects_count = len(np.unique(array))
    scaled = array * np.uint8(255 / different_objects_count)
    hsv_map = cv2.applyColorMap(scaled, cv2.COLORMAP_HSV)
    cv2.imwrite(filepath, hsv_map)


def draw_background(backgrounds_dir: str) -> str:
    return choice(glob(f"{backgrounds_dir}/*"))


def draw_category(categories_dir: str) -> str:
    return choice(os.listdir(categories_dir))


def draw_model(category_dir: str) -> str:
    return choice(glob(f"{category_dir}/models/*"))


def get_model_texture_path(model_path: str) -> str:
    return model_path.replace("models", "textures").replace("obj", "png")
