import logging
import string

import bpy
import kubric as kb
import numpy as np
from kubric.renderer.blender import Blender as KubricRenderer
from kubric.simulator import PyBullet
from random import choice, randint, sample
from typing import Tuple, List, Dict
from argparse import ArgumentParser

from consts import KUBASIC_URI, HDRI_HAVEN_URI, SHAPENET_URI, IMAGE_SHAPE, CATEGORY
from utils import (
    load_policies,
    draw_category,
    draw_background,
    compute_bboxes,
    get_instance_info,
)
from policy import ModelPolicy


def _load_asset_sources() -> Tuple[kb.AssetSource, kb.AssetSource, kb.AssetSource]:
    """
    Loads asset sources
    :return: kubasic, shapenet and hdri asset sources
    """
    kubasic = kb.AssetSource.from_manifest(KUBASIC_URI)
    shapenet = kb.AssetSource.from_manifest(SHAPENET_URI)
    hdri = kb.AssetSource.from_manifest(HDRI_HAVEN_URI)

    return kubasic, shapenet, hdri


def _get_random_model_asset(category: str, asset_provider: kb.AssetSource) -> str:
    """
    Returns random asset from given category
    :param category: asset category
    :param asset_provider: the source from which the asset is taken
    :return: asset id
    """
    return choice(
        [
            asset_id
            for asset_id, spec in asset_provider._assets.items()
            if spec["metadata"]["category"] == category.replace("_", " ")
        ]
    )


def _create_model_obj(
    category: str, asset_provider: kb.AssetSource, policy: ModelPolicy
) -> kb.core.Asset:
    """
    Creates asset model object
    :param category: category of asset
    :param asset_provider: the source from which the asset is taken
    :param policy: model policy
    :return: asset 3D object
    """
    model_asset = _get_random_model_asset(category, asset_provider)
    model = asset_provider.create(asset_id=model_asset)
    model.quaternion = policy.random_rotation
    scale = policy.random_scale
    model.scale = scale / np.max(model.bounds[1] - model.bounds[0])
    model.metadata["scale"] = scale
    model.metadata["is_dynamic"] = False
    model.friction = 1
    model.restitution = 0

    return model


def _create_camera(model: kb.core.Asset, policy: ModelPolicy) -> kb.PerspectiveCamera:
    """
    Creates camera object
    :param model: the model to which the camera is to be pointed
    :param policy: model policy
    :return: camera object
    """
    camera = kb.PerspectiveCamera()
    camera.position = kb.sample_point_in_half_sphere_shell(
        *policy.camera_position_sphere_radius
    )
    camera.look_at(model.position - np.random.uniform(*policy.camera_look_at_noise, 3))
    return camera


def _generate_image(
    kubasic: kb.AssetSource,
    shapenet: kb.AssetSource,
    hdri: kb.AssetSource,
    policies: List[ModelPolicy],
) -> Tuple[Dict[str, np.ndarray], List[kb.Asset]]:
    """
    The core methods, generate image with random objects and random background
    :param kubasic: kubasic asset provider
    :param shapenet: shapenet asset provider
    :param hdri: hdri asset provider
    :param policies: list of model policies
    :return: image frame, visible objects on this frame
    """
    scene = kb.Scene(resolution=IMAGE_SHAPE)
    simulator = PyBullet(scene)
    renderer = KubricRenderer(scene)
    category = draw_category()
    model_policy = next(filter(lambda m: m.category == category, policies))
    background = draw_background(model_policy.allowed_backgrounds)
    background_hdri = hdri.create(asset_id=background)

    scene.metadata["background"] = background
    renderer._set_ambient_light_hdri(background_hdri.filename)

    dome = kubasic.create(
        asset_id="dome",
        name="dome",
        friction=1.0,
        restitution=0.0,
        static=True,
        background=True,
    )
    scene.add(dome)

    dome_blender = dome.linked_objects[renderer]
    texture_node = dome_blender.data.materials[0].node_tree.nodes["Image Texture"]
    texture_node.image = bpy.data.images.load(background_hdri.filename)

    model = _create_model_obj(category, shapenet, model_policy)
    scene.add(model)
    kb.resample_while(
        model, [kb.position_sampler(model_policy.spawn_region)], simulator.check_overlap
    )

    for _ in range(randint(0, model_policy.additional_objects_num)):
        obj_cat = draw_category(category)
        obj_policy = next(filter(lambda m: m.category == obj_cat, policies))
        obj_model = _create_model_obj(obj_cat, shapenet, obj_policy)
        scene.add(obj_model)
        try:
            kb.resample_while(
                obj_model,
                [kb.position_sampler(obj_policy.spawn_region)],
                simulator.check_overlap,
            )
        except RuntimeError:
            continue

    camera = _create_camera(model, model_policy)
    scene.add(camera)

    if not category == CATEGORY.airplane:
        _, _ = simulator.run(frame_start=-100, frame_end=0)

    frame = renderer.render_still()

    kb.compute_visibility(frame["segmentation"], scene.assets)
    visible_assets = [
        asset
        for asset in scene.foreground_assets
        if np.max(asset.metadata["visibility"]) > 0
    ]
    visible_assets = sorted(
        visible_assets, key=lambda asset: np.sum(asset.metadata["visibility"])
    )

    frame["segmentation"] = kb.adjust_segmentation_idxs(
        frame["segmentation"], scene.assets, visible_assets
    )
    compute_bboxes(frame["segmentation"], visible_assets)

    return frame, visible_assets


def main(series: str, output_dir: str, iteration: int) -> None:
    kubasic, shapenet, hdri = _load_asset_sources()
    policies = load_policies("policies.json")

    logging.info(f"Series: {series}, iteration: {iteration}")
    frame, visible_assets = _generate_image(kubasic, shapenet, hdri, policies)
    kb.write_png(frame["rgba"], f"{output_dir}/images/{series}_{iteration}.png")

    image_data = {"resolution": IMAGE_SHAPE, "file_name": f"{series}_{iteration}.png"}
    kb.file_io.write_json(
        filename=f"{output_dir}/annotations/{series}_{iteration}.json",
        data={
            "objects": get_instance_info(
                visible_assets, data_keys=["bbox", "category", "visibility"]
            ),
            "image": image_data,
        },
    )
    kb.done()


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    parser = ArgumentParser()
    parser.add_argument(
        "-s", "--series", type=str, default="".join(sample(string.ascii_lowercase, 16))
    )
    parser.add_argument("-o", "--output_dir", type=str)
    parser.add_argument("-i", "--iteration", type=int)
    args = parser.parse_args()
    main(args.series, args.output_dir, args.iteration)
