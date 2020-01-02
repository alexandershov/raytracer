import math
from typing import List

import pytest
from raytracer import geometry

START = geometry.Point(3, 2, 1)
AFTER_START = geometry.Point(9, 6, 3)
DIRECTION = geometry.Vector(6, 4, 2)
RAY = geometry.Ray.from_points(geometry.Point(1, 0, 0), geometry.Point(0, 0, 0))
CENTER = geometry.Point(5, 10, 9)


def test_sub_points():
    assert (AFTER_START - START) == DIRECTION


def test_vector_length():
    vector = geometry.Vector(3, 4, 5)
    assert abs(vector) == pytest.approx(math.sqrt(50))


def test_create_ray_from_start_and_direction():
    ray = geometry.Ray(START, DIRECTION)
    assert ray.start == START
    assert ray.direction == DIRECTION


def test_create_ray_from_points():
    ray = geometry.Ray.from_points(START, AFTER_START)
    assert ray.start == START
    assert ray.direction == DIRECTION


def test_plane():
    plane = geometry.Plane(1, 2, 3, 4)
    assert plane.a == 1
    assert plane.b == 2
    assert plane.c == 3
    assert plane.d == 4


def test_sphere():
    sphere = geometry.Sphere(CENTER, 10)
    assert sphere.center == CENTER
    assert sphere.radius == 10


@pytest.mark.parametrize(
    "ray, figure, expected",
    [
        (RAY, geometry.Plane(1, 0, 0, 0), [geometry.Point(0, 0, 0)]),
        (
            geometry.Ray(geometry.Point(8, 9, 10), geometry.Vector(-5, -6, -7)),
            geometry.Plane(1, 2, 3, 4),
            [
                geometry.Point(
                    0.10526315789473628, -0.47368421052631504, -1.0526315789473681
                )
            ],
        ),
        (RAY, geometry.Plane(1, 0, 0, -2), []),
        (RAY, geometry.Plane(0, 0, 1, -1), []),
        (RAY, geometry.Plane(0, 0, 1, 0), []),
    ],
)
def test_intersect_ray(ray, figure, expected):
    assert same_points(ray.intersect(figure), expected)


def same_points(xs: List[geometry.Point], ys: List[geometry.Point]) -> bool:
    if len(xs) != len(ys):
        return False
    xs_sorted = sort_by_distance_to_origin(xs)
    ys_sorted = sort_by_distance_to_origin(ys)
    return all(are_close(a, b) for a, b in zip(xs_sorted, ys_sorted))


def are_close(a: geometry.Point, b: geometry.Point) -> bool:
    return abs(b - a) == pytest.approx(0)


def sort_by_distance_to_origin(points: List[geometry.Point]) -> List[geometry.Point]:
    return sorted(points, key=distance_to_origin)


def distance_to_origin(point: geometry.Point) -> float:
    return abs(point - geometry.Point(0, 0, 0))
