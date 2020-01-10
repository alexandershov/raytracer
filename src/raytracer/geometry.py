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


def make_line_segment(start: Point, to: Point) -> LineSegment:
    return LineSegment(_point=start, _direction=to - start, min_k=0, max_k=1)


def make_ray(start: Point, to: Point) -> Ray:
    return Ray(_point=start, _direction=to - start, min_k=0)


def make_infinite_line(a: Point, b: Point) -> InfiniteLine:
    return InfiniteLine(a, b - a)


def make_plane(a: float, b: float, c: float, d: float) -> Plane:
    return Plane(make_point(a, b, c), d)


class Line(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def point(self) -> Point:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def direction(self) -> Point:
        raise NotImplementedError

    @abc.abstractmethod
    def is_mine(self, k: float) -> bool:
        raise NotImplementedError

    def __post_init__(self):
        assert not np.array_equal(self.direction, make_point(0, 0, 0))


@dataclass(frozen=True)
class LineSegment(Line):
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
class InfiniteLine(Line):
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
class Ray(Line):
    _point: Point
    _direction: Point
    min_k: float

    @property
    def point(self) -> Point:
        return self._point

    @property
    def direction(self) -> Point:
        return self._direction

    def perpendicular(self, other: InfiniteLine) -> Ray:
        other_direction_squared = other.direction @ other.direction
        k = (other.direction @ (self.point - other.point)) / other_direction_squared
        return make_ray(self.point, _point_at(other, k))

    def mirror(self, axis: InfiniteLine) -> Ray:
        perpendicular = self.perpendicular(axis)
        return make_ray(axis.point, _point_at(perpendicular, 2))

    def is_mine(self, k: float) -> bool:
        return k >= self.min_k


class Figure(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def intersections(self, line: Line) -> List[Point]:
        raise NotImplemented

    @abc.abstractmethod
    def perpendicular(self, point: Point) -> Ray:
        raise NotImplementedError


@dataclass
class Plane(Figure):
    coeffs: Point
    d: float

    def intersections(self, line: Line) -> List[Point]:
        # solving equation tk + s = 0
        s = (self.coeffs @ line.point) + self.d
        t = self.coeffs @ line.direction
        if t == 0:
            return []
        return _get_line_points_at_ks(line, [-s / t])

    def perpendicular(self, point: Point) -> InfiniteLine:
        assert self._get_num_zero_coeffs() == 2, "only simple planes are supported"
        delta = _normalize(self.coeffs)
        return make_infinite_line(point, point + make_point(*delta))

    def _get_num_zero_coeffs(self) -> int:
        return sum(self.coeffs == 0)


@dataclass(frozen=True)
class Sphere(Figure):
    center: Point
    radius: float

    def intersections(self, line: Line) -> List[Point]:
        v = line.point - self.center
        a = line.direction @ line.direction
        b = 2 * (v @ line.direction)
        c = (v @ v) - self.radius ** 2
        return _get_line_points_at_ks(line, algebra.solve_quadratic(a, b, c))

    def perpendicular(self, point: Point) -> InfiniteLine:
        return make_infinite_line(self.center, point)


def _normalize(point: Point) -> Point:
    return point / np.linalg.norm(point)


def _get_line_points_at_ks(line: Line, ks: List[float]) -> List[Point]:
    return [_point_at(line, k) for k in ks if line.is_mine(k)]


def _point_at(line: Line, k: float):
    return line.point + line.direction * k
