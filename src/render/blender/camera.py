import bpy
import numpy as np
from typing import Tuple
from pyquaternion import Quaternion
from mathutils import Vector

from src.render.blender.blender_object import BlenderObject
from src.render.blender.utils import str_direction_to_vector, normalize


class Camera(BlenderObject):

    def _create_reference_object(self):
        bpy.ops.object.camera_add()

    def look_at(self, point: Tuple[float, float, float], up: str = "Y", front: str = "-Z") -> None:
        world_up = str_direction_to_vector("Z")

        camera_up = normalize(str_direction_to_vector(up))
        camera_front = normalize(str_direction_to_vector(front))
        camera_right = np.cross(camera_up, camera_front)

        target_front = normalize(np.array(point) - np.array(self.location))
        target_right = normalize(np.cross(world_up, target_front))
        target_up = normalize(np.cross(target_front, target_right))

        rotation_matrix1 = np.stack([target_right, target_up, target_front])
        rotation_matrix2 = np.stack([camera_right, camera_up, camera_front])

        self.rotation = Quaternion(matrix=(rotation_matrix1.T @ rotation_matrix2))
