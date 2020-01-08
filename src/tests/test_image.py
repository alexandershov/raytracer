import pytest

from raytracer.color import Palette
from raytracer.image import Image


def test_image():
    image = Image(300, 200)
    image.set_pixel(5, 10, Palette.BLACK)
    assert image.get_pixel(5, 10) == Palette.BLACK


def test_set_pixel_out_of_bounds():
    image = Image(300, 200)
    with pytest.raises(ValueError):
        image.set_pixel(300, 199, Palette.BLACK)
