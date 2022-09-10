import bpy
from abc import abstractmethod
from typing import Tuple
from pyquaternion import Quaternion
from src.render.blender.exceptions import ObjectReferenceNotExist


class BlenderObject:

    def __init__(self, location: Tuple[float, float, float] = (0, 0, 0), scale: Tuple[float, float, float] = (1, 1, 1), reference=None):
        self.reference = self._assign_reference(reference)
        self.scale = scale
        self.location = location

    def _assign_reference(self, reference):
        if not reference:
            bpy.ops.object.select_all(action="DESELECT")
            self._create_reference_object()
            return bpy.context.selected_objects[0]
        return reference

    @abstractmethod
    def _create_reference_object(self):
        raise NotImplementedError

    @property
    def scale(self) -> Tuple[int, int, int]:
        return self.reference.scale

    @scale.setter
    def scale(self, scale) -> None:
        self.reference.scale = scale

    @property
    def location(self) -> Tuple[int, int, int]:
        return self.reference.location

    @location.setter
    def location(self, location) -> None:
        self.reference.location = location

    @property
    def rotation(self):
        return self.reference.rotation_quaternion

    @rotation.setter
    def rotation(self, quaternion: Quaternion) -> None:
        self.reference.rotation_mode = 'QUATERNION'
        self.reference.rotation_quaternion = quaternion.q

    def rotate(self, quaternion: Quaternion) -> None:
        self.reference.rotation_mode = "QUATERNION"
        current_rotation = Quaternion(axis=self.rotation.axis, angle=self.rotation.angle)
        self.rotation = current_rotation * quaternion

    def delete(self) -> None:
        if not self.reference:
            raise ObjectReferenceNotExist
        bpy.ops.object.select_all(action="DESELECT")
        self.reference.select = True
        bpy.ops.object.delete()
        self.reference = None


class Cube(BlenderObject):

    def _create_reference_object(self) -> None:
        bpy.ops.mesh.primitive_cube_add()
