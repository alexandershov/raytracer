from raytracer import geometry

START = geometry.Point(3, 2, 1)
AFTER_START = geometry.Point(9, 6, 3)
DIRECTION = geometry.Vector(6, 4, 2)


def test_sub_points():
    assert (AFTER_START - START) == DIRECTION


def test_create_ray_from_start_and_direction():
    ray = geometry.Ray(START, DIRECTION)
    assert ray.start == START
    assert ray.direction == DIRECTION


def test_create_ray_from_points():
    ray = geometry.Ray.from_points(START, AFTER_START)
    assert ray.start == START
    assert ray.direction == DIRECTION