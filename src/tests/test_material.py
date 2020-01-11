import numpy as np
import pytest

from raytracer import geometry
from raytracer.color import Palette
from raytracer.material import Checkered
from raytracer.material import Monochrome


def test_solid_material():
    material = Monochrome(color=Palette.BLACK)
    assert material.get_color(geometry.make_point(0, 0, 0)) == Palette.BLACK


def test_checkered_project_to_local_xy():
    point = geometry.make_point(3, 4, 5)
    expected = geometry.make_point(3, 4, 0)
    assert np.array_equal(Checkered.project_to_local_xy(point), expected)


def test_checkered_project_to_local_xz():
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
def test_checkered_material(point, expected):
    material = Checkered(
        square_width=20,
        lighter=Palette.WHITE,
        darker=Palette.BLACK,
        projection=Checkered.project_to_local_xy,
    )
    assert material.get_color(point) == expected
