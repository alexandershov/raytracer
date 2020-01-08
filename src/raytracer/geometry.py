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


@dataclass(frozen=True)
class Ray:
    start: Point
    direction: Point

    @property
    def point(self) -> Point:
        return self.start

    @staticmethod
    def from_points(start: Point, after_start: Point) -> Ray:
        assert not np.array_equal(start, after_start)
        return Ray(start, after_start - start)

    def intersect(self, figure: Figure, max_k=None) -> List[Point]:
        return figure.intersect(self, max_k=max_k)

    def perpendicular(self, other: Ray) -> Ray:
        k = (other.direction @ (self.point - other.point)) / (
            other.direction @ other.direction
        )
        p = other.point + other.direction * k
        return Ray.from_points(self.point, p)

    def mirror(self, axis: Ray) -> Ray:
        perpendicular = self.perpendicular(axis)
        return Ray.from_points(
            axis.point,
            perpendicular.point + perpendicular.direction + perpendicular.direction,
        )


class Figure(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def intersect(self, ray: Ray, max_k=None) -> List[Point]:
        raise NotImplemented

    @abc.abstractmethod
    def perpendicular(self, point: Point) -> Ray:
        raise NotImplementedError


@dataclass
class Plane(Figure):
    a: float
    b: float
    c: float
    d: float

    def __post_init__(self):
        self.coeff_vec = make_point(self.a, self.b, self.c)

    def intersect(self, ray: Ray, max_k=None) -> List[Point]:
        denominator = self.coeff_vec @ ray.direction
        if denominator == 0:
            return []
        k = -((self.coeff_vec @ ray.point) + self.d) / denominator
        if k < 0:
            return []
        if max_k is not None and k > max_k:
            return []
        return [ray.point + ray.direction * k]

    def perpendicular(self, point: Point) -> Ray:
        assert [self.a, self.b, self.c].count(
            0
        ) == 2, "only simple planes are supported"
        if self.a != 0:
            return Ray.from_points(
                point, make_point(get_x(point) + 1, get_y(point), get_z(point))
            )
        if self.b != 0:
            return Ray.from_points(
                point, make_point(get_x(point), get_y(point) + 1, get_z(point))
            )
        if self.c != 0:
            return Ray.from_points(
                point, make_point(get_x(point), get_y(point), get_z(point) + 1)
            )
        raise ValueError(f"only simple planes are supported: {self!r}")


@dataclass(frozen=True)
class Sphere(Figure):
    center: Point
    radius: float

    def intersect(self, ray: Ray, max_k=None) -> List[Point]:
        v = ray.point - self.center
        a = ray.direction @ ray.direction
        b = 2 * (v @ ray.direction)
        c = (v @ v) - self.radius ** 2
        return [
            ray.point + ray.direction * k
            for k in algebra.solve_quadratic(a, b, c)
            if k >= 0 and (max_k is None or k < max_k)
        ]

    def perpendicular(self, point: Point) -> Ray:
        return Ray.from_points(self.center, point)
