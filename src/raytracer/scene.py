from __future__ import annotations

import dataclasses
import time
from typing import List, Iterable

from . import geometry

from . import image


class Material:
    def get_color(self) -> image.Color:
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class Solid(Material):
    color: image.Color

    def get_color(self) -> image.Color:
        return self.color


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
        started_at = time.time()
        img = image.PillowImage(self.width, self.height)
        for point in self._iter_screen():
            ray = geometry.Ray.from_points(self.camera, point)
            intersections = []
            for thing in self:
                for p in ray.intersect(thing.figure):
                    intersections.append((p, thing))
            if intersections:
                _, thing = min(
                    intersections, key=lambda p_thing: abs(p_thing[0] - self.camera)
                )
                img.set_pixel(
                    point.x, self.height - 1 - point.y, thing.material.get_color()
                )
            else:
                img.set_pixel(
                    point.x, self.height - 1 - point.y, image.Color(0, 0, 255)
                )
        duration = time.time() - started_at
        print(f"render took {duration:.3f} seconds")
        img.show()

    def _iter_screen(self) -> Iterable[geometry.Point]:
        return (
            geometry.Point(x, y, 0)
            for x in range(0, self.width)
            for y in range(0, self.height)
        )
