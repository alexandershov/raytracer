import math
from typing import List


def solve_quadratic(a, b, c) -> List[float]:
    if a == 0:
        return _solve_linear(b, c)
    d = b ** 2 - 4 * a * c
    if d < 0:
        return []
    roots = [(-b + sign * math.sqrt(d)) / (2 * a) for sign in [-1, 1]]
    return _exclude_duplicates(roots)


def _solve_linear(a, b) -> List[float]:
    if a == 0:
        raise ValueError(f"`{a}x + {b} = 0` is not a function")
    return [-b / a]


def _exclude_duplicates(roots: List[float]) -> List[float]:
    # TODO: is using set on floats okay?
    return list(set(roots))
