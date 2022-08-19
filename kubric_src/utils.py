import json
import kubric as kb
import numpy as np
from random import choice
from typing import Optional, List, Dict

from policy import ModelPolicy
from consts import (
    CATEGORY,
    HOUSEHOLD_ITEMS,
    VEHICLES,
    BACKGROUNDS_TYPE,
    BACKGROUND_MAPPING,
    DEFAULT_SCALE,
    DEFAULT_SPAWN_REGION,
    DEFAULT_ROTATION,
    DEFAULT_CAMERA_LOOK_AT_NOISE,
    DEFAULT_ADDITIONAL_OBJECTS_NUM,
)
from exceptions import PolicyValidationError
from type import Range


def _create_policy(policy: Dict[str, any]) -> ModelPolicy:
    """
    Load policy to ModelPolicy object
    :param policy(Dict[str, any]) - policy dictionary representation
    :return: ModelPolicy
    """
    category = policy.get("category", None)
    if not category or category not in CATEGORY:
        raise PolicyValidationError(f"Category is invalid or missing: {category}")

    allowed_backgrounds = policy.get("allowed_backgrounds", None)
    if not allowed_backgrounds or any(
        [background not in BACKGROUNDS_TYPE for background in allowed_backgrounds]
    ):
        raise PolicyValidationError(
            f"Missing or invalid allowed_backgrounds for category: {category}"
        )

    camera_position_sphere_radius = policy.get("camera_position_sphere_radius", None)
    if not camera_position_sphere_radius:
        raise PolicyValidationError(
            f"Camera position sphere radius is missing for category: {category}"
        )

    rotation = policy.get("rotation", DEFAULT_ROTATION)
    spawn_region = policy.get("spawn_region", DEFAULT_SPAWN_REGION)
    scale = policy.get("scale", DEFAULT_SCALE)
    camera_look_at_noise = policy.get(
        "camera_look_at_noise", DEFAULT_CAMERA_LOOK_AT_NOISE
    )
    additional_objects_num = policy.get(
        "additional_objects_num", DEFAULT_ADDITIONAL_OBJECTS_NUM
    )

    return ModelPolicy(
        category=category,
        allowed_backgrounds=allowed_backgrounds,
        rotation=rotation,
        spawn_region=spawn_region,
        scale=Range(*scale),
        camera_position_sphere_radius=camera_position_sphere_radius,
        camera_look_at_noise=camera_look_at_noise,
        additional_objects_num=additional_objects_num,
    )


def load_policies(policy_file_path: str) -> List[ModelPolicy]:
    """
    Parse model polices from file
    :param policy_file_path: path to file with policies
    :return: list of policy models
    """
    with open(policy_file_path) as f:
        policies = json.load(f)
        return [_create_policy(policy) for policy in policies]


def draw_category(category: Optional[str] = None) -> str:
    """
    Draw category
    :param category: optional parameter, useful when we want to draw category matching given category
    :return: category
    """

    if not category:
        return choice(CATEGORY)

    if category in HOUSEHOLD_ITEMS:
        return choice(HOUSEHOLD_ITEMS)

    if category in VEHICLES:
        return choice(VEHICLES)

    return category


def draw_background(allowed_backgrounds: List[str]) -> str:
    """
    Draw background image
    :param allowed_backgrounds: list of allowed backgrounds types
    :return: background id
    """
    return choice(
        choice(
            [
                BACKGROUND_MAPPING[background_type]
                for background_type in allowed_backgrounds
            ]
        )
    )


def compute_bboxes(segmentation: np.ndarray, assets: List[kb.core.Asset]) -> None:
    """
    Adds asset bounding box to its metadata based on given segmentation array
    :param segmentation: image segmentation array
    :param assets: list of asset visible on image
    :return:
    """
    for k, asset in enumerate(assets, start=1):
        seg = segmentation.copy()
        idxs = np.array(np.where(seg == k), dtype=np.float32)
        if idxs.size > 0:
            x = float(idxs[1].min() / seg.shape[1])
            y = float(idxs[0].min() / seg.shape[0])
            width = float((idxs[1].max() + 1) / seg.shape[1]) - x
            height = float((idxs[0].max() + 1) / seg.shape[0]) - y
            asset.metadata["bbox"] = (x, y, width, height)


def get_instance_info(
    assets_subset: List[kb.core.Asset], data_keys: List[str]
) -> List[Dict[str, any]]:
    """
    Returns information about given asset subset based on provided data keys
    :param assets_subset: list of asset objects
    :param data_keys: metadata keys
    :return: dictionary with instance data
    """
    return [
        {key: instance.metadata[key] for key in data_keys} for instance in assets_subset
    ]
