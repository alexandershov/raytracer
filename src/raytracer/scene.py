from __future__ import annotations

import dataclasses
import time
from typing import List, Iterable, Callable

from . import geometry

from . import image


class Material:
    def get_color(self, point: geometry.Point) -> image.Color:
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class Solid(Material):
    color: image.Color

    def get_color(self, point: geometry.Point) -> image.Color:
        return self.color


@dataclasses.dataclass(frozen=True)
class Squared(Material):
    width: float
    white: image.Color
    black: image.Color
    projection: Callable

    @staticmethod
    def project_to_local_xy(point: geometry.Point) -> geometry.Point:
        return geometry.Point(point.x, point.y, 0)

    @staticmethod
    def project_to_local_xz(point: geometry.Point) -> geometry.Point:
        return geometry.Point(point.x, point.z, 0)

    @staticmethod
    def project_to_local_yz(point: geometry.Point) -> geometry.Point:
        return geometry.Point(point.y, point.z, 0)

    def get_color(self, point: geometry.Point) -> image.Color:
        local = self.projection(point)
        score = int(local.x // self.width) + int(local.y // self.width)
        if not score % 2:
            return self.white
        return self.black


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
    lights: List[geometry.Point]
    things: List[Thing]

    def __iter__(self):
        return iter(self.things)

    def render(self):
        started_at = time.time()
        img = image.PillowImage(self.width, self.height)
        for point in self._iter_screen():
            color = image.Color(26, 108, 171)
            ray = geometry.Ray.from_points(self.camera, point)
            excluded_things = set()
            for _ in range(5):
                intersections = []
                for thing in self:
                    if thing in excluded_things:
                        continue
                    for p in ray.intersect(thing.figure):
                        intersections.append((p, thing))
                if intersections:
                    p, thing = min(
                        intersections, key=lambda p_thing: abs(p_thing[0] - ray.start)
                    )
                    if isinstance(thing.material, Mirror):
                        ray = ray.mirror(thing.figure.perpendicular(p))
                        excluded_things = {thing}
                        continue
                    color = thing.material.get_color(p) * self._lightning_coeff(p)
                break
            img.set_pixel(point.x, self.height - 1 - point.y, color)
        duration = time.time() - started_at
        print(f"rendering took {duration:.3f} seconds")
        img.show()

    def _lightning_coeff(self, p: geometry.Point) -> float:
        coeffs = []
        for light in self.lights:
            in_the_shadow = False
            ray = geometry.Ray.from_points(p, light)
            for thing in self:
                for intersect in ray.intersect(thing.figure, max_k=1):
                    if abs(intersect - p) > 1:
                        in_the_shadow = True
            if in_the_shadow:
                coeffs.append(0.5)
                continue
            d = abs(light - p)
            cutoff = 800
            if d > cutoff:
                coeffs.append(cutoff / d)
            else:
                coeffs.append(1)
        if not coeffs:
            return 1
        return max(coeffs)

    def _iter_screen(self) -> Iterable[geometry.Point]:
        return (
            geometry.Point(x, y, 0)
            for x in range(0, self.width)
            for y in range(0, self.height)
        )
