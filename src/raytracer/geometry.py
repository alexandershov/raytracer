from __future__ import annotations

import abc
import dataclasses
import math
from typing import List

from . import algebra


@dataclasses.dataclass(frozen=True)
class Point:
    x: float
    y: float
    z: float

    def __sub__(self, other) -> Vector:
        if not isinstance(other, Point):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)


@dataclasses.dataclass(frozen=True)
class Vector:
    x: float
    y: float
    z: float

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


@dataclasses.dataclass(frozen=True)
class Ray:
    start: Point
    direction: Vector

    @staticmethod
    def from_points(start: Point, after_start: Point) -> Ray:
        assert start != after_start
        return Ray(start, after_start - start)

    def intersect(self, figure: Figure, max_k=None) -> List[Point]:
        return figure.intersect(self, max_k=max_k)


class Figure:
    @abc.abstractmethod
    def intersect(self, ray: Ray, max_k=None) -> List[Point]:
        raise NotImplemented


@dataclasses.dataclass(frozen=True)
class Plane(Figure):
    a: float
    b: float
    c: float
    d: float

    def intersect(self, ray: Ray, max_k=None) -> List[Point]:
        x0 = ray.start.x
        y0 = ray.start.y
        z0 = ray.start.z
        dx = ray.direction.x
        dy = ray.direction.y
        dz = ray.direction.z
        denominator = self.a * dx + self.b * dy + self.c * dz
        if denominator == 0:
            return []
        k = -(self.a * x0 + self.b * y0 + self.c * z0 + self.d) / denominator
        if k < 0:
            return []
        if max_k is not None and k > max_k:
            return []
        return [
            Point(
                ray.start.x + k * ray.direction.x,
                ray.start.y + k * ray.direction.y,
                ray.start.z + k * ray.direction.z,
            )
        ]


@dataclasses.dataclass(frozen=True)
class Sphere(Figure):
    center: Point
    radius: float

    def intersect(self, ray: Ray, max_k=None) -> List[Point]:
        x1 = ray.start.x - self.center.x
        y1 = ray.start.y - self.center.y
        z1 = ray.start.z - self.center.z
        a = ray.direction.x ** 2 + ray.direction.y ** 2 + ray.direction.z ** 2
        b = 2 * (x1 * ray.direction.x + y1 * ray.direction.y + z1 * ray.direction.z)
        c = x1 ** 2 + y1 ** 2 + z1 ** 2 - self.radius ** 2
        return [
            Point(
                ray.start.x + k * ray.direction.x,
                ray.start.y + k * ray.direction.y,
                ray.start.z + k * ray.direction.z,
            )
            for k in algebra.solve_quadratic(a, b, c)
            if k >= 0 and (max_k is None or k < max_k)
        ]
