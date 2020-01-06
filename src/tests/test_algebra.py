import pytest

from raytracer import algebra


@pytest.mark.parametrize(
    "a, b, c, expected",
    [
        # two roots
        (3, 7, 2, [-2, -1 / 3]),
        # one root
        (1, 10, 25, [-5]),
        # b == 0
        (1, 0, -4, [-2, 2]),
        # no roots
        (1, 0, 4, []),
        # linear
        (0, 2, 4, [-2]),
    ],
)
def test_solve_quadratic(a, b, c, expected):
    assert sorted(algebra.solve_quadratic(a, b, c)) == list(
        map(pytest.approx, expected)
    )
