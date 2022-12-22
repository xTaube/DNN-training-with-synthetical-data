import OpenEXR
import numpy as np
import Imath


FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)


def convert_exr_to_rgb_array(filepath: str) -> np.ndarray:
    file = OpenEXR.InputFile(filepath)
    dw = file.header()["dataWindow"]
    width, height = dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1
    rgb = [
        np.frombuffer(file.channel(channel, FLOAT), dtype=np.float32)
        for channel in ("R", "G", "B")
    ]
    merged_rgb = np.clip(np.dstack(rgb), 0, 1)

    # convert colour to sRGB https://en.wikipedia.org/wiki/SRGB#The_forward_transformation_(CIE_XYZ_to_sRGB)
    img = np.where(
        merged_rgb <= 0.0031308,
        12.92 * merged_rgb,
        1.055 * np.power(merged_rgb, 1 / 2.4) - 0.055,
    )
    return (np.reshape(img, (height, width, 3)) * 255).astype(np.uint8)


def convert_exr_to_segmentation_array(filepath: str) -> np.ndarray:
    file = OpenEXR.InputFile(filepath)
    dw = file.header()["dataWindow"]
    width, height = dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1
    r = np.frombuffer(file.channel("R", FLOAT), dtype=np.float32)
    return np.reshape(r, (height, width)).astype(np.uint8)


def str_direction_to_vector(direction: str) -> np.ndarray:
    return {
        "X": np.array([1.0, 0.0, 0.0], dtype=np.float32),
        "Y": np.array([0.0, 1.0, 0.0], dtype=np.float32),
        "Z": np.array([0.0, 0.0, 1.0], dtype=np.float32),
        "-X": np.array([-1.0, 0.0, 0.0], dtype=np.float32),
        "-Y": np.array([0.0, -1.0, 0.0], dtype=np.float32),
        "-Z": np.array([0.0, 0.0, -1.0], dtype=np.float32),
    }[direction.upper()]


def normalize(value: np.ndarray) -> np.ndarray:
    return np.divide(value, np.linalg.norm(value))
