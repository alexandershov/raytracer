import abc
from dataclasses import dataclass
from typing import Callable

from raytracer import geometry
from raytracer.color import Color


class Material(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_color(self, point: geometry.Point) -> Color:
        raise NotImplementedError


@dataclass(frozen=True)
class Monochrome(Material):
    color: Color

    def get_color(self, point: geometry.Point) -> Color:
        return self.color


@dataclass(frozen=True)
class Checkered(Material):
    square_width: float
    lighter: Color
    darker: Color
    projection: Callable

    @staticmethod
    def project_to_local_xy(point: geometry.Point) -> geometry.Point:
        return geometry.make_point(geometry.get_x(point), geometry.get_y(point), 0)

    @staticmethod
    def project_to_local_xz(point: geometry.Point) -> geometry.Point:
        return geometry.make_point(geometry.get_x(point), geometry.get_z(point), 0)

    @staticmethod
    def project_to_local_yz(point: geometry.Point) -> geometry.Point:
        return geometry.make_point(geometry.get_y(point), geometry.get_z(point), 0)

    def get_color(self, point: geometry.Point) -> Color:
        local = self.projection(point)
        x = geometry.get_x(local)
        y = geometry.get_y(local)
        if (self._get_square_index(x) + self._get_square_index(y)) % 2:
            return self.darker
        return self.lighter

    def _get_square_index(self, coordinate: float) -> int:
        return int(coordinate // self.square_width)


class Mirror(Material):
    def get_color(self, point: geometry.Point) -> Color:
        raise NotImplemented("should never be called")
