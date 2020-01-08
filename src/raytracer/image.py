import PIL.Image

from raytracer.color import Color


class Image:
    def __init__(self, width: int, height: int) -> None:
        self._image = PIL.Image.new("RGB", (width, height), "white")
        self._pixels = self._image.load()

    def show(self) -> None:
        self._image.show()

    def set_pixel(self, x: int, y: int, color: Color) -> None:
        self._check_inside(x, y)
        self._pixels[x, y] = (color.r, color.g, color.b)

    def get_pixel(self, x: int, y: int) -> Color:
        # TODO: check that x,y in inside the image
        return Color(*self._pixels[x, y])

    def _check_inside(self, x: int, y: int):
        if not ((0 <= x < self._width) and (0 <= y < self._height)):
            raise ValueError(
                f"Point ({x}, {y}) is out of {self._width}x{self._height} image bounds"
            )

    @property
    def _width(self) -> int:
        return self._image.width

    @property
    def _height(self) -> int:
        return self._image.height
