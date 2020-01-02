from __future__ import annotations

import abc
import dataclasses
import math
from typing import List


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

    def intersect(self, figure: Intersectable) -> List[Point]:
        return figure.intersect(self)


class Intersectable:
    @abc.abstractmethod
    def intersect(self, ray: Ray) -> List[Point]:
        raise NotImplemented


@dataclasses.dataclass(frozen=True)
class Plane(Intersectable):
    a: float
    b: float
    c: float
    d: float

    def intersect(self, ray: Ray) -> List[Point]:
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
        return [
            Point(
                ray.start.x + k * ray.direction.x,
                ray.start.y + k * ray.direction.y,
                ray.start.z + k * ray.direction.z,
            )
        ]


@dataclasses.dataclass(frozen=True)
class Sphere:
    center: Point
    radius: float
