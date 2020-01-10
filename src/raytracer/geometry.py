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


def make_segment(start: Point, to: Point) -> LineSegment:
    return LineSegment(_point=start, _direction=to - start, min_k=0, max_k=1)


def make_ray(start: Point, to: Point) -> Ray:
    return Ray(_point=start, _direction=to - start, min_k=0)


def make_line(a: Point, b: Point) -> Line:
    return Line(a, b - a)


def make_plane(a: float, b: float, c: float, d: float) -> Plane:
    return Plane(make_point(a, b, c), d)


class Straight(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def point(self) -> Point:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def direction(self) -> Point:
        pass

    def point_at(self, k: float) -> Point:
        return self.point + self.direction * k

    @abc.abstractmethod
    def is_mine(self, k: float) -> bool:
        raise NotImplementedError


@dataclass(frozen=True)
class LineSegment(Straight):
    _point: Point
    _direction: Point
    min_k: float
    max_k: float

    @property
    def point(self) -> Point:
        return self._point

    @property
    def direction(self) -> Point:
        return self._direction

    def is_mine(self, k: float) -> bool:
        return self.min_k <= k <= self.max_k


@dataclass(frozen=True)
class Line(Straight):
    _point: Point
    _direction: Point

    @property
    def point(self) -> Point:
        return self._point

    @property
    def direction(self) -> Point:
        return self._direction

    def is_mine(self, k: float) -> bool:
        return True


@dataclass(frozen=True)
class Ray(Straight):
    _point: Point
    _direction: Point
    min_k: float

    @property
    def point(self) -> Point:
        return self._point

    @property
    def direction(self) -> Point:
        return self._direction

    def __post_init__(self):
        assert not np.array_equal(self.direction, make_point(0, 0, 0))

    def perpendicular(self, other: Ray) -> Ray:
        k = (other.direction @ (self.point - other.point)) / (
                other.direction @ other.direction
        )
        p = other.point_at(k)
        return make_ray(self.point, p)

    def mirror(self, axis: Ray) -> Ray:
        perpendicular = self.perpendicular(axis)
        return make_ray(axis.point, perpendicular.point_at(2))

    def point_at(self, k: float) -> Point:
        return self.point + self.direction * k

    def is_mine(self, k: float) -> bool:
        return k >= self.min_k


class Figure(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def intersections(self, line: Ray) -> List[Point]:
        raise NotImplemented

    @abc.abstractmethod
    def perpendicular(self, point: Point) -> Ray:
        raise NotImplementedError


@dataclass
class Plane(Figure):
    coeffs: Point
    d: float

    def intersections(self, line: Ray) -> List[Point]:
        # solving equation tk + s = 0
        s = (self.coeffs @ line.point) + self.d
        t = self.coeffs @ line.direction
        if t == 0:
            return []
        return _get_line_points_at_ks(line, [-s / t])

    def perpendicular(self, point: Point) -> Ray:
        assert self._get_num_zero_coeffs() == 2, "only simple planes are supported"
        delta = _normalize(self.coeffs)
        return make_line(point, point + make_point(*delta))

    def _get_num_zero_coeffs(self) -> int:
        return sum(self.coeffs == 0)


@dataclass(frozen=True)
class Sphere(Figure):
    center: Point
    radius: float

    def intersections(self, line: Ray) -> List[Point]:
        v = line.point - self.center
        a = line.direction @ line.direction
        b = 2 * (v @ line.direction)
        c = (v @ v) - self.radius ** 2
        return _get_line_points_at_ks(line, algebra.solve_quadratic(a, b, c))

    def perpendicular(self, point: Point) -> Ray:
        return make_line(self.center, point)


def _normalize(point: Point) -> Point:
    return point / np.linalg.norm(point)


def _get_line_points_at_ks(line: Ray, ks: List[float]) -> List[Point]:
    return [line.point_at(k) for k in ks if line.is_mine(k)]
