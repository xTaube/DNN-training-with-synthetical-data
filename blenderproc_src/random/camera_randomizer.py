import blenderproc as bproc
import numpy as np
from abc import abstractmethod
from numpy.random import uniform
from typing import List, Optional, Union, Dict, Any
from blenderproc.python.types.MeshObjectUtility import MeshObject
from random import choice

from blenderproc_src.random.types import Range
from blenderproc_src.random import RandomStack


class CameraRandomizer:
    @staticmethod
    def calculate_rotation_matrix(
        position: np.ndarray,
        objects: List[MeshObject],
        noise: Range,
        inplane_rot: Optional[float] = None,
    ) -> np.ndarray:
        poi = bproc.object.compute_poi(objects)
        return bproc.camera.rotation_from_forward_vec(
            poi - position - uniform(*noise), inplane_rot=inplane_rot
        )

    @abstractmethod
    def get_random_position(self) -> np.ndarray:
        raise NotImplementedError

    def __call__(
        self,
        objects_of_interest: List[Union[RandomStack, MeshObject]],
        objects: List[Union[RandomStack, MeshObject]],
        cam_settings: Dict[str, Any],
        inplane_rot: Optional[float] = None,
        noise: Range = ((0, 0, 0), (0, 0, 0)),
    ) -> None:
        bvh_tree = bproc.object.create_bvh_tree_multi_objects(objects_of_interest+objects)
        for _ in range(10000):
            position = self.get_random_position()
            rotation_matrix = self.calculate_rotation_matrix(
                position, objects_of_interest, noise, inplane_rot
            )
            cam2world_matrix = bproc.math.build_transformation_mat(
                position,
                rotation_matrix
            )
            if all([
                bproc.camera.perform_obstacle_in_view_check(cam2world_matrix=cam2world_matrix, proximity_checks=cam_settings, bvh_tree=bvh_tree),
                bproc.camera.scene_coverage_score(cam2world_matrix=cam2world_matrix) > 0.1
            ]):
                bproc.camera.add_camera_pose(cam2world_matrix)
                break


class CameraUpperRegionSampler(CameraRandomizer):
    def __init__(self, region: MeshObject, min_height: float, max_height: float) -> None:
        self.region = region
        self.min_height = min_height
        self.max_height = max_height

    def get_random_position(self) -> np.ndarray:
        return bproc.sampler.upper_region(
            self.region,
            min_height=self.min_height,
            max_height=self.max_height
        )


class CameraDiskSampler(CameraRandomizer):
    def __init__(self, center_range: Range, radius_range: Range):
        super().__init__()
        self.center_range = center_range
        self.radius_range = radius_range

    def get_random_position(self) -> np.ndarray:
        return bproc.sampler.disk(
            center=uniform(*self.center_range),
            radius=uniform(*self.radius_range),
            sample_from=choice(["disk", "circle", "arc", "sector"]),
        )


class CameraPartSphereSampler(CameraRandomizer):
    def __init__(
        self,
        center_range: Range,
        part_sphere_vector_range: Range,
        radius_range: Range,
        distance_above_center_range: Range,
    ):
        super().__init__()
        self.center_range = center_range
        self.part_sphere_vector_range = part_sphere_vector_range
        self.radius_range = radius_range
        self.distance_above_center_range = distance_above_center_range

    def get_random_position(self) -> np.ndarray:
        return bproc.sampler.part_sphere(
            center=uniform(*self.center_range),
            part_sphere_dir_vector=uniform(*self.part_sphere_vector_range),
            mode=choice(["SURFACE", "INTERIOR"]),
            radius=uniform(*self.radius_range),
        )
