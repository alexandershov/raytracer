import pytest

from raytracer import algebra


@pytest.mark.parametrize("a, b, c, expected", [(1, 10, 25, [-5]), (1, 0, -4, [-2, 2])])
def test_solve_quadratic(a, b, c, expected):
    assert sorted(algebra.solve_quadratic(a, b, c)) == list(
        map(pytest.approx, expected)
    )
