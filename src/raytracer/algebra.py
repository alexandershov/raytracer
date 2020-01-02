import math

from typing import List


def solve_quadratic(a, b, c) -> List[float]:
    d = (b ** 2 - 4 * a * c)
    if d < 0:
        return []
    return list({(-b - math.sqrt(d)) / (2 * a), (-b + math.sqrt(d)) / (2 * a)})
