import numpy as np
from abc import abstractmethod
from blenderproc.python.types.MeshObjectUtility import MeshObject
from blenderproc.python.types.EntityUtility import Entity
from itertools import chain
from typing import List

from blenderproc_src.render.utils import is_overlapping


class Stack:
    def __init__(self, objects: List[MeshObject]):
        self.objects = objects
        self.reference = self._create_stack()

    @abstractmethod
    def _create_stack(self) -> Entity:
        raise NotImplementedError

    def get_object_from_stack(self, index: int) -> MeshObject:
        return self.objects[index]

    def get_bound_box(self) -> np.ndarray:
        all_points = np.array(list(chain(*[obj.get_bound_box() for obj in self.objects])))

        x_values = all_points[:, 0]
        y_values = all_points[:, 1]
        z_values = all_points[:, 2]

        min_x, max_x = np.min(x_values), np.max(x_values)
        min_y, max_y = np.min(y_values), np.max(y_values)
        min_z, max_z = np.min(z_values), np.max(z_values)

        return np.array([
            (min_x, min_y, min_z),
            (min_x, min_y, max_z),
            (min_x, max_y, min_z),
            (min_x, max_y, max_z),
            (max_x, min_y, min_z),
            (max_x, min_y, max_z),
            (max_x, max_y, min_z),
            (max_x, max_y, max_z)
        ])

    @property
    def location(self) -> np.ndarray:
        return self.reference.get_location()

    @location.setter
    def location(self, location: np.ndarray) -> None:
        self.reference.set_location(location)

    @property
    def scale(self) -> np.ndarray:
        return self.reference.get_scale()

    @scale.setter
    def scale(self, scale: np.ndarray) -> None:
        self.reference.set_scale(scale)

    @property
    def rotation(self) -> np.ndarray:
        return self.reference.get_rotation()

    @rotation.setter
    def rotation(self, rotation_euler: np.ndarray):
        self.reference.set_rotation_euler(rotation_euler)

    def delete(self):
        self.reference.delete()

    def check_collision_with_other_objects(self, objects: List) -> bool:
        return any([
            is_overlapping(self.get_bound_box(), obj.get_bound_box())
            for obj in objects if obj != self
        ])
