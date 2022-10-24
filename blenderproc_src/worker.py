import blenderproc as bproc
import os
import sys
import numpy as np
from numpy.random import choice, randint
from dotenv import load_dotenv
from pathlib import Path


src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(src_dir)


from blenderproc_src.render import RenderManager
from blenderproc_src.random import CameraDiskSampler, CameraPartSphereSampler, LightRandomizer, RandomCubeGenerator, StackRandomizer, RandomObjGenerator


bproc.init()
load_dotenv()

GENERAL_TEXTURES_PATH = os.getenv("GENERAL_TEXTURES_PATH")
BOX_TEXTURES_PATH = os.getenv("BOX_TEXTURES_PATH")
OBJECTS_PATH = os.getenv("OBJECTS_PATH")
HDRI_PATH = os.getenv("HDRI_PATH")
NOISE_OBJECTS_PATH = os.getenv("NOISE_OBJECTS_PATH")


def main() -> None:
    general_textures = list(Path(GENERAL_TEXTURES_PATH).absolute().rglob("*.jpg"))
    box_textures = list(Path(BOX_TEXTURES_PATH).absolute().rglob("*"))
    objects_paths = list(Path(OBJECTS_PATH).absolute().rglob("*.obj"))

    render_manager = RenderManager()
    render_manager.set_floor(textures=general_textures, scale=(60, 60, 1))
    render_manager.set_random_hdri_background(HDRI_PATH)

    random_obj_generator = RandomObjGenerator(
        rotation_range=(np.array([0, 0, 0]), np.array([0, 0, 2 * np.pi])),
        scale_range=(np.array([15, 15, 15]), np.array([23, 23, 20.5])),
        obj_files_paths=objects_paths,
        textures=box_textures
    )

    stack_randomizer = StackRandomizer(obj_generators=[random_obj_generator], no_of_objs_range=(2, 5), no_of_stack_range=(1, 3), surface=render_manager.floor, location_range=((-10, -10, 0), (10, 10, 0)))
    camera_randomizers = [
        CameraDiskSampler(center_range=((-0.5, -0.5, 1.5), (0.5, 0.5, 5)), radius_range=(45, 60)),
        CameraPartSphereSampler(center_range=((-1, -1, 1.5), (1, 1, 5)), part_sphere_vector_range=((0, 0, 1), (0, 0, 1)), radius_range=(45, 60), distance_above_center_range=(0, 1))
    ]
    light_randomizer = LightRandomizer(location_range=((-5, -5, 3), (5, 5, 10)), energy_range=(5, 30), color_range=((15, 15, 15), (200, 200, 200)), falloff_distance_range=(0.5, 1), no_lights_range=(1, 4))

    render_manager.add_random_noise_objects(noise_objects_path=NOISE_OBJECTS_PATH, location_range=((-20, -20, 0), (20, 20, 0)), rotation_range=((0, 0, 0), (0, 0, 2 * np.pi)), scale_range=((17, 17, 17), (20, 20, 20)), objects_num=randint(4, 10))
    render_manager.compose_scene(camera_randomizer=choice(camera_randomizers), light_randomizer=light_randomizer, stack_randomizer=stack_randomizer, images_per_scene=4)

    data = render_manager.render()
    bproc.writer.write_coco_annotations(
        "test",
        instance_segmaps=data["instance_segmaps"],
        instance_attribute_maps=data["instance_attribute_maps"],
        colors=data["colors"],
        color_file_format="JPEG"
    )

    render_manager.clear_scene()


if __name__ == "__main__":
    main()
