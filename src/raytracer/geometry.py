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

    def __sub__(self, other) -> Point:
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other) -> Point:
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other) -> Point:
        if not isinstance(other, (int, float)):
            return NotImplemented
        return Point(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other) -> Point:
        if not isinstance(other, (int, float)):
            return NotImplemented
        return Point(self.x / other, self.y / other, self.z / other)

    def __matmul__(self, other) -> float:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __abs__(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


@dataclasses.dataclass(frozen=True)
class Ray:
    start: Point
    direction: Point

    @staticmethod
    def from_points(start: Point, after_start: Point) -> Ray:
        assert start != after_start
        return Ray(start, after_start - start)

    @property
    def not_start(self) -> Point:
        return self.start + self.direction

    def intersect(self, figure: Figure, max_k=None) -> List[Point]:
        return figure.intersect(self, max_k=max_k)

    def perpendicular(self, other: Ray) -> Ray:
        k = (other.direction @ (self.start - other.start)) / (
            other.direction @ other.direction
        )
        p = other.start + other.direction * k
        return Ray.from_points(self.start, p)

    def mirror(self, axis: Ray) -> Ray:
        perpendicular = self.perpendicular(axis)
        return Ray.from_points(
            axis.start,
            perpendicular.start + perpendicular.direction + perpendicular.direction,
        )


class Figure(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def intersect(self, ray: Ray, max_k=None) -> List[Point]:
        raise NotImplemented

    @abc.abstractmethod
    def perpendicular(self, point: Point) -> Ray:
        raise NotImplementedError


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
        return [ray.start + ray.direction * k]

    def perpendicular(self, point: Point) -> Ray:
        assert [self.a, self.b, self.c].count(
            0
        ) == 2, "only simple planes are supported"
        if self.a != 0:
            return Ray.from_points(point, Point(point.x + 1, point.y, point.z))
        if self.b != 0:
            return Ray.from_points(point, Point(point.x, point.y + 1, point.z))
        if self.c != 0:
            return Ray.from_points(point, Point(point.x, point.y, point.z + 1))
        raise ValueError(f"only simple planes are supported: {self!r}")


@dataclasses.dataclass(frozen=True)
class Sphere(Figure):
    center: Point
    radius: float

    def intersect(self, ray: Ray, max_k=None) -> List[Point]:
        v = ray.start - self.center
        f = ray.start - self.center
        x1 = ray.start.x - self.center.x
        y1 = ray.start.y - self.center.y
        z1 = ray.start.z - self.center.z
        a = ray.direction.x ** 2 + ray.direction.y ** 2 + ray.direction.z ** 2
        b = 2 * (x1 * ray.direction.x + y1 * ray.direction.y + z1 * ray.direction.z)
        c = (f @ f) - self.radius ** 2
        return [
            ray.start + ray.direction * k
            for k in algebra.solve_quadratic(a, b, c)
            if k >= 0 and (max_k is None or k < max_k)
        ]

    def perpendicular(self, point: Point) -> Ray:
        return Ray.from_points(self.center, point)
