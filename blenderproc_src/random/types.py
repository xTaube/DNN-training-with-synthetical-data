import numpy as np
from typing import Tuple, Union

Range = Union[Union[Tuple[float, ...], np.ndarray], Union[Tuple[Tuple[float, ...], Tuple[float, ...]], Tuple[np.ndarray, np.ndarray]]]
