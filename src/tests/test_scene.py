import numpy as np
import pytest

from raytracer import geometry
from raytracer import image
from raytracer import scene


def test_scene():
    floor = scene.Thing(
        figure=geometry.Plane(0, 1, 0, 200), material=scene.Solid(image.Color.black())
    )

    sphere = scene.Thing(
        geometry.Sphere(center=geometry.from_xyz(150, -150, 150), radius=30),
        material=scene.Solid(image.Color.grey()),
    )
    lights = [geometry.from_xyz(1, 1, 1), geometry.from_xyz(50, 50, 50)]
    camera = geometry.from_xyz(300, 200, -600)
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
    assert list(map(id, s)) == [id(floor), id(sphere)]


def test_solid_material():
    material = scene.Solid(color=image.Color.black())
    assert material.get_color(geometry.from_xyz(0, 0, 0)) == image.Color.black()


def test_squared_project_to_local_xy():
    point = geometry.from_xyz(3, 4, 5)
    expected = geometry.from_xyz(3, 4, 0)
    assert np.array_equal(scene.Squared.project_to_local_xy(point), expected)


def test_squared_project_to_local_xz():
    point = geometry.from_xyz(3, 4, 5)
    expected = geometry.from_xyz(3, 5, 0)
    assert np.array_equal(scene.Squared.project_to_local_xz(point), expected)


@pytest.mark.parametrize(
    "point, expected",
    [
        (geometry.from_xyz(10, 10, 90), image.Color.white()),
        (geometry.from_xyz(-10, -10, 90), image.Color.white()),
        (geometry.from_xyz(10, -10, 90), image.Color.black()),
        (geometry.from_xyz(30, 10, 90), image.Color.black()),
    ],
)
def test_squared_material(point, expected):
    material = scene.Squared(
        width=20,
        white=image.Color.white(),
        black=image.Color.black(),
        projection=scene.Squared.project_to_local_xy,
    )
    assert material.get_color(point) == expected
