from __future__ import annotations

import abc
from dataclasses import dataclass

import PIL.Image


@dataclass(frozen=True)
class Color:
    red: int
    green: int
    blue: int

    # TODO: black/white/grey is method, red/green/blue is property, that's confusing
    @staticmethod
    def black() -> Color:
        return Color(0, 0, 0)

    @staticmethod
    def white() -> Color:
        return Color(255, 255, 255)

    @staticmethod
    def grey() -> Color:
        return Color(100, 100, 100)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            return NotImplemented
        assert other >= 0
        return Color(
            red=min(int(self.red * other), 255),
            green=min(int(self.green * other), 255),
            blue=min(int(self.blue * other), 255),
        )


class Image(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def show(self):
        raise NotImplementedError

    @abc.abstractmethod
    def set_pixel(self, x, y, color):
        raise NotImplementedError


class PillowImage(Image):
    def __init__(self, width, height):
        self._image = PIL.Image.new("RGB", (width, height), "white")
        self._pixels = self._image.load()

    def show(self):
        self._image.show()

    def set_pixel(self, x, y, color):
        self._pixels[x, y] = (color.red, color.green, color.blue)
