from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import List

import numpy as np

from . import algebra

Point = np.ndarray


def make_point(x: float, y: float, z: float) -> Point:
    return np.array((x, y, z))


def get_x(point: Point) -> float:
    return point[0]


def get_y(point: Point) -> float:
    return point[1]


def get_z(point: Point) -> float:
    return point[2]


def make_ray(start: Point, to: Point) -> Line:
    return Line.from_points(start, to)


@dataclass(frozen=True)
class Line:
    point: Point
    direction: Point

    @staticmethod
    def from_points(start: Point, to: Point) -> Line:
        assert not np.array_equal(start, to)
        return Line(start, to - start)

    def intersect(self, figure: Figure, max_k=None) -> List[Point]:
        return figure.intersect(self, max_k=max_k)

    def perpendicular(self, other: Line) -> Line:
        k = (other.direction @ (self.point - other.point)) / (
            other.direction @ other.direction
        )
        p = other.point + other.direction * k
        return make_ray(self.point, p)

    def mirror(self, axis: Line) -> Line:
        perpendicular = self.perpendicular(axis)
        return make_ray(
            axis.point,
            perpendicular.point + perpendicular.direction + perpendicular.direction,
        )


class Figure(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def intersect(self, ray: Line, max_k=None) -> List[Point]:
        raise NotImplemented

    @abc.abstractmethod
    def perpendicular(self, point: Point) -> Line:
        raise NotImplementedError


@dataclass
class Plane(Figure):
    a: float
    b: float
    c: float
    d: float

    def __post_init__(self):
        self.coeff_vec = make_point(self.a, self.b, self.c)

    def intersect(self, ray: Line, max_k=None) -> List[Point]:
        denominator = self.coeff_vec @ ray.direction
        if denominator == 0:
            return []
        k = -((self.coeff_vec @ ray.point) + self.d) / denominator
        if k < 0:
            return []
        if max_k is not None and k > max_k:
            return []
        return [ray.point + ray.direction * k]

    def perpendicular(self, point: Point) -> Line:
        assert [self.a, self.b, self.c].count(
            0
        ) == 2, "only simple planes are supported"
        if self.a != 0:
            return make_ray(
                point, make_point(get_x(point) + 1, get_y(point), get_z(point))
            )
        if self.b != 0:
            return make_ray(
                point, make_point(get_x(point), get_y(point) + 1, get_z(point))
            )
        if self.c != 0:
            return make_ray(
                point, make_point(get_x(point), get_y(point), get_z(point) + 1)
            )
        raise ValueError(f"only simple planes are supported: {self!r}")


@dataclass(frozen=True)
class Sphere(Figure):
    center: Point
    radius: float

    def intersect(self, ray: Line, max_k=None) -> List[Point]:
        v = ray.point - self.center
        a = ray.direction @ ray.direction
        b = 2 * (v @ ray.direction)
        c = (v @ v) - self.radius ** 2
        return [
            ray.point + ray.direction * k
            for k in algebra.solve_quadratic(a, b, c)
            if k >= 0 and (max_k is None or k < max_k)
        ]

    def perpendicular(self, point: Point) -> Line:
        return make_ray(self.center, point)
