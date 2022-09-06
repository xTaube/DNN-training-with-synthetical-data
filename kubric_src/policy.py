import numpy as np
from typing import List, Dict
from dataclasses import dataclass
from kubric import Quaternion
from numpy.random import uniform

from type import Range


@dataclass
class ModelPolicy:
    """Representation of model placing on scene policy"""

    category: str
    allowed_backgrounds: List[str]
    rotation: List[Dict[str, List[float]]]
    spawn_region: List[List[float]]
    scale: Range
    camera_position_sphere_radius: List[float]
    camera_look_at_noise: List[float]
    additional_objects_num: int
    min_visibility: int

    @property
    def random_rotation(self) -> Quaternion:
        return np.prod(
            [
                Quaternion(axis=rot["axis"], degrees=uniform(*rot["degrees"]))
                for rot in self.rotation
            ]
        )

    @property
    def random_scale(self) -> float:
        return uniform(*self.scale)
