import blenderproc as bproc
import os
import sys
import numpy as np
from numpy.random import choice
from dotenv import load_dotenv
from pathlib import Path


src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(src_dir)


from blenderproc_src.render import RenderManager
from blenderproc_src.random import (
    CameraDiskSampler,
    StackRandomizer,
    RandomObjGenerator,
    FlyingDistractorGenerator,
)


bproc.init()
load_dotenv()

BOX_TEXTURES_PATH = os.getenv("BOX_TEXTURES_PATH")
NOISE_OBJECTS_PATH = os.getenv("NOISE_OBJECT_PATH")
BOX_PATH = os.getenv("BOX_PATH")
HDRI_PATH = os.getenv("HDRI_PATH")


def main() -> None:
    box_textures = list(Path(BOX_TEXTURES_PATH).absolute().rglob("*"))
    objects_paths = list(Path(BOX_PATH).absolute().rglob("*.obj"))

    render_manager = RenderManager()
    render_manager.set_random_hdri_background(HDRI_PATH)

    random_obj_generator = RandomObjGenerator(
        rotation_range=(np.array([0, 0, 0]), np.array([0, 0, 2 * np.pi])),
        scale_range=(np.array([15, 15, 15]), np.array([23, 23, 20.5])),
        obj_files_paths=objects_paths,
        textures=box_textures,
    )

    fd_generator = FlyingDistractorGenerator(
        rotation_range=((0, 0, 0), (2 * np.pi, 2 * np.pi, 2 * np.pi)),
        scale_range=(0.7, 2),
        location_range=((-20, -20, -5), (20, 20, 25)),
    )

    stack_randomizer = StackRandomizer(
        obj_generators=[random_obj_generator],
        no_of_objs_range=(2, 5),
        no_of_stack_range=(1, 3),
        rotation_range=((-np.pi / 8, -np.pi / 8, 0), (np.pi / 8, np.pi / 8, 0)),
        location_range=((-10, -10, -5), (10, 20, 5)),
    )
    camera_randomizers = [
        CameraDiskSampler(
            center_range=((-0.5, -0.5, 5), (0.5, 0.5, 20)), radius_range=(45, 65)
        ),
    ]

    render_manager.add_objects_of_interest(stack_randomizer)
    render_manager.add_random_noise_objects(
        noise_objects_path=NOISE_OBJECTS_PATH,
        location_range=((-15, -15, -5), (15, 15, 5)),
        rotation_range=((-np.pi / 8, -np.pi / 8, 0), (np.pi / 8, np.pi / 8, 2*np.pi)),
        scale_range=((17, 17, 17), (23, 23, 23)),
        objects_num=15
    )
    render_manager.compose_scene(
        camera_randomizer=choice(camera_randomizers),
        images_per_scene=1,
        camera_noise=((-2, -2, -2), (2, 2, 2))
    )

    data = render_manager.render()
    bproc.writer.write_coco_annotations(
        "output",
        instance_segmaps=data["instance_segmaps"],
        instance_attribute_maps=data["instance_attribute_maps"],
        colors=data["colors"],
        color_file_format="JPEG",
    )

    render_manager.clear_scene()


if __name__ == "__main__":
    main()
