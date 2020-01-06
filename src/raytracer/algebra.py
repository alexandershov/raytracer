import math
from typing import List


def solve_quadratic(a, b, c) -> List[float]:
    if a == 0:
        return _solve_linear(b, c)
    d = b ** 2 - 4 * a * c
    if d < 0:
        return []
    # TODO: is using set on floats okay?
    roots = set()
    for sign in [-1, 1]:
        roots.add((-b + sign * math.sqrt(d)) / (2 * a))
    return list(roots)


def _solve_linear(a, b) -> List[float]:
    if a == 0:
        raise ValueError(f"`{a}x + {b} = 0` is not a function")
    return [-b / a]
