from __future__ import annotations

import dataclasses
from typing import List, Iterable

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


@dataclasses.dataclass(frozen=True)
class Scene:
    width: int
    height: int
    camera: geometry.Point
    things: List[Thing]

    def __iter__(self):
        return iter(self.things)

    def render(self):
        img = image.PillowImage(self.width, self.height)
        for point in self._iter_screen():
            ray = geometry.Ray.from_points(self.camera, point)
        img.show()

    def _iter_screen(self) -> Iterable[geometry.Point]:
        return (
            geometry.Point(x, y, 0)
            for x in range(0, self.width)
            for y in range(0, self.height)
        )
