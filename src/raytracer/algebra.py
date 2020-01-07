import math
from dataclasses import dataclass
from typing import List


def solve_quadratic(a, b, c) -> List[float]:
    solver = _QuadraticSolver(a, b, c)
    return solver.solve()


@dataclass(frozen=True)
class _QuadraticSolver:
    a: float
    b: float
    c: float

    def solve(self) -> List[float]:
        if self.a == 0:
            return _solve_linear(self.b, self.c)
        d = self.b ** 2 - 4 * self.a * self.c
        if d < 0:
            return []
        roots = [(-self.b + sign * math.sqrt(d)) / (2 * self.a) for sign in [-1, 1]]
        return _exclude_duplicates(roots)


def _solve_linear(a, b) -> List[float]:
    if a == 0:
        raise ValueError(f"`{a}x + {b} = 0` is not a function")
    return [-b / a]


def _exclude_duplicates(roots: List[float]) -> List[float]:
    assert len(roots) == 2
    if math.isclose(roots[0], roots[1]):
        return [roots[0]]
    return roots
