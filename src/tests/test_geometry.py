from raytracer import geometry


def test_ray():
    start = geometry.Point(3, 2, 1)
    after_start = geometry.Point(9, 6, 3)
    ray = geometry.Ray.from_points(start, after_start)
    assert ray.start == start
    assert ray.direction == geometry.Vector(6, 4, 2)
