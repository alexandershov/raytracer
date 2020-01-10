from __future__ import annotations

import multiprocessing
import time
from dataclasses import dataclass
from typing import List, Callable, Tuple

import numpy as np

from raytracer.image import Image
from . import geometry
from .color import Color


class Material:
    def get_color(self, point: geometry.Point) -> Color:
        raise NotImplementedError


@dataclass(frozen=True)
class Solid(Material):
    color: Color

    def get_color(self, point: geometry.Point) -> Color:
        return self.color


@dataclass(frozen=True)
class Squared(Material):
    width: float
    white: Color
    black: Color
    projection: Callable

    @staticmethod
    def project_to_local_xy(point: geometry.Point) -> geometry.Point:
        return geometry.make_point(geometry.get_x(point), geometry.get_y(point), 0)

    @staticmethod
    def project_to_local_xz(point: geometry.Point) -> geometry.Point:
        return geometry.make_point(geometry.get_x(point), geometry.get_z(point), 0)

    @staticmethod
    def project_to_local_yz(point: geometry.Point) -> geometry.Point:
        return geometry.make_point(geometry.get_y(point), geometry.get_z(point), 0)

    def get_color(self, point: geometry.Point) -> Color:
        local = self.projection(point)
        score = int(geometry.get_x(local) // self.width) + int(
            geometry.get_y(local) // self.width
        )
        if not score % 2:
            return self.white
        return self.black


class Mirror(Material):
    def get_color(self, point: geometry.Point) -> Color:
        raise NotImplemented("should never be called")


@dataclass(frozen=True)
class Thing:
    figure: geometry.Figure
    material: Material


@dataclass(frozen=True)
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
        img = Image(self.width, self.height)
        points = self._screen_points()
        num_processes = 6
        with multiprocessing.Pool(processes=num_processes) as pool:
            chunks = _get_chunks(points, num_processes)
            for colored in pool.map(self._get_colors, chunks):
                for point, color in colored:
                    img.set_pixel(
                        int(geometry.get_x(point)), int(geometry.get_y(point)), color
                    )
        duration = time.time() - started_at
        print(f"rendering took {duration:.3f} seconds")
        img.show()

    def _get_colors(
        self, points: List[geometry.Point]
    ) -> List[Tuple[geometry.Point, Color]]:
        result = []
        for point in points:
            color = Color(26, 108, 171)
            ray = geometry.make_ray(self.camera, point)
            excluded_ids = set()
            for _ in range(5):
                intersections = []
                for thing in self:
                    if id(thing) in excluded_ids:
                        continue
                    for p in thing.figure.intersections(ray):
                        intersections.append((p, thing))
                if intersections:
                    p, thing = min(
                        intersections,
                        key=lambda p_thing: np.linalg.norm(p_thing[0] - ray.point),
                    )
                    if isinstance(thing.material, Mirror):
                        ray = ray.mirror(thing.figure.perpendicular(p))
                        excluded_ids = {id(thing)}
                        continue
                    color = thing.material.get_color(p) * self._lightning_coeff(p)
                break
            result.append((point, color))
        return result

    def _lightning_coeff(self, p: geometry.Point) -> float:
        coeffs = []
        for light in self.lights:
            in_the_shadow = False
            segment = geometry.make_line_segment(p, light)
            for thing in self:
                for intersections in thing.figure.intersections(segment):
                    if np.linalg.norm(intersections - p) > 1:
                        in_the_shadow = True
            if in_the_shadow:
                coeffs.append(0.5)
                continue
            d = np.linalg.norm(light - p)
            cutoff = 800
            if d > cutoff:
                coeffs.append(cutoff / d)
            else:
                coeffs.append(1)
        if not coeffs:
            return 1
        return max(coeffs)

    def _screen_points(self) -> List[geometry.Point]:
        return [
            geometry.make_point(x, y, 0)
            for x in range(0, self.width)
            for y in range(0, self.height)
        ]


def _get_chunks(seq: list, n: int) -> List[list]:
    chunks = []
    for i in range(n):
        chunks.append(seq[i::n])
    return chunks
