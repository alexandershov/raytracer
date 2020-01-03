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


def test_solid_material():
    material = scene.Solid(color=image.Color.black())
    assert material.get_color(geometry.Point(0, 0, 0)) == image.Color.black()


def test_squared_project_to_xy():
    point = geometry.Point(3, 4, 5)
    expected = geometry.Point(3, 4, 0)
    assert scene.Squared.project_to_xy(point) == expected


def test_squared_project_to_xz():
    point = geometry.Point(3, 4, 5)
    expected = geometry.Point(3, 0, 5)
    assert scene.Squared.project_to_xz(point) == expected
