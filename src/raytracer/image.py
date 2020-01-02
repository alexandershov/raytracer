from __future__ import annotations

import abc
import dataclasses

import PIL.Image


@dataclasses.dataclass(frozen=True)
class Color:
    red: int
    green: int
    blue: int

    @staticmethod
    def black() -> Color:
        return Color(0, 0, 0)

    @staticmethod
    def white() -> Color:
        return Color(255, 255, 255)

    @staticmethod
    def grey() -> Color:
        return Color(100, 100, 100)


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
