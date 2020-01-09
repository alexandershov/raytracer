from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import List

import numpy as np

from raytracer.interval import Interval
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


def make_segment(start: Point, to: Point) -> Line:
    return Line(start, to - start, Interval(min=0, max=1))


def make_ray(start: Point, to: Point) -> Line:
    return Line(start, to - start, Interval(min=0))


@dataclass(frozen=True)
class Line:
    point: Point
    direction: Point
    ks: Interval

    def intersect(self, figure: Figure) -> List[Point]:
        return figure.intersect(self)

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
    def intersect(self, line: Line) -> List[Point]:
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

    def intersect(self, line: Line) -> List[Point]:
        denominator = self.coeff_vec @ line.direction
        if denominator == 0:
            return []
        k = -((self.coeff_vec @ line.point) + self.d) / denominator
        if k not in line.ks:
            return []
        return [line.point + line.direction * k]

    def perpendicular(self, point: Point) -> Line:
        assert [self.a, self.b, self.c].count(
            0
        ) == 2, "only simple planes are supported"
        delta = self.coeff_vec / np.linalg.norm(self.coeff_vec)
        return make_ray(point, point + delta)


@dataclass(frozen=True)
class Sphere(Figure):
    center: Point
    radius: float

    def intersect(self, line: Line) -> List[Point]:
        v = line.point - self.center
        a = line.direction @ line.direction
        b = 2 * (v @ line.direction)
        c = (v @ v) - self.radius ** 2
        return [
            line.point + line.direction * k
            for k in algebra.solve_quadratic(a, b, c)
            if k in line.ks
        ]

    def perpendicular(self, point: Point) -> Line:
        return make_ray(self.center, point)
