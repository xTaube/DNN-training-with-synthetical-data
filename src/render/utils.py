import cv2
import numpy as np


def save_rgb_as_png(array: np.ndarray, filepath: str) -> None:
    cv2.imwrite(filepath, array)


def save_segmentation_as_png(array: np.ndarray, filepath: str) -> None:
    different_objects_count = len(np.unique(array))
    scaled = array * np.uint8(255/different_objects_count)
    hsv_map = cv2.applyColorMap(scaled, cv2.COLORMAP_HSV)
    cv2.imwrite(filepath, hsv_map)

