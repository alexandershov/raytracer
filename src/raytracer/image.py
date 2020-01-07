from __future__ import annotations

from dataclasses import dataclass

import PIL.Image


@dataclass(frozen=True)
class Color:
    red: int
    green: int
    blue: int

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            return NotImplemented
        assert other >= 0
        return Color(
            red=min(int(self.red * other), 255),
            green=min(int(self.green * other), 255),
            blue=min(int(self.blue * other), 255),
        )


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
        self._pixels[x, y] = (color.red, color.green, color.blue)
