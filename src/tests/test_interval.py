import pytest

from raytracer.interval import Interval


POSITIVE_OR_ZERO = Interval(min=0)
NEGATIVE_OR_ZERO = Interval(max=0)
ZERO_TO_ONE = Interval(min=0, max=1)


@pytest.mark.parametrize(
    "interval, value, expected",
    [
        (POSITIVE_OR_ZERO, 5, True),
        (POSITIVE_OR_ZERO, 0, True),
        (POSITIVE_OR_ZERO, -1, False),
        (NEGATIVE_OR_ZERO, 5, False),
        (NEGATIVE_OR_ZERO, 0, True),
        (NEGATIVE_OR_ZERO, -1, True),
        (ZERO_TO_ONE, 0, True),
        (ZERO_TO_ONE, 1, True),
        (ZERO_TO_ONE, 0.5, True),
        (ZERO_TO_ONE, 2, False),
        (ZERO_TO_ONE, -1, False),
    ],
)
def test_contains(interval, value, expected):
    assert (value in interval) is expected