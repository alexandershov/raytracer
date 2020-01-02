from raytracer import geometry


def test_sub_points():
    a = geometry.Point(3, 2, 1)
    b = geometry.Point(9, 6, 3)
    assert (b - a) == geometry.Vector(6, 4, 2)


def test_create_ray_from_start_and_direction():
    start = geometry.Point(3, 2, 1)
    direction = geometry.Vector(6, 4, 2)
    ray = geometry.Ray(start, direction)
    assert ray.start == start
    assert ray.direction == direction


def test_create_ray_from_points():
    start = geometry.Point(3, 2, 1)
    after_start = geometry.Point(9, 6, 3)
    ray = geometry.Ray.from_points(start, after_start)
    assert ray.start == start
    assert ray.direction == geometry.Vector(6, 4, 2)
