import dataclasses


@dataclasses.dataclass(frozen=True)
class Point:
    x: float
    y: float
    z: float


@dataclasses.dataclass(frozen=True)
class Ray:
    start: Point
    direction: Point
