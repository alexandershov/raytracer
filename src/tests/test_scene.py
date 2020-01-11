import numpy as np
import pytest

from raytracer import geometry
from raytracer import scene
from raytracer.color import Palette
from raytracer.material import Checkered
from raytracer.material import Monochrome


def test_scene():
    floor = scene.Thing(
        figure=geometry.make_plane(0, 1, 0, 200), material=Monochrome(Palette.BLACK)
    )

    sphere = scene.Thing(
        geometry.Sphere(center=geometry.make_point(150, -150, 150), radius=30),
        material=Monochrome(Palette.GRAY),
    )
    lights = [geometry.make_point(1, 1, 1), geometry.make_point(50, 50, 50)]
    camera = geometry.make_point(300, 200, -600)
    s = scene.Scene(
        width=600, height=400, camera=camera, lights=lights, things=[floor, sphere]
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


def test_solid_material():
    material = Monochrome(color=Palette.BLACK)
    assert material.get_color(geometry.make_point(0, 0, 0)) == Palette.BLACK


def test_squared_project_to_local_xy():
    point = geometry.make_point(3, 4, 5)
    expected = geometry.make_point(3, 4, 0)
    assert np.array_equal(Checkered.project_to_local_xy(point), expected)


def test_squared_project_to_local_xz():
    point = geometry.make_point(3, 4, 5)
    expected = geometry.make_point(3, 5, 0)
    assert np.array_equal(Checkered.project_to_local_xz(point), expected)


@pytest.mark.parametrize(
    "point, expected",
    [
        (geometry.make_point(10, 10, 90), Palette.WHITE),
        (geometry.make_point(-10, -10, 90), Palette.WHITE),
        (geometry.make_point(10, -10, 90), Palette.BLACK),
        (geometry.make_point(30, 10, 90), Palette.BLACK),
    ],
)
def test_squared_material(point, expected):
    material = Checkered(
        width=20,
        lighter=Palette.WHITE,
        darker=Palette.BLACK,
        projection=Checkered.project_to_local_xy,
    )
    assert material.get_color(point) == expected
