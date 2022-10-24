import blenderproc as bproc
import numpy as np
from numpy.random import choice, randint, uniform
from random import sample
from string import ascii_lowercase
from typing import List

from blenderproc_src.random.types import Range


class LightRandomizer:
    def __init__(self, location_range: Range, energy_range: Range, color_range: Range, falloff_distance_range: Range, no_lights_range: Range):
        self.location_range = location_range
        self.energy_range = energy_range
        self.color_range = color_range
        self.falloff_distance_range = falloff_distance_range
        self.no_lights_range = no_lights_range

    def create_single_light(self) -> bproc.types.Light:
        light = bproc.types.Light(type=choice(["POINT", "AREA"]), name=f"light{''.join(sample(ascii_lowercase, 4))}")
        light.set_location(uniform(*self.location_range))
        light.set_energy(uniform(*self.energy_range))
        light.set_color(uniform(*self.color_range))
        light.set_distance(uniform(*self.falloff_distance_range))
        return light

    def __call__(self) -> List[bproc.types.Light]:
        return [self.create_single_light() for _ in range(randint(*self.no_lights_range))]
