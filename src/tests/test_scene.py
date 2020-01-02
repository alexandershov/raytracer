from raytracer import geometry
from raytracer import image
from raytracer import scene


def test_scene():
    floor = scene.Thing(
        figure=geometry.Plane(0, 1, 0, 200), material=scene.Solid(image.Color.black())
    )

    sphere = scene.Thing(
        geometry.Sphere(center=geometry.Point(150, -150, 0), radius=30),
        material=scene.Solid(image.Color.grey()),
    )
    s = scene.Scene([floor, sphere])
    assert len(list(s)) == 2
