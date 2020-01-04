from __future__ import annotations

import abc
import dataclasses
from typing import List

import numpy as np

from . import algebra

Point = np.ndarray


def from_xyz(x: float, y: float, z: float) -> Point:
    return np.array((x, y, z), dtype=np.float)


def get_x(point: Point) -> float:
    return point[0]


def get_y(point: Point) -> float:
    return point[1]


def get_z(point: Point) -> float:
    return point[2]


@dataclasses.dataclass(frozen=True)
class Ray:
    start: Point
    direction: Point

    @staticmethod
    def from_points(start: Point, after_start: Point) -> Ray:
        assert not np.array_equal(start, after_start)
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


@dataclasses.dataclass
class Plane(Figure):
    a: float
    b: float
    c: float
    d: float

    def __post_init__(self):
        self.coeff_vec = from_xyz(self.a, self.b, self.c)

    def intersect(self, ray: Ray, max_k=None) -> List[Point]:
        denominator = self.coeff_vec @ ray.direction
        if denominator == 0:
            return []
        k = -((self.coeff_vec @ ray.start) + self.d) / denominator
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
            return Ray.from_points(
                point, from_xyz(get_x(point) + 1, get_y(point), get_z(point))
            )
        if self.b != 0:
            return Ray.from_points(
                point, from_xyz(get_x(point), get_y(point) + 1, get_z(point))
            )
        if self.c != 0:
            return Ray.from_points(
                point, from_xyz(get_x(point), get_y(point), get_z(point) + 1)
            )
        raise ValueError(f"only simple planes are supported: {self!r}")


@dataclasses.dataclass(frozen=True)
class Sphere(Figure):
    center: Point
    radius: float

    def intersect(self, ray: Ray, max_k=None) -> List[Point]:
        v = ray.start - self.center
        a = ray.direction @ ray.direction
        b = 2 * (v @ ray.direction)
        c = (v @ v) - self.radius ** 2
        return [
            ray.start + ray.direction * k
            for k in algebra.solve_quadratic(a, b, c)
            if k >= 0 and (max_k is None or k < max_k)
        ]

    def perpendicular(self, point: Point) -> Ray:
        return Ray.from_points(self.center, point)
