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
            return self._solve_linear()
        d = self._get_discriminant()
        if d < 0:
            return []
        roots = [(-self.b + sign * math.sqrt(d)) / (2 * self.a) for sign in [-1, 1]]
        return _exclude_duplicates(roots)

    def _solve_linear(self) -> List[float]:
        assert self.a == 0
        if self.b == 0:
            raise ValueError(f"`{self.b}x + {self.c} = 0` is not a function")
        return [-self.c / self.b]

    def _get_discriminant(self):
        return self.b ** 2 - 4 * self.a * self.c


def _exclude_duplicates(roots: List[float]) -> List[float]:
    assert len(roots) == 2
    if math.isclose(roots[0], roots[1]):
        return [roots[0]]
    return roots
