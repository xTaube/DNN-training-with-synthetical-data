import OpenEXR
import numpy as np
import Imath

FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)


def convert_exr_to_rgb_array(filepath: str) -> np.ndarray:
    file = OpenEXR.InputFile(filepath)
    dw = file.header()['dataWindow']
    width, height = dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1
    rgb = [np.frombuffer(file.channel(channel, FLOAT), dtype=np.float32) for channel in ("R", "G", "B")]
    return np.reshape(np.dstack(rgb), (height, width, 3))


def convert_exr_to_segmentation_array(filepath: str) -> np.ndarray:
    file = OpenEXR.InputFile(filepath)
    dw = file.header()['dataWindow']
    width, height = dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1
    r = np.frombuffer(file.channel("R", FLOAT), dtype=np.float32)
    return np.reshape(r, (height, width)).astype(np.uint8)
