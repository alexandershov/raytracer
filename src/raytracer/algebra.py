import math
from typing import List


def solve_quadratic(a, b, c) -> List[float]:
    if a == 0:
        return _solve_linear(b, c)
    d = b ** 2 - 4 * a * c
    if d < 0:
        return []
    return list({(-b - math.sqrt(d)) / (2 * a), (-b + math.sqrt(d)) / (2 * a)})


def _solve_linear(a, b) -> List[float]:
    if a == 0:
        raise ValueError(f"`{a}x + {b} = 0` is not a function")
    return [-b / a]
