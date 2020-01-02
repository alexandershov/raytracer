from __future__ import annotations

import dataclasses


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


@dataclasses.dataclass(frozen=True)
class Ray:
    start: Point
    direction: Vector

    @staticmethod
    def from_points(start: Point, after_start: Point) -> Ray:
        assert start != after_start
        return Ray(start, after_start - start)
