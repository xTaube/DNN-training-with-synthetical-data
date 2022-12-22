import numpy as np
from typing import List, Dict, Any

from blenderproc.python.types.MeshObjectUtility import MeshObject


def get_object_size(obj: MeshObject) -> np.ndarray:
    bbox3d = obj.get_bound_box()
    return np.max(bbox3d, axis=0) - np.min(bbox3d, axis=0)


def is_overlapping(bbox1: np.ndarray, bbox2: np.ndarray) -> bool:
    x_min1, y_min1, z_min1 = np.min(bbox1, axis=0)
    x_max1, y_max1, z_max1 = np.max(bbox1, axis=0)

    x_min2, y_min2, z_min2 = np.min(bbox2, axis=0)
    x_max2, y_max2, z_max2 = np.max(bbox2, axis=0)

    return all(
        [
            x_min1 <= x_max2,
            x_max1 >= x_min2,
            y_min1 <= y_max2,
            y_max1 >= y_min2,
            z_min1 <= z_max2,
            z_max1 >= z_min2,
        ]
    )
