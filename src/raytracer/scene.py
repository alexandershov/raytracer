from __future__ import annotations

import dataclasses
from typing import List

from . import geometry

from . import image


class Material:
    pass


@dataclasses.dataclass(frozen=True)
class Solid(Material):
    color: image.Color


class Mirror(Material):
    pass


@dataclasses.dataclass(frozen=True)
class Thing:
    figure: geometry.Figure
    material: Material


class Scene:
    def __init__(self, things: List[Thing]):
        self._things = things

    def __iter__(self):
        return iter(self._things)
