from __future__ import annotations

from dataclasses import dataclass

import PIL.Image


@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int

    _MIN_RGB = 0
    _MAX_RGB = 255

    def __post_init__(self):
        for component in [self.r, self.g, self.b]:
            if not (Color._MIN_RGB <= component <= Color._MAX_RGB):
                raise ValueError(f"{self!r} is not a valid color")

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            return NotImplemented
        return Color(
            r=Color._mul_rgb(self.r, other),
            g=Color._mul_rgb(self.g, other),
            b=Color._mul_rgb(self.b, other),
        )

    @staticmethod
    def _mul_rgb(x: int, mul: float) -> int:
        assert mul >= 0
        return min(int(x * mul), Color._MAX_RGB)


class Palette:
    BLACK = Color(0, 0, 0)
    GRAY = Color(100, 100, 100)
    WHITE = Color(255, 255, 255)


class Image:
    def __init__(self, width: int, height: int) -> None:
        self._image = PIL.Image.new("RGB", (width, height), "white")
        self._pixels = self._image.load()

    def show(self) -> None:
        self._image.show()

    def set_pixel(self, x: int, y: int, color: Color) -> None:
        self._pixels[x, y] = (color.r, color.g, color.b)
