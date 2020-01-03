from raytracer import geometry
from raytracer import image
from raytracer import scene


def test_scene():
    floor = scene.Thing(
        figure=geometry.Plane(0, 1, 0, 200), material=scene.Solid(image.Color.black())
    )

    sphere = scene.Thing(
        geometry.Sphere(center=geometry.Point(150, -150, 150), radius=30),
        material=scene.Solid(image.Color.grey()),
    )
    lights = [geometry.Point(1, 1, 1), geometry.Point(50, 50, 50)]
    camera = geometry.Point(300, 200, -600)
    s = scene.Scene(
        width=600, height=400, camera=camera, lights=lights, things=[floor, sphere]
    )
    assert s.width == 600
    assert s.height == 400
    assert s.camera == camera
    assert s.lights == lights
    assert list(s) == [floor, sphere]


def test_material():
    material = scene.Solid(color=image.Color.black())
    assert material.get_color() == image.Color.black()
