import bpy
import numpy as np
from typing import Tuple
from pyquaternion import Quaternion
from mathutils import Vector
from src.render.blender.blender_object import BlenderObject


class Camera(BlenderObject):

    def _create_reference_object(self):
        bpy.ops.object.camera_add()

    def look_at(self, point: Tuple[float, float, float]) -> None:
        target = np.array(point) - np.array(self.location)
        target = np.divide(target, np.linalg.norm(target))

        camera_origin_rotation_vec = np.array([0, 0, -1])
        camera_origin_rotation_vec = np.divide(camera_origin_rotation_vec, np.linalg.norm(camera_origin_rotation_vec))

        rot_axis = np.cross(camera_origin_rotation_vec, target)
        rot_angle = np.degrees(np.arccos(np.dot(camera_origin_rotation_vec, target)))

        self.rotation = Quaternion(axis=rot_axis, angle=(np.pi/180 * rot_angle))

    def roll(self, angle: float) -> None:
        focal_origin = Vector([0, 0, -1])
        focal_axis = self.rotation.to_matrix() @ focal_origin
        focal_axis = focal_axis/np.linalg.norm(focal_axis)
        self.rotate(Quaternion(axis=focal_axis, angle=(np.pi/180*angle)))
