from raytracer import geometry

START = geometry.Point(3, 2, 1)
AFTER_START = geometry.Point(9, 6, 3)
DIRECTION = geometry.Vector(6, 4, 2)
CENTER = geometry.Point(5, 10, 9)


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


def test_intersect_ray_with_plane():
    ray = geometry.Ray.from_points(
        geometry.Point(1, 0, 0), geometry.Point(0, 0, 0),
    )
    plane = geometry.Plane(1, 0, 0, 0)
    assert ray.intersect(plane) == geometry.Point(0, 0, 0)
