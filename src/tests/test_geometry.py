from raytracer import geometry


def test_ray():
    start = geometry.Point(0, 0, 0)
    direction = geometry.Vector(1, 1, 1)
    ray = geometry.Ray(start, direction)
    assert ray.start == start
    assert ray.direction == direction
