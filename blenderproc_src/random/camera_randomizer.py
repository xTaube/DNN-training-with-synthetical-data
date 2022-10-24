import blenderproc as bproc
import numpy as np
from abc import abstractmethod
from numpy.random import uniform
from typing import List, Optional
from blenderproc.python.types.MeshObjectUtility import MeshObject, Entity
from random import choice

from blenderproc_src.random.types import Range
from blenderproc_src.random import RandomStack


class CameraRandomizer:
    @staticmethod
    def calculate_rotation_matrix(position: np.ndarray, objects: List[MeshObject], noise: Range, inplane_rot: Optional[float] = None) -> np.ndarray:
        poi = bproc.object.compute_poi(objects)
        return bproc.camera.rotation_from_forward_vec(poi - position - uniform(*noise), inplane_rot=inplane_rot)

    @abstractmethod
    def get_random_position(self) -> np.ndarray:
        raise NotImplementedError

    def __call__(self, objects: List[RandomStack], inplane_rot: Optional[float] = None, noise: Range = ((0, 0, 0), (0, 0, 0))) -> None:
        position = self.get_random_position()
        rotation_matrix = self.calculate_rotation_matrix(position, objects, noise, inplane_rot)
        cam2world_matrix = bproc.math.build_transformation_mat(position, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)


class CameraDiskSampler(CameraRandomizer):
    def __init__(self, center_range: Range, radius_range: Range):
        super().__init__()
        self.center_range = center_range
        self.radius_range = radius_range

    def get_random_position(self) -> np.ndarray:
        return bproc.sampler.disk(center=uniform(*self.center_range), radius=uniform(*self.radius_range), sample_from=choice(["disk", "circle", "arc", "sector"]))


class CameraPartSphereSampler(CameraRandomizer):
    def __init__(self, center_range: Range, part_sphere_vector_range: Range, radius_range: Range, distance_above_center_range: Range):
        super().__init__()
        self.center_range = center_range
        self.part_sphere_vector_range = part_sphere_vector_range
        self.radius_range = radius_range
        self.distance_above_center_range = distance_above_center_range

    def get_random_position(self) -> np.ndarray:
        return bproc.sampler.part_sphere(center=uniform(*self.center_range), part_sphere_dir_vector=uniform(*self.part_sphere_vector_range), mode=choice(["SURFACE", "INTERIOR"]), radius=uniform(*self.radius_range))
