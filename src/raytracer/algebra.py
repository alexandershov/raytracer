import math

from typing import List


def solve_quadratic(a, b, c) -> List[float]:
    if a == 0 and b == 0:
        raise ValueError(f'not a quadratic equation: {a}x^2 + {b}x + c')
    if a == 0:
        return [-c / b]
    d = (b ** 2 - 4 * a * c)
    if d < 0:
        return []
    return list({(-b - math.sqrt(d)) / (2 * a), (-b + math.sqrt(d)) / (2 * a)})
