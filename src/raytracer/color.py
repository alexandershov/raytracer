from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int

    _MIN_RGB = 0
    _MAX_RGB = 255

    def __post_init__(self) -> None:
        for rgb in self._components():
            self._check_valid_rgb(rgb)

    def __mul__(self, other) -> Color:
        if not isinstance(other, (int, float)):
            return NotImplemented
        return Color(
            r=self._mul_rgb(self.r, other),
            g=self._mul_rgb(self.g, other),
            b=self._mul_rgb(self.b, other),
        )

    def _mul_rgb(self, x: int, mul: float) -> int:
        if mul < 0:
            raise ValueError(f"can't multiply {self!r} by negative {mul!r}")
        return int(min((x * mul), Color._MAX_RGB))

    def _components(self) -> List[int]:
        return [self.r, self.g, self.b]

    def _check_valid_rgb(self, rgb: int) -> None:
        if not (Color._MIN_RGB <= rgb <= Color._MAX_RGB):
            raise ValueError(self._get_invalid_rgb_msg(rgb))

    def _get_invalid_rgb_msg(self, rgb: int) -> str:
        range_msg = f"{rgb} should be in range [{Color._MIN_RGB}; {Color._MAX_RGB}]"
        return f"{self!r} is not a valid color: {range_msg}"


class Palette:
    BLACK = Color(0, 0, 0)
    GRAY = Color(100, 100, 100)
    WHITE = Color(255, 255, 255)
