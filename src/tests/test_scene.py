import numpy as np

from raytracer import geometry
from raytracer import scene
from raytracer.color import Palette
from raytracer.material import Monochrome


def test_scene():
    floor = scene.Body(
        figure=geometry.make_plane(0, 1, 0, 200), material=Monochrome(Palette.BLACK)
    )

    sphere = scene.Body(
        geometry.Sphere(center=geometry.make_point(150, -150, 150), radius=30),
        material=Monochrome(Palette.GRAY),
    )
    lights = [geometry.make_point(1, 1, 1), geometry.make_point(50, 50, 50)]
    camera = geometry.make_point(300, 200, -600)
    s = scene.Scene(
        bodies=[floor, sphere], camera=camera, lights=lights,
        width=600, height=400,
    )
    assert s.width == 600
    assert s.height == 400
    assert np.array_equal(s.camera, camera)
    assert all(
        np.array_equal(actual_light, expected_light)
        for actual_light, expected_light in zip(s.lights, lights)
    )
    assert len(s.lights) == len(lights)
    assert list(map(id, s)) == [id(floor), id(sphere)]
