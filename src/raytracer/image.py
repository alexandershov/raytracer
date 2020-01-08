import PIL.Image

from raytracer.color import Color


class Image:
    def __init__(self, width: int, height: int) -> None:
        self._image = PIL.Image.new("RGB", (width, height), "white")
        self._pixels = self._image.load()

    def show(self) -> None:
        self._image.show()

    def set_pixel(self, x: int, y: int, color: Color) -> None:
        self._pixels[x, y] = (color.r, color.g, color.b)

    def get_pixel(self, x: int, y: int) -> Color:
        return Color(*self._pixels[x, y])
