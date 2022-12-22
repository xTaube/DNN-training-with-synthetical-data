import blenderproc as bproc
import numpy as np
import os
from numpy.random import choice, uniform
from typing import Optional, Tuple, List
from blenderproc.python.types.MeshObjectUtility import MeshObject
from blenderproc.python.types.LightUtility import Light
from pathlib import Path
from glob import glob
from random import sample
from string import ascii_lowercase

from blenderproc_src.render.consts import RESOLUTION
from blenderproc_src.render.utils import get_object_size
from blenderproc_src.random import FlyingDistractorGenerator
from blenderproc_src.random import CameraRandomizer
from blenderproc_src.random.types import Range


class RenderManager:
    def __init__(self):
        self.objects_of_interest: List[MeshObject] = []
        self.noise_objects: List[MeshObject] = []
        self.lights: List[Light] = []
        self.floor: Optional[MeshObject] = None
        self.ceiling: Optional[MeshObject] = None
        self.wall: List[MeshObject] = []

    @staticmethod
    def set_random_hdri_background(background_paths: str) -> None:
        path = bproc.loader.get_random_world_background_hdr_img_path_from_haven(
            background_paths
        )
        bproc.world.set_world_background_hdr_img(path)

    def set_floor(
        self,
        scale: Tuple[float, float, float],
        location: Tuple[float, float, float] = (0, 0, 0),
        textures: Optional[List[Path]] = None,
    ) -> None:
        self.floor = bproc.object.create_primitive("PLANE")
        self.floor.set_scale(scale)
        self.floor.set_location(location)
        self.floor.set_cp("category_id", 0)
        self.floor.set_cp("idx", 0)

        if textures:
            floor_material = bproc.material.create_material_from_texture(
                np.random.choice(textures), "floor_mat"
            )
            self.floor.add_material(floor_material)

    def create_random_room(
        self,
        noise_objects_path: str,
        scale_range: Range,
        objects_num: int,
        wall_material_path: str,
        wall_material_types: List[str],
        floor_area: float = 25,
        wall_height: float = 5
    ) -> None:
        materials = bproc.loader.load_ccmaterials(wall_material_path, wall_material_types)
        room_objects = bproc.constructor.construct_random_room(
            wall_height=wall_height,
            used_floor_area=floor_area,
            interior_objects=[],
            materials=materials
        )
        self.floor = room_objects.pop()
        self.wall = room_objects.pop(0)
        self.ceiling = room_objects.pop(0)

        bproc.lighting.light_surface([self.ceiling], emission_strength=uniform(1, 4), emission_color=[*uniform((0.1, 0.9, 3)), 1])

        self.add_random_noise_objects_on_floor(noise_objects_path, scale_range, objects_num)

    def add_objects_of_interest(self, randomizer, sample_on_floor: bool = False) -> None:
        ooi = randomizer()
        if sample_on_floor:
            if not self.floor:
                raise(Exception("Floor is not set"))

            floor_size = get_object_size(self.floor)
            location_range = ((-floor_size[0] / 2, -floor_size[1] / 2, 0), (floor_size[0] / 2, floor_size[1] / 2, 0))

            def position_sampler(mesh: MeshObject) -> None:
                mesh.set_location(uniform(*location_range))

            ooi = bproc.object.sample_poses_on_surface(
                objects_to_sample=ooi,
                surface=self.floor,
                sample_pose_func=position_sampler,
                min_distance=0.01,
                max_distance=2000,
            )

        self.objects_of_interest.extend(ooi)

    def add_random_noise_objects(
        self,
        noise_objects_path: str,
        scale_range: Range,
        objects_num: int,
        rotation_range: Range = ((0, 0, 0), (0, 0, 2*np.pi)),
        location_range: Optional[Range] = None
    ) -> None:
        if self.floor:
            floor_size = get_object_size(self.floor)
            location_range = ((-floor_size[0]/2, -floor_size[1]/2, 0), (floor_size[0]/2, floor_size[1]/2, 0))

        if not location_range:
            raise Exception("You need to provide location_range or setup scene floor")

        noise_objects = []
        for _ in range(objects_num):
            obj_path = choice(glob(f"{noise_objects_path}/model/*.obj"))
            texture_path = obj_path.replace("model", "texture").replace(".obj", ".png")
            obj = bproc.loader.load_obj(obj_path)[0]
            obj.set_cp("category_id", 0)
            obj.set_cp("idx", 0)
            obj.set_name("".join(sample(ascii_lowercase, 4)))
            obj.set_scale(uniform(*scale_range) * np.ones(3))

            obj_material = bproc.material.create_material_from_texture(
                texture_path, f"light{''.join(sample(ascii_lowercase, 4))}"
            )
            if len(obj.get_materials()) > 0:
                obj.set_material(0, obj_material)
            else:
                obj.add_material(obj_material)
            noise_objects.append(obj)

        def position_sampler(mesh: MeshObject) -> None:
            mesh.set_location(uniform(*location_range))
            mesh.set_rotation_euler(uniform(*rotation_range))

        if self.floor:
            objects = bproc.object.sample_poses_on_surface(
                objects_to_sample=self.objects_of_interest+noise_objects,
                surface=self.floor,
                sample_pose_func=position_sampler,
                min_distance=0.5,
                max_distance=20,
            )
        else:
            objects = bproc.object.sample_poses(
                objects_to_sample=self.objects_of_interest+noise_objects,
                sample_pose_func=position_sampler
            )
        self.noise_objects.extend([obj for obj in objects if obj not in self.objects_of_interest])

    def add_flying_distractors(
        self, fd_generator: FlyingDistractorGenerator, num: int
    ) -> None:
        distractors = fd_generator(num)
        self.noise_objects.extend(distractors)

    def random_scenenet_room(self, scenenet_path: Path, scenenet_texture_path: str) -> None:
        label_mapping = bproc.utility.LabelIdMapping.from_csv(
            bproc.utility.resolve_resource(os.path.join('id_mappings', 'nyu_idset.csv'))
        )
        objs = bproc.loader.load_scenenet(str(scenenet_path), scenenet_texture_path, label_mapping)

        self.walls = bproc.filter.by_cp(objs, "category_id", label_mapping.id_from_label("wall"))
        for wall in self.walls:
            wall.set_cp("category_id", 0)
            objs.remove(wall)

        floors = [obj for obj in objs if obj.get_name() == 'floor']
        if floors:
            self.floor = floors[0]
            objs.remove(self.floor)
        else:
            self.floor = bproc.object.extract_floor(
                self.walls, new_name_for_object="floor",
                should_skip_if_object_is_already_there=True
            )[0]
        self.floor.set_cp("category_id", 0)

        ceilings = [obj for obj in objs if obj.get_name() == 'ceiling']
        if ceilings:
            self.ceiling = ceilings[0]
            objs.remove(self.ceiling)
        else:
            self.ceiling = bproc.object.extract_floor(
                self.walls, new_name_for_object="ceiling",
                up_vector_upwards=False,
                should_skip_if_object_is_already_there=True
            )[0]

        self.ceiling.set_cp("category_id", 0)

        self.lamps = bproc.filter.by_attr(objs, "name", ".*[l|L]amp.*", regex=True)
        for lamp in self.lamps:
            objs.remove(lamp)

        bproc.lighting.light_surface(self.lamps, emission_strength=15)
        bproc.lighting.light_surface([self.ceiling], emission_strength=2, emission_color=[1, 1, 1, 1])

        for obj in objs:
            obj.set_cp("category_id", 0)
            self.noise_objects.append(obj)

    def compose_scene(
        self,
        camera_randomizer: CameraRandomizer,
        images_per_scene: int,
        camera_noise: Range = ((0, 0, 0), (0, 0, 0))
    ) -> None:
        bproc.camera.set_resolution(*RESOLUTION)

        for _ in range(images_per_scene):
            camera_randomizer(
                self.objects_of_interest,
                self.noise_objects,
                {"min": 50},
                noise=camera_noise
            )

    def clear_scene(self) -> None:
        for obj in self.objects_of_interest:
            obj.delete()

        for obj in self.noise_objects:
            obj.delete()

        for light in self.lights:
            light.delete()

        if self.floor:
            self.floor.delete()
            self.floor = None

        if self.wall:
            self.wall.delete()
            self.wall = None

        if self.ceiling:
            self.ceiling.delete()
            self.ceiling = None

        self.objects_of_interest.clear()
        self.noise_objects.clear()
        self.lights.clear()

    @staticmethod
    def render():
        data = bproc.renderer.render()
        data.update(bproc.renderer.render_segmap(map_by=["instance", "class", "name"]))
        return data
