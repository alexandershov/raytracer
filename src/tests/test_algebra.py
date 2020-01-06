import pytest

from raytracer import algebra


@pytest.mark.parametrize(
    "a, b, c, expected",
    [
        # two roots
        (3, 7, 2, [-2, -1 / 3]),
        # one root
        (1, 10, 25, [-5]),
        # no roots
        (1, 0, 4, []),
        # b == 0
        (1, 0, -4, [-2, 2]),
        # linear
        (0, 2, 4, [-2]),
    ],
)
def test_solve_quadratic(a, b, c, expected):
    assert algebra.solve_quadratic(a, b, c) == pytest.approx(expected)


def test_solve_quadratic_failure():
    with pytest.raises(ValueError):
        algebra.solve_quadratic(0, 0, 0)
