from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Iterable
from typing import Set
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
class PointOnBody:
    point: geometry.Point
    body: Body


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
        for point, color in parallel(self._get_colored_points, points, num_processes=6):
            _draw(color, image, point)
        image.show()

    def _get_colored_points(
        self, points: List[geometry.Point]
    ) -> List[Tuple[geometry.Point, Color]]:
        result = []
        for point in points:
            result.append((point, self._get_color(point)))
        return result

    def _get_color(self, point: geometry.Point) -> Color:
        ray = geometry.make_ray(self.camera, point)
        return self._get_color_from_ray(ray, set(), 0)

    def _get_color_from_ray(
        self, ray: geometry.Ray, excluded_body_ids: Set[int], depth: int
    ) -> Color:
        if depth == 5:
            return self._sky_color
        points_on_bodies = self._get_points_on_bodies(ray, excluded_body_ids)
        if points_on_bodies:
            point_on_body = _closest(points_on_bodies, ray.point)
            p = point_on_body.point
            body = point_on_body.body
            if isinstance(body.material, Mirror):
                # TODO: catch exception from ray.mirror here
                return self._get_color_from_ray(
                    ray.mirror(body.shape.perpendicular(p)), {id(body)}, depth + 1
                )
            return body.material.get_color(p) * self._lightning_coeff(p)
        return self._sky_color

    def _get_points_on_bodies(self, ray, excluded_body_ids):
        points_on_bodies = []
        for body in self._iter_bodies(excluded_body_ids):
            for p in body.shape.intersections(ray):
                points_on_bodies.append(PointOnBody(p, body))
        return points_on_bodies

    def _iter_bodies(self, excluded_ids: Set[int]) -> Iterable[Body]:
        return (body for body in self if id(body) not in excluded_ids)

    @property
    def _sky_color(self):
        return Color(26, 108, 171)

    def _lightning_coeff(self, point: geometry.Point) -> float:
        coeffs = []
        for light in self.lights:
            if self._in_the_shadow(point, light):
                coeffs.append(_get_shadow_lightning_coeff())
            else:
                coeffs.append(_get_exposed_lightning_coeff(point, light))

        return max(coeffs, default=1)

    def _in_the_shadow(self, point: geometry.Point, light: geometry.Point) -> bool:
        segment = geometry.make_line_segment(point, light)
        for body in self:
            for intersection in body.shape.intersections(segment):
                if not _close_points(intersection, point):
                    return True
        return False

    def _points_on_screen(self) -> List[geometry.Point]:
        return [
            geometry.make_point(x, y, 0)
            for x in range(0, self.width)
            for y in range(0, self.height)
        ]


def _draw(color: Color, image: Image, point: geometry.Point) -> None:
    x = int(geometry.get_x(point))
    y = int(geometry.get_y(point))
    image.set_pixel(x, y, color)


def _close_points(a: geometry.Point, b: geometry.Point):
    return math.isclose(np.linalg.norm(b - a), 0, abs_tol=1e-3)


def _get_exposed_lightning_coeff(point: geometry.Point, light: geometry.Point) -> float:
    d = np.linalg.norm(light - point)
    min_distance_to_dim = 800
    if d >= min_distance_to_dim:
        return min_distance_to_dim / d
    return 1


def _get_shadow_lightning_coeff() -> float:
    return 0.5


def _closest(points_on_bodies: List[PointOnBody], point: geometry.Point) -> PointOnBody:
    assert points_on_bodies
    return min(points_on_bodies, key=lambda pb: np.linalg.norm(pb.point - point),)
