import bpy
import string
from abc import abstractmethod
from typing import Tuple, Any
from pyquaternion import Quaternion
from random import sample


from src.render.blender.exceptions import ObjectReferenceNotExist


class BlenderObject:

    def __init__(
            self,
            location: Tuple[float, float, float] = (0, 0, 0),
            scale: float = 1.0,
            rotation: Quaternion = Quaternion(0, 0, 0, 0),
            reference=None
    ):
        self.reference = self._assign_reference(reference)
        self.scale = scale
        self.location = location
        self.rotation = rotation
        self.metadata = {}

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
    def scale(self, scale: float) -> None:
        self.reference.scale = (scale, scale, scale)

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
        self.reference.select_set(True)
        bpy.ops.object.delete()
        self.reference = None


class Cube(BlenderObject):

    def _create_reference_object(self) -> None:
        bpy.ops.mesh.primitive_cube_add()


class ImportedObject(BlenderObject):

    def __init__(
            self,
            path: str,
            name: str = "".join(sample(string.ascii_lowercase, 4)),
            location: Tuple[float, float, float] = (0, 0, 0),
            scale: float = 1.0,
            rotation: Quaternion = Quaternion(0, 0, 0, 0),
            reference: Any = None
    ):
        self.path = path
        self.name = name
        super().__init__(location, scale, rotation, reference)

    def add_texture(self, texture_path: str) -> None:
        material = bpy.data.materials.new(name=f"mat_{self.name}")
        material.use_nodes = True
        bsdf = material.node_tree.nodes["Principled BSDF"]
        texture = material.node_tree.nodes.new("ShaderNodeTexImage")
        texture.image = bpy.data.images.load(texture_path)
        material.node_tree.links.new(bsdf.inputs["Base Color"], texture.outputs["Color"])

        if self.reference.data.materials:
            self.reference.data.materials[0] = material
        else:
            self.reference.data.materials.append(material)

    def _create_reference_object(self) -> None:
        bpy.ops.import_scene.obj(filepath=self.path)
