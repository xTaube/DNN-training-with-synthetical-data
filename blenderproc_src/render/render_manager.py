import blenderproc as bproc
import numpy as np
from numpy.random import choice, uniform
from typing import Optional, Tuple, List
from blenderproc.python.types.MeshObjectUtility import MeshObject
from blenderproc.python.types.LightUtility import Light
from pathlib import Path
from glob import glob
from random import sample
from string import ascii_lowercase

from blenderproc_src.render.consts import RESOLUTION
from blenderproc_src.random import StackRandomizer
from blenderproc_src.random import CameraRandomizer, LightRandomizer
from blenderproc_src.render.utils import get_object_size
from blenderproc_src.random.types import Range


class RenderManager:
    def __init__(self):
        self.objects: List[MeshObject] = []
        self.lights: List[Light] = []
        self.walls: List[MeshObject] = []
        self.floor: Optional[MeshObject] = None

    @staticmethod
    def set_random_hdri_background(background_paths: str) -> None:
        path = bproc.loader.get_random_world_background_hdr_img_path_from_haven(background_paths)
        bproc.world.set_world_background_hdr_img(path)

    def set_walls(self, scale: Tuple[float, float, float], textures: Optional[List[Path]] = None) -> None:
        assert self.floor, "You need to setup floor first"
        floor_loc = self.floor.get_location()
        floor_size = get_object_size(self.floor)

        north_wall = bproc.object.create_primitive("CUBE")
        north_wall.set_scale(scale)
        north_wall.set_location([floor_loc[0], floor_loc[1] + floor_size[1]/2 + scale[1]/2, floor_loc[2] + scale[2]/2])
        north_wall.set_cp("category_id", 0)

        south_wall = bproc.object.create_primitive("CUBE")
        south_wall.set_scale(scale)
        south_wall.set_location([floor_loc[0], floor_loc[1]-(floor_size[1]/2 + scale[1]/2), floor_loc[2] + scale[2]/2])
        south_wall.set_cp("category_id", 0)

        east_wall = bproc.object.create_primitive("CUBE")
        east_wall.set_scale(scale)
        east_wall.set_location([floor_loc[0] + (floor_size[0]/2 + scale[1]/2), floor_loc[1], floor_loc[2] + scale[2]/2])
        east_wall.set_rotation_euler([0, 0, np.pi/2])
        east_wall.set_cp("category_id", 0)

        west_wall = bproc.object.create_primitive("CUBE")
        west_wall.set_scale(scale)
        west_wall.set_location([floor_loc[0] - (floor_size[0]/2 + scale[1]/2), floor_loc[1], floor_loc[2] + scale[2]/2])
        west_wall.set_rotation_euler([0, 0, np.pi/2])
        west_wall.set_cp("category_id", 0)

        if textures:
            wall_material = bproc.material.create_material_from_texture(np.random.choice(textures), "wall_mat")
            north_wall.add_material(wall_material)
            south_wall.add_material(wall_material)
            east_wall.add_material(wall_material)
            west_wall.add_material(wall_material)

        self.walls = [north_wall, south_wall, east_wall, west_wall]

    def set_floor(self, scale: Tuple[float, float, float], location: Tuple[float, float, float] = (0, 0, 0), textures: Optional[List[Path]] = None) -> None:
        self.floor = bproc.object.create_primitive("PLANE")
        self.floor.set_scale(scale)
        self.floor.set_location(location)
        self.floor.set_cp("category_id", 0)
        self.floor.set_cp("idx", 0)

        if textures:
            floor_material = bproc.material.create_material_from_texture(np.random.choice(textures), "floor_mat")
            self.floor.add_material(floor_material)

    def add_random_noise_objects(self, noise_objects_path: str, objects_num: int, location_range: Range, rotation_range: Range, scale_range: Range) -> None:
        noise_objects = []
        for _ in range(objects_num):
            obj_path = choice(glob(f"{noise_objects_path}/model/*.obj"))
            texture_path = obj_path.replace("model", "texture").replace(".obj", ".png")
            obj = bproc.loader.load_obj(obj_path)[0]
            obj.set_cp("category_id", 0)
            obj.set_cp("idx", 0)
            obj.set_name(''.join(sample(ascii_lowercase, 4)))
            obj.set_scale(uniform(*scale_range))

            obj_material = bproc.material.create_material_from_texture(texture_path, f"light{''.join(sample(ascii_lowercase, 4))}")
            if len(obj.get_materials()) > 0:
                obj.set_material(0, obj_material)
            else:
                obj.add_material(obj_material)
            noise_objects.append(obj)

        def position_sampler(mesh: MeshObject) -> None:
            mesh.set_location(uniform(*location_range))
            mesh.set_rotation_euler(uniform(*rotation_range))

        noise_objects = bproc.object.sample_poses_on_surface(objects_to_sample=noise_objects, surface=self.floor, sample_pose_func=position_sampler, min_distance=5, max_distance=20)
        self.objects.extend(noise_objects)

    def compose_scene(self, camera_randomizer: CameraRandomizer, light_randomizer: LightRandomizer, stack_randomizer: StackRandomizer, images_per_scene: int) -> None:
        bproc.camera.set_resolution(*RESOLUTION)
        stacks = stack_randomizer(self.objects)
        self.objects += stacks

        for _ in range(images_per_scene):
            camera_randomizer(stacks, noise=((-0.5, -0.5, -0.5), (0.5, 0.5, 0.5)))

    def clear_scene(self) -> None:
        for obj in self.objects:
            obj.delete()

        for light in self.lights:
            light.delete()

        for wall in self.walls:
            wall.delete()

        self.floor.delete()

        self.floor = None
        self.objects.clear()
        self.lights.clear()
        self.walls.clear()

    @staticmethod
    def render():
        data = bproc.renderer.render()
        data.update(bproc.renderer.render_segmap(map_by=["instance", "class", "name"]))
        return data
