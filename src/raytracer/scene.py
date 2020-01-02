from __future__ import annotations

import dataclasses
from typing import List

from . import geometry


class Material:
    pass


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


@dataclasses.dataclass(frozen=True)
class Solid(Material):
    color: Color


class Mirror(Material):
    pass


@dataclasses.dataclass(frozen=True)
class Thing:
    figure: geometry.Figure
    material: Material


class Scene:
    def __init__(self, things: List[Thing]):
        self._things = things

    def __iter__(self):
        return iter(self._things)
