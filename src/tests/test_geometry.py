import math
from typing import List

import pytest
import numpy as np
from raytracer import geometry

Point = geometry.make_point
Plane = geometry.make_plane


def Sphere(x1, y1, z1, radius):
    center = Point(x1, y1, z1)
    return geometry.Sphere(center, radius)


def Ray(x1, y1, z1, placeholder, x2, y2, z2):
    assert placeholder is Ellipsis
    a = Point(x1, y1, z1)
    b = Point(x2, y2, z2)
    return geometry.make_ray(a, b)


def Line(x1, y1, z1, placeholder, x2, y2, z2):
    assert placeholder is Ellipsis
    a = Point(x1, y1, z1)
    b = Point(x2, y2, z2)
    return geometry.make_infinite_line(a, b)


RAY = Ray(1, 0, 0, ..., 0, 0, 0)


def test_make_point():
    point = Point(1, 2, 3)
    assert geometry.get_x(point) == 1
    assert geometry.get_y(point) == 2
    assert geometry.get_z(point) == 3


def test_sub_points():
    assert same_points((Point(9, 6, 3) - Point(3, 2, 1)), Point(6, 4, 2))


def test_mul_point():
    assert same_points(Point(3, 2, 1) * 2, Point(6, 4, 2))


def test_div_point():
    assert close_points(Point(3, 2, 1) / 2, Point(1.5, 1, 0.5))


def test_mat_mul_points():
    assert Point(3, 2, 1) @ Point(9, 6, 3) == 42


def test_vector_length():
    vector = Point(3, 4, 5)
    assert np.linalg.norm(vector) == pytest.approx(math.sqrt(50))


def test_make_ray():
    ray = geometry.make_ray(Point(3, 2, 1), Point(9, 6, 3))
    assert same_points(ray.point, Point(3, 2, 1))
    assert same_points(ray.direction, Point(6, 4, 2))


def test_plane():
    plane = Plane(1, 2, 3, 4)
    assert same_points(plane.coeffs, Point(1, 2, 3))
    assert plane.d == 4


def test_sphere():
    sphere = geometry.Sphere(Point(5, 10, 9), 10)
    assert same_points(sphere.center, Point(5, 10, 9))
    assert sphere.radius == 10


@pytest.mark.parametrize(
    "line, shape, expected",
    [
        (RAY, Plane(1, 0, 0, 0), [Point(0, 0, 0)]),
        (
            Ray(8, 9, 10, ..., 3, 3, 3),
            Plane(1, 2, 3, 4),
            [Point(0.10526315789473628, -0.47368421052631504, -1.0526315789473681)],
        ),
        (RAY, Plane(1, 0, 0, -2), []),
        (RAY, Plane(0, 0, 1, -1), []),
        (RAY, Plane(0, 0, 1, 0), []),
        (RAY, Sphere(0, 0, 0, radius=0.5), [Point(0.5, 0, 0), Point(-0.5, 0, 0)],),
        (RAY, Sphere(10, 0, 0, radius=0.5), []),
        (RAY, Sphere(0, 0, 0, radius=2), [Point(-2, 0, 0)],),
    ],
)
def test_line_intersections(line, shape, expected):
    assert close_intersections(shape.intersections(line), expected)


@pytest.mark.parametrize(
    "ray, other, expected",
    [
        (
            Ray(1, 0, 0, ..., 1, 1, 0),
            Line(0, 0, 0, ..., 0, 1, 0),
            Ray(1, 0, 0, ..., 0, 0, 0),
        ),
        (
            Ray(1, 0, 0, ..., 1, 1, 0),
            Line(0, 1, 0, ..., 0, 2, 0),
            Ray(1, 0, 0, ..., 0, 0, 0),
        ),
    ],
)
def test_ray_perpendicular(ray, other, expected):
    assert close_lines(ray.perpendicular(other), expected)


def test_ray_perpendicular_failure():
    ray = Ray(1, 0, 0, ..., 1, 1, 0)
    line = Line(1, 0, 0, ..., 1, 1, 0)
    with pytest.raises(geometry.InvalidLineError):
        ray.perpendicular(line)


@pytest.mark.parametrize(
    "shape, point, expected",
    [
        (Sphere(0, 0, 0, radius=10), Point(10, 0, 0), Line(0, 0, 0, ..., 10, 0, 0),),
        (Plane(1, 0, 0, -10), Point(10, 0, 0), Line(10, 0, 0, ..., 11, 0, 0),),
        (Plane(0, 1, 0, -10), Point(0, 10, 0), Line(0, 10, 0, ..., 0, 11, 0),),
        (Plane(0, 0, 1, -10), Point(0, 0, 10), Line(0, 0, 10, ..., 0, 0, 11),),
    ],
)
def test_shape_perpendicular(shape, point, expected):
    assert close_lines(shape.perpendicular(point), expected)


def test_sphere_perpendicular_failure():
    sphere = Sphere(0, 0, 0, radius=10)
    with pytest.raises(geometry.InvalidLineError):
        sphere.perpendicular(sphere.center)


@pytest.mark.parametrize(
    "ray, axis, expected",
    [
        (
            Ray(2, 1, 0, ..., 1, 0, 0),
            Line(1, 0, 0, ..., 1, 1, 0),
            Ray(1, 0, 0, ..., 0, 1, 0),
        )
    ],
)
def test_mirror(ray, axis, expected):
    assert close_lines(ray.mirror(axis), expected)


def close_lines(x: geometry.Line, y: geometry.Line) -> bool:
    same_starts = close_points(x.point, y.point)
    same_directions = close_points(normalize(x.direction), normalize(y.direction))
    same_ks = x.ks == y.ks
    return same_starts and same_directions and same_ks


def normalize(x: geometry.Point) -> geometry.Point:
    return x / np.linalg.norm(x)


def same_points(x: geometry.Point, y: geometry.Point) -> bool:
    return np.array_equal(x, y)


def close_intersections(xs: List[geometry.Point], ys: List[geometry.Point]) -> bool:
    if len(xs) != len(ys):
        return False
    xs_sorted = sort_by_distance_to_origin(xs)
    ys_sorted = sort_by_distance_to_origin(ys)
    return all(close_points(a, b) for a, b in zip(xs_sorted, ys_sorted))


def close_points(a: geometry.Point, b: geometry.Point) -> bool:
    return np.linalg.norm(b - a) == pytest.approx(0)


def sort_by_distance_to_origin(points: List[geometry.Point]) -> List[geometry.Point]:
    return sorted(points, key=distance_to_origin)


def distance_to_origin(point: geometry.Point) -> float:
    return np.linalg.norm(point)
