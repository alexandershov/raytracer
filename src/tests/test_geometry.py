import math
from typing import List

import pytest
import numpy as np
from raytracer import geometry

Point = geometry.make_point


def Sphere(x1, y1, z1, placeholder, radius):
    assert placeholder is Ellipsis
    center = Point(x1, y1, z1)
    return geometry.Sphere(center, radius)


def Ray(x1, y1, z1, placeholder, x2, y2, z2):
    assert placeholder is Ellipsis
    a = Point(x1, y1, z1)
    b = Point(x2, y2, z2)
    return geometry.make_ray(a, b)


START = Point(3, 2, 1)
AFTER_START = Point(9, 6, 3)
DIRECTION = Point(6, 4, 2)
RAY = Ray(1, 0, 0, ..., 0, 0, 0)
CENTER = Point(5, 10, 9)


def test_make_point():
    point = Point(1, 2, 3)
    assert geometry.get_x(point) == 1
    assert geometry.get_y(point) == 2
    assert geometry.get_z(point) == 3


def test_sub_points():
    assert np.array_equal((AFTER_START - START), DIRECTION)


def test_mul_point():
    assert np.array_equal(START * 2, Point(6, 4, 2))


def test_div_point():
    assert are_close(START / 2, Point(1.5, 1, 0.5))


def test_mat_mul_points():
    assert START @ AFTER_START == 42


def test_vector_length():
    vector = Point(3, 4, 5)
    assert np.linalg.norm(vector) == pytest.approx(math.sqrt(50))


def test_make_ray():
    ray = geometry.make_ray(START, AFTER_START)
    assert np.array_equal(ray.point, START)
    assert np.array_equal(ray.direction, DIRECTION)


def test_plane():
    plane = geometry.make_plane(1, 2, 3, 4)
    assert np.array_equal(plane.coeffs, Point(1, 2, 3))
    assert plane.d == 4


def test_sphere():
    sphere = geometry.Sphere(CENTER, 10)
    assert np.array_equal(sphere.center, CENTER)
    assert sphere.radius == 10


@pytest.mark.parametrize(
    "line, figure, expected",
    [
        (RAY, geometry.make_plane(1, 0, 0, 0), [Point(0, 0, 0)]),
        (
            Ray(8, 9, 10, ..., 3, 3, 3),
            geometry.make_plane(1, 2, 3, 4),
            [Point(0.10526315789473628, -0.47368421052631504, -1.0526315789473681)],
        ),
        (RAY, geometry.make_plane(1, 0, 0, -2), []),
        (RAY, geometry.make_plane(0, 0, 1, -1), []),
        (RAY, geometry.make_plane(0, 0, 1, 0), []),
        (
            RAY,
            geometry.Sphere(Point(0, 0, 0), 0.5),
            [Point(0.5, 0, 0), Point(-0.5, 0, 0)],
        ),
        (RAY, geometry.Sphere(Point(10, 0, 0), 0.5), []),
        (RAY, geometry.Sphere(Point(0, 0, 0), 2), [Point(-2, 0, 0)],),
    ],
)
def test_line_intersections(line, figure, expected):
    assert same_points(figure.intersections(line), expected)


@pytest.mark.parametrize(
    "line, other, expected",
    [
        (
            geometry.make_ray(Point(1, 0, 0), Point(1, 1, 0)),
            geometry.make_infinite_line(Point(0, 0, 0), Point(0, 1, 0)),
            geometry.make_ray(Point(1, 0, 0), Point(0, 0, 0)),
        ),
        (
            geometry.make_ray(Point(1, 0, 0), Point(1, 1, 0)),
            geometry.make_infinite_line(Point(0, 1, 0), Point(0, 2, 0)),
            geometry.make_ray(Point(1, 0, 0), Point(0, 0, 0)),
        ),
    ],
)
def test_line_perpendicular(line, other, expected):
    assert same_lines(line.perpendicular(other), expected)


@pytest.mark.parametrize(
    "figure, point, expected",
    [
        (
            geometry.Sphere(Point(0, 0, 0), 10),
            Point(10, 0, 0),
            geometry.make_infinite_line(Point(0, 0, 0), Point(10, 0, 0)),
        ),
        (
            geometry.make_plane(1, 0, 0, -10),
            Point(10, 0, 0),
            geometry.make_infinite_line(Point(10, 0, 0), Point(11, 0, 0)),
        ),
        (
            geometry.make_plane(0, 1, 0, -10),
            Point(0, 10, 0),
            geometry.make_infinite_line(Point(0, 10, 0), Point(0, 11, 0)),
        ),
        (
            geometry.make_plane(0, 0, 1, -10),
            Point(0, 0, 10),
            geometry.make_infinite_line(Point(0, 0, 10), Point(0, 0, 11)),
        ),
    ],
)
def test_figure_perpendicular(figure, point, expected):
    assert same_lines(figure.perpendicular(point), expected)


@pytest.mark.parametrize(
    "ray, axis, expected",
    [
        (
            geometry.make_ray(Point(2, 1, 0), Point(1, 0, 0)),
            geometry.make_infinite_line(Point(1, 0, 0), Point(1, 1, 0)),
            geometry.make_infinite_line(Point(1, 0, 0), Point(0, 1, 0)),
        )
    ],
)
def test_mirror(ray, axis, expected):
    assert same_lines(ray.mirror(axis), expected)


def same_lines(x: geometry.Line, y: geometry.Line) -> bool:
    # TODO: should compare instance types
    same_starts = are_close(x.point, y.point)
    same_directions = are_close(normalize(x.direction), normalize(y.direction))
    return same_starts and same_directions


def normalize(x: geometry.Point) -> geometry.Point:
    return x / np.linalg.norm(x)


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
    return np.linalg.norm(point - Point(0, 0, 0))
