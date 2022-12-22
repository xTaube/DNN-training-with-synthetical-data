import blenderproc as bproc
import numpy as np
from blenderproc.python.types.EntityUtility import Entity
from blenderproc.python.types.MeshObjectUtility import MeshObject
from numpy.random import randint, uniform, choice
from pathlib import Path
from typing import Optional, List
from random import sample
from string import ascii_lowercase

from blenderproc_src.random.types import Range
from blenderproc_src.render.utils import get_object_size
from blenderproc_src.render import Stack


class RandomPartOfStackGenerator:
    def __init__(
        self,
        scale_range: Range,
        rotation_range: Range,
        textures: Optional[List[Path]] = None,
    ):
        self.scale_range = scale_range
        self.rotation_range = rotation_range
        self.textures = textures

    def _create_obj(self) -> MeshObject:
        raise NotImplemented

    def __call__(self) -> MeshObject:
        obj = self._create_obj()
        obj.set_scale(scale=uniform(*self.scale_range))
        obj.set_rotation_euler(rotation_euler=uniform(*self.rotation_range))
        obj.set_name("part_of_stack")
        obj.set_cp("category_id", 1)
        obj.set_cp("category", "part_of_stack")

        if self.textures:
            obj_material = bproc.material.create_material_from_texture(
                choice(self.textures), f"light{''.join(sample(ascii_lowercase, 4))}"
            )
            obj.replace_materials(obj_material)

        return obj


class RandomObjGenerator(RandomPartOfStackGenerator):
    def __init__(
        self,
        scale_range: Range,
        rotation_range: Range,
        obj_files_paths: List[Path],
        textures: Optional[List[Path]] = None,
    ):
        self.obj_file_path = obj_files_paths
        super().__init__(scale_range, rotation_range, textures)

    def _create_obj(self) -> MeshObject:
        return bproc.loader.load_obj(str(choice(self.obj_file_path)))[0]


class RandomCubeGenerator(RandomPartOfStackGenerator):
    def _create_obj(self) -> MeshObject:
        return bproc.object.create_primitive("CUBE")


class FlyingDistractorGenerator:
    def __init__(
        self, rotation_range: Range, scale_range: Range, location_range: Range
    ) -> None:
        self.rotation_range = rotation_range
        self.scale_range = scale_range
        self.location_range = location_range

    def __call__(self, num: int) -> List[MeshObject]:
        objects = [
            bproc.object.create_primitive(
                choice(["CYLINDER", "CONE", "SPHERE", "MONKEY"])
            )
            for _ in range(num)
        ]

        def sampler(mesh: MeshObject) -> None:
            mesh.set_location(uniform(*self.location_range))
            mesh.set_rotation_euler(uniform(*self.rotation_range))
            mesh.set_scale(uniform(*self.scale_range) * np.ones(3))

        pose_sampling_result = bproc.object.sample_poses(objects, sampler)
        distractors = list()
        for obj in objects:
            if not pose_sampling_result[obj][1]:
                obj.delete()
                continue

            mat = bproc.material.create(f"fd{''.join(sample(ascii_lowercase, 4))}")
            mat.set_principled_shader_value("Base Color", (*uniform(0, 1, size=3), 0))
            obj.add_material(mat)

            obj.set_name("flying_distractor")
            obj.set_cp("category_id", 0)
            obj.set_cp("category", "flying_distractor")
            obj.set_cp("idx", 0)
            distractors.append(obj)

        return distractors


class RandomStack(Stack):
    def __init__(
        self,
        obj_generators: List[RandomPartOfStackGenerator],
        no_of_objs: int,
    ):
        objects = [choice(obj_generators)() for _ in range(no_of_objs)]
        super().__init__(objects)

    def _create_stack(self) -> Entity:
        prev_obj = self.objects[0]
        for obj in self.objects[1:]:
            prev_obj_size = get_object_size(prev_obj)
            x, y, z = prev_obj.get_location()
            x += uniform(-prev_obj_size[0] / 4, prev_obj_size[0] / 4)
            y += uniform(-prev_obj_size[1] / 4, prev_obj_size[0] / 4)
            z += prev_obj_size[2]
            obj.set_location([x, y, z])
            prev_obj = obj

        return bproc.object.merge_objects(self.objects)

    def put_over(self, surface: MeshObject) -> None:
        surface_size = get_object_size(surface)
        base_z = surface_size[2] / 2
        self.location = np.array([self.set_location[0], self.set_location[1], base_z])


class StackRandomizer:
    def __init__(
        self,
        obj_generators: List[RandomPartOfStackGenerator],
        location_range: Range,
        rotation_range: Range,
        no_of_objs_range: Range,
        no_of_stack_range: Range,
        surface: Optional[bproc.python.types.MeshObjectUtility.MeshObject] = None,
    ):
        self.obj_generators = obj_generators
        self.location_range = location_range
        self.rotation_range = rotation_range
        self.no_of_objs_range = no_of_objs_range
        self.no_of_stack_range = no_of_stack_range
        self.surface = surface

    def __call__(self, objects: Optional[List[MeshObject]] = None) -> List[RandomStack]:
        if not objects:
            return [RandomStack(self.obj_generators, no_of_objs=randint(*self.no_of_objs_range)) for _ in range(randint(*self.no_of_stack_range))]

        stacks = []
        for _ in range(randint(*self.no_of_stack_range)):
            stack = RandomStack(
                self.obj_generators, no_of_objs=randint(*self.no_of_objs_range)
            )
            for iteration in range(1000):
                stack.location = uniform(*self.location_range)
                stack.rotation = uniform(*self.rotation_range)
                if self.surface:
                    stack.put_over(self.surface)
                if not stack.check_collision_with_other_objects(stacks + objects):
                    stacks.append(stack)
                    break
                if iteration == 999:
                    stack.delete()

        return stacks
