import math
from typing import List

import pytest
import numpy as np
from raytracer import geometry

START = geometry.from_xyz(3, 2, 1)
AFTER_START = geometry.from_xyz(9, 6, 3)
DIRECTION = geometry.from_xyz(6, 4, 2)
RAY = geometry.Ray.from_points(geometry.from_xyz(1, 0, 0), geometry.from_xyz(0, 0, 0))
CENTER = geometry.from_xyz(5, 10, 9)


def test_point_from_xyz():
    point = geometry.from_xyz(1, 2, 3)
    assert geometry.get_x(point) == 1
    assert geometry.get_y(point) == 2
    assert geometry.get_z(point) == 3


def test_sub_points():
    assert np.array_equal((AFTER_START - START), DIRECTION)


def test_mul_point():
    assert np.array_equal(START * 2, geometry.from_xyz(6, 4, 2))


def test_div_point():
    assert are_close(START / 2, geometry.from_xyz(1.5, 1, 0.5))


def test_mat_mul_points():
    assert START @ AFTER_START == 42


def test_vector_length():
    vector = geometry.from_xyz(3, 4, 5)
    assert np.linalg.norm(vector) == pytest.approx(math.sqrt(50))


def test_create_ray_from_start_and_direction():
    ray = geometry.Ray(START, DIRECTION)
    assert np.array_equal(ray.start, START)
    assert np.array_equal(ray.direction, DIRECTION)


def test_create_ray_from_points():
    ray = geometry.Ray.from_points(START, AFTER_START)
    assert np.array_equal(ray.start, START)
    assert np.array_equal(ray.direction, DIRECTION)


def test_plane():
    plane = geometry.Plane(1, 2, 3, 4)
    assert plane.a == 1
    assert plane.b == 2
    assert plane.c == 3
    assert plane.d == 4


def test_sphere():
    sphere = geometry.Sphere(CENTER, 10)
    assert np.array_equal(sphere.center, CENTER)
    assert sphere.radius == 10


@pytest.mark.parametrize(
    "ray, figure, expected",
    [
        (RAY, geometry.Plane(1, 0, 0, 0), [geometry.from_xyz(0, 0, 0)]),
        (
            geometry.Ray(geometry.from_xyz(8, 9, 10), geometry.from_xyz(-5, -6, -7)),
            geometry.Plane(1, 2, 3, 4),
            [
                geometry.from_xyz(
                    0.10526315789473628, -0.47368421052631504, -1.0526315789473681
                )
            ],
        ),
        (RAY, geometry.Plane(1, 0, 0, -2), []),
        (RAY, geometry.Plane(0, 0, 1, -1), []),
        (RAY, geometry.Plane(0, 0, 1, 0), []),
        (
            RAY,
            geometry.Sphere(geometry.from_xyz(0, 0, 0), 0.5),
            [geometry.from_xyz(0.5, 0, 0), geometry.from_xyz(-0.5, 0, 0)],
        ),
        (RAY, geometry.Sphere(geometry.from_xyz(10, 0, 0), 0.5), []),
        (
            RAY,
            geometry.Sphere(geometry.from_xyz(0, 0, 0), 2),
            [geometry.from_xyz(-2, 0, 0)],
        ),
    ],
)
def test_intersect_ray(ray, figure, expected):
    assert same_points(ray.intersect(figure), expected)


@pytest.mark.parametrize(
    "ray, other, expected",
    [
        (
            geometry.Ray.from_points(
                geometry.from_xyz(1, 0, 0), geometry.from_xyz(1, 1, 0)
            ),
            geometry.Ray.from_points(
                geometry.from_xyz(0, 0, 0), geometry.from_xyz(0, 1, 0)
            ),
            geometry.Ray.from_points(
                geometry.from_xyz(1, 0, 0), geometry.from_xyz(0, 0, 0)
            ),
        ),
        (
            geometry.Ray.from_points(
                geometry.from_xyz(1, 0, 0), geometry.from_xyz(1, 1, 0)
            ),
            geometry.Ray.from_points(
                geometry.from_xyz(0, 1, 0), geometry.from_xyz(0, 2, 0)
            ),
            geometry.Ray.from_points(
                geometry.from_xyz(1, 0, 0), geometry.from_xyz(0, 0, 0)
            ),
        ),
    ],
)
def test_ray_perpendicular(ray, other, expected):
    assert same_rays(ray.perpendicular(other), expected)


@pytest.mark.parametrize(
    "figure, point, expected",
    [
        (
            geometry.Sphere(geometry.from_xyz(0, 0, 0), 10),
            geometry.from_xyz(10, 0, 0),
            geometry.Ray.from_points(
                geometry.from_xyz(0, 0, 0), geometry.from_xyz(10, 0, 0)
            ),
        ),
        (
            geometry.Plane(1, 0, 0, -10),
            geometry.from_xyz(10, 0, 0),
            geometry.Ray.from_points(
                geometry.from_xyz(10, 0, 0), geometry.from_xyz(11, 0, 0)
            ),
        ),
        (
            geometry.Plane(0, 1, 0, -10),
            geometry.from_xyz(0, 10, 0),
            geometry.Ray.from_points(
                geometry.from_xyz(0, 10, 0), geometry.from_xyz(0, 11, 0)
            ),
        ),
        (
            geometry.Plane(0, 0, 1, -10),
            geometry.from_xyz(0, 0, 10),
            geometry.Ray.from_points(
                geometry.from_xyz(0, 0, 10), geometry.from_xyz(0, 0, 11)
            ),
        ),
    ],
)
def test_figure_perpendicular(figure, point, expected):
    assert same_rays(figure.perpendicular(point), expected)


@pytest.mark.parametrize(
    "ray, axis, expected",
    [
        (
            geometry.Ray.from_points(
                geometry.from_xyz(2, 1, 0), geometry.from_xyz(1, 0, 0)
            ),
            geometry.Ray.from_points(
                geometry.from_xyz(1, 0, 0), geometry.from_xyz(1, 1, 0)
            ),
            geometry.Ray.from_points(
                geometry.from_xyz(1, 0, 0), geometry.from_xyz(0, 1, 0)
            ),
        )
    ],
)
def test_mirror(ray, axis, expected):
    assert same_rays(ray.mirror(axis), expected)


def same_rays(x: geometry.Ray, y: geometry.Ray) -> bool:
    return are_close(x.start, y.start) and are_close(x.not_start, y.not_start)


def same_points(xs: List[geometry.Point], ys: List[geometry.Point]) -> bool:
    if len(xs) != len(ys):
        return False
    xs_sorted = sort_by_distance_to_origin(xs)
    ys_sorted = sort_by_distance_to_origin(ys)
    return all(are_close(a, b) for a, b in zip(xs_sorted, ys_sorted))


def are_close(a: geometry.Point, b: geometry.Point) -> bool:
    return np.linalg.norm(b - a) == pytest.approx(0)


def sort_by_distance_to_origin(points: List[geometry.Point]) -> List[geometry.Point]:
    return sorted(points, key=distance_to_origin)


def distance_to_origin(point: geometry.Point) -> float:
    return np.linalg.norm(point - geometry.from_xyz(0, 0, 0))
