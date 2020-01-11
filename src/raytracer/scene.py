from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List
from typing import Tuple

import numpy as np

from raytracer import geometry
from raytracer import performance
from raytracer.color import Color
from raytracer.image import Image
from raytracer.material import Material
from raytracer.material import Mirror
from raytracer.performance import parallel


@dataclass(frozen=True)
class Body:
    shape: geometry.Shape
    material: Material


@dataclass(frozen=True)
class Scene:
    bodies: List[Body]

    camera: geometry.Point
    lights: List[geometry.Point]

    width: int
    height: int

    def __iter__(self):
        return iter(self.bodies)

    @performance.timed
    def render(self):
        image = Image(self.width, self.height)
        points = self._points_on_screen()
        for point, color in parallel(self._get_colors, points, num_processes=6):
            self._draw(color, image, point)
        image.show()

    def _get_colors(
        self, points: List[geometry.Point]
    ) -> List[Tuple[geometry.Point, Color]]:
        result = []
        for point in points:
            color = self._sky_color
            ray = geometry.make_ray(self.camera, point)
            excluded_ids = set()
            for _ in range(5):
                intersections = []
                for body in self:
                    if id(body) in excluded_ids:
                        continue
                    for p in body.shape.intersections(ray):
                        intersections.append((p, body))
                if intersections:
                    p, body = min(
                        intersections,
                        key=lambda p_body: np.linalg.norm(p_body[0] - ray.point),
                    )
                    if isinstance(body.material, Mirror):
                        # TODO: catch exception here
                        ray = ray.mirror(body.shape.perpendicular(p))
                        excluded_ids = {id(body)}
                        continue
                    color = body.material.get_color(p) * self._lightning_coeff(p)
                break
            result.append((point, color))
        return result

    @property
    def _sky_color(self):
        return Color(26, 108, 171)

    def _lightning_coeff(self, p: geometry.Point) -> float:
        coeffs = []
        for light in self.lights:
            in_the_shadow = False
            segment = geometry.make_line_segment(p, light)
            for body in self:
                for intersection in body.shape.intersections(segment):
                    if not _close_points(intersection, p):
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

    def _points_on_screen(self) -> List[geometry.Point]:
        return [
            geometry.make_point(x, y, 0)
            for x in range(0, self.width)
            for y in range(0, self.height)
        ]

    def _draw(self, color, image, point):
        x = int(geometry.get_x(point))
        y = int(geometry.get_y(point))
        image.set_pixel(x, y, color)


def _close_points(a: geometry.Point, b: geometry.Point):
    return math.isclose(np.linalg.norm(b - a), 0, abs_tol=1e-3)
