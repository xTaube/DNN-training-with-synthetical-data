from src.render.blender.utils import convert_exr_to_rgb_array, convert_exr_to_segmentation_array


LAYER_MAP = {
    "RGB": convert_exr_to_rgb_array,
    "segmentation": convert_exr_to_segmentation_array
}

