import math

from typing import List


def solve_quadratic(a, b, c) -> List[float]:
    d = math.sqrt(b ** 2 - 4 * a * c)
    return list({(-b - d) / (2 * a), (-b + d) / (2 * a)})
