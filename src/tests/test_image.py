from raytracer.color import Palette
from raytracer.image import Image


def test_image():
    image = Image(300, 200)
    image.set_pixel(5, 10, Palette.BLACK)
